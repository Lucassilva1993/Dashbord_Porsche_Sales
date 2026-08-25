import re
import pandas as pd
from datetime import datetime

SRC = "/mnt/user-data/uploads/Planilha_base_Porsche.xlsx"
OUT = "/home/claude/Planilha_Porsche_Sanitizada.xlsx"

df = pd.read_excel(SRC, dtype=str)
df = df.fillna("")

# ---------------------------------------------------------------------------
# Word-to-number helper (English number words -> integer)
# ---------------------------------------------------------------------------
ONES = {"zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,
        "eight":8,"nine":9}
TEENS = {"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,
         "sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19}
TENS = {"twenty":20,"thirty":30,"forty":40,"fifty":50,"sixty":60,"seventy":70,
        "eighty":80,"ninety":90}
SCALES = {"hundred":100,"thousand":1000,"million":1000000}

def word2num(words):
    total = 0
    current = 0
    for w in words:
        w = w.lower()
        if w in ONES:
            current += ONES[w]
        elif w in TEENS:
            current += TEENS[w]
        elif w in TENS:
            current += TENS[w]
        elif w == "hundred":
            current = (current if current else 1) * 100
        elif w in SCALES:
            total += (current if current else 1) * SCALES[w]
            current = 0
        # unknown words (miles, usd, dollars, and, etc.) are ignored
    return total + current

# ---------------------------------------------------------------------------
# 1) sale_date -> SaleDateSanitized
# ---------------------------------------------------------------------------
DATE_FORMATS = [
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%Y.%m.%d",
    "%m/%d/%Y",
    "%m/%d/%y",
    "%m-%d-%y",
    "%B %d, %Y",
    "%B %d %Y",
    "%b %d, %Y",
    "%b %d %Y",
]

def parse_date(raw):
    s = str(raw).strip()
    if not s:
        return "INVALID"
    m = re.match(r'^(\d{4}-\d{2}-\d{2}) \d{2}:\d{2}:\d{2}$', s)
    if m:
        try:
            d = datetime.strptime(m.group(1), "%Y-%m-%d")
            return d.strftime("%Y-%m-%d")
        except ValueError:
            return "INVALID"
    s_clean = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', s, flags=re.IGNORECASE)
    for fmt in DATE_FORMATS:
        try:
            d = datetime.strptime(s_clean, fmt)
            return d.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return "INVALID"

# ---------------------------------------------------------------------------
# 2) porsche_model -> PorscheModelSanitized
# ---------------------------------------------------------------------------
CANONICAL_MODELS = [
    "911 Carrera","911 Carrera S","911 Carrera GTS","911 Turbo","911 Turbo S",
    "911 GT3","911 GT3 RS","911 Dakar","911 Targa 4","911 Targa 4S",
    "718 Cayman","718 Cayman S","718 Cayman GT4 RS","718 Boxster","718 Boxster GTS",
    "718 Spyder RS","Cayenne","Cayenne S","Cayenne Coupe","Cayenne E-Hybrid",
    "Cayenne Turbo","Cayenne Turbo GT","Macan","Macan S","Macan T","Macan GTS",
    "Macan Electric","Panamera","Panamera 4","Panamera 4S","Panamera Turbo",
    "Panamera Turbo S","Panamera 4 E-Hybrid","Taycan","Taycan 4S","Taycan GTS",
    "Taycan Turbo","Taycan Turbo S","Taycan Cross Turismo",
]
CANONICAL_LOOKUP = {m.lower(): m for m in CANONICAL_MODELS}

def smart_title(s):
    words = s.split()
    out = []
    for w in words:
        if any(c.isdigit() for c in w) or w.isupper():
            out.append(w)
        else:
            out.append(w[:1].upper() + w[1:].lower() if w else w)
    return " ".join(out)

def parse_model(raw):
    s = str(raw).strip()
    if not s:
        return "INVALID"
    key = s.lower()
    if key in CANONICAL_LOOKUP:
        return CANONICAL_LOOKUP[key]
    return smart_title(s)

# ---------------------------------------------------------------------------
# 3) model_year -> ModelYearSanitized
# ---------------------------------------------------------------------------
def parse_year(raw):
    s = str(raw).strip().lower()
    if not s:
        return "INVALID"
    if re.fullmatch(r'\d{4}', s):
        year = int(s)
    else:
        m = re.fullmatch(r'20[-\s](\d{2})', s)
        if m:
            year = 2000 + int(m.group(1))
        else:
            words = re.split(r'[\s-]+', s)
            words = [w for w in words if w]
            if words and words[0] == "twenty" and len(words) > 1:
                year = 2000 + word2num(words[1:])
            else:
                year = word2num(words)
    if 1990 <= year <= 2035:
        return str(year)
    return "INVALID"

# ---------------------------------------------------------------------------
# 4) sale_price -> SalesPriceSanitized
# ---------------------------------------------------------------------------
def parse_price(raw):
    s = str(raw).strip()
    if not s:
        return "INVALID"
    if not re.search(r'\d', s):
        words = re.findall(r'[a-zA-Z]+', s.lower())
        words = [w for w in words if w not in ("usd", "dollars", "dollar")]
        val = word2num(words)
        return f"{float(val):.2f}"

    s_clean = re.sub(r'(?i)usd|dollars?', '', s)
    s_clean = s_clean.replace('$', '').strip()

    k_suffix = False
    if s_clean.lower().endswith('k'):
        k_suffix = True
        s_clean = s_clean[:-1].strip()

    has_comma = ',' in s_clean
    has_dot = '.' in s_clean

    if has_comma and has_dot:
        last_comma = s_clean.rfind(',')
        last_dot = s_clean.rfind('.')
        if last_dot > last_comma:
            num = s_clean.replace(',', '')
        else:
            num = s_clean.replace('.', '').replace(',', '.')
    elif has_comma:
        after = s_clean.split(',')[-1]
        num = s_clean.replace(',', '.') if len(after) == 2 else s_clean.replace(',', '')
    elif has_dot:
        after = s_clean.split('.')[-1]
        if len(after) == 3:
            num = s_clean.replace('.', '')
        else:
            num = s_clean
    else:
        num = s_clean

    try:
        val = float(num)
    except ValueError:
        return "INVALID"
    if k_suffix:
        val *= 1000
    return f"{val:.2f}"

# ---------------------------------------------------------------------------
# 5) vehicle_mileage -> VehicleMileageSanitized
# ---------------------------------------------------------------------------
KM_TO_MI = 0.621371

def parse_mileage(raw):
    s = str(raw).strip()
    if not s:
        return "0"
    low = s.lower()
    is_km = bool(re.search(r'\bkm\b', low))

    s_num = re.sub(r'(?i)\bkm\b', '', s)
    s_num = re.sub(r'(?i)\bmiles?\b', '', s_num)
    s_num = re.sub(r'(?i)\bmi\b\.?', '', s_num)
    s_num = s_num.replace(':', '').strip()

    if not re.search(r'\d', s_num):
        words = re.findall(r'[a-zA-Z]+', low)
        val = word2num(words)
        return str(int(round(val)))

    s_num = re.sub(r'[a-zA-Z]', '', s_num).strip()

    has_comma = ',' in s_num
    has_dot = '.' in s_num
    if has_comma:
        num = s_num.replace(',', '')
    elif has_dot:
        after = s_num.split('.')[-1]
        num = s_num.replace('.', '') if len(after) == 3 else s_num
    else:
        num = s_num

    try:
        val = float(num)
    except ValueError:
        return "INVALID"
    if is_km:
        val = val * KM_TO_MI
    return str(int(round(val)))

# ---------------------------------------------------------------------------
# 6) payment_method -> PayMethodSanitized
# ---------------------------------------------------------------------------
def parse_payment(raw):
    s = str(raw).strip()
    if not s:
        return "INVALID"
    low = s.lower()
    if 'debit' in low:
        return 'Debit Card'
    if 'credit' in low:
        return 'Credit Card'
    if 'crypto' in low:
        return 'Crypto Payment'
    if 'ach' in low:
        return 'ACH Payment'
    if 'wire' in low:
        return 'Wire Transfer'
    if 'bank' in low and 'transfer' in low:
        return 'Bank Transfer'
    if 'lease' in low or 'leasing' in low:
        return 'Lease'
    if 'financ' in low:
        return 'Financing'
    if 'cash' in low:
        return 'Cash'
    return smart_title(s)

# ---------------------------------------------------------------------------
# 7) city -> CitySanitized
# ---------------------------------------------------------------------------
def parse_city(raw):
    s = str(raw).strip()
    if not s:
        return "INVALID"
    return s.title()

# ---------------------------------------------------------------------------
# 8) state -> StateSanitized
# ---------------------------------------------------------------------------
STATE_TO_ABBR = {
    "alabama":"AL","alaska":"AK","arizona":"AZ","arkansas":"AR","california":"CA",
    "colorado":"CO","connecticut":"CT","delaware":"DE","florida":"FL","georgia":"GA",
    "hawaii":"HI","idaho":"ID","illinois":"IL","indiana":"IN","iowa":"IA",
    "kansas":"KS","kentucky":"KY","louisiana":"LA","maine":"ME","maryland":"MD",
    "massachusetts":"MA","michigan":"MI","minnesota":"MN","mississippi":"MS",
    "missouri":"MO","montana":"MT","nebraska":"NE","nevada":"NV",
    "new hampshire":"NH","new jersey":"NJ","new mexico":"NM","new york":"NY",
    "north carolina":"NC","north dakota":"ND","ohio":"OH","oklahoma":"OK",
    "oregon":"OR","pennsylvania":"PA","rhode island":"RI","south carolina":"SC",
    "south dakota":"SD","tennessee":"TN","texas":"TX","utah":"UT","vermont":"VT",
    "virginia":"VA","washington":"WA","west virginia":"WV","wisconsin":"WI",
    "wyoming":"WY","district of columbia":"DC",
}
VALID_ABBR = set(STATE_TO_ABBR.values())

def parse_state(raw):
    s = str(raw).strip()
    if not s:
        return "INVALID"
    if s.upper() in VALID_ABBR and len(s.strip()) == 2:
        return s.upper()
    low = s.lower()
    if low in STATE_TO_ABBR:
        return STATE_TO_ABBR[low]
    return "INVALID"

# ---------------------------------------------------------------------------
# 9) delivery_status -> DeliveryStatusSanitized
# ---------------------------------------------------------------------------
def parse_delivery(raw):
    s = str(raw).strip()
    if not s:
        return "INVALID"
    clean = re.sub(r'[^a-z\s]', ' ', s.lower().replace('-', ' '))
    clean = re.sub(r'\s+', ' ', clean).strip()
    if 'awaiting' in clean:
        if 'delivery' in clean:
            return 'Awaiting Delivery'
        if 'pickup' in clean:
            return 'Awaiting Pickup'
        if 'review' in clean:
            return 'Awaiting Review'
    if 'pending' in clean:
        if 'approval' in clean:
            return 'Pending Approval'
        if 'review' in clean:
            return 'Pending Review'
        return 'Pending'
    if 'transit' in clean:
        return 'In Transit'
    if 'cancel' in clean:
        return 'Cancelled'
    if 'ship' in clean:
        return 'Shipped'
    if 'deliver' in clean:
        return 'Delivered'
    return smart_title(s)

# ---------------------------------------------------------------------------
# Apply all sanitizers
# ---------------------------------------------------------------------------
df["SaleDateSanitized"] = df["sale_date"].apply(parse_date)
df["PorscheModelSanitized"] = df["porsche_model"].apply(parse_model)
df["ModelYearSanitized"] = df["model_year"].apply(parse_year)
df["SalesPriceSanitized"] = df["sale_price"].apply(parse_price)
df["VehicleMileageSanitized"] = df["vehicle_mileage"].apply(parse_mileage)
df["PayMethodSanitized"] = df["payment_method"].apply(parse_payment)
df["CitySanitized"] = df["city"].apply(parse_city)
df["StateSanitized"] = df["state"].apply(parse_state)
df["DeliveryStatusSanitized"] = df["delivery_status"].apply(parse_delivery)

# ---------------------------------------------------------------------------
# Reorder columns: sanitized column right after its source column
# ---------------------------------------------------------------------------
pairs = [
    ("sale_date", "SaleDateSanitized"),
    ("porsche_model", "PorscheModelSanitized"),
    ("model_year", "ModelYearSanitized"),
    ("sale_price", "SalesPriceSanitized"),
    ("vehicle_mileage", "VehicleMileageSanitized"),
    ("payment_method", "PayMethodSanitized"),
    ("city", "CitySanitized"),
    ("state", "StateSanitized"),
    ("delivery_status", "DeliveryStatusSanitized"),
]
sanitized_map = dict(pairs)
original_cols = ["sale_id","sale_date","customer_name","porsche_model","model_year",
                  "sale_price","vehicle_mileage","payment_method","city","state",
                  "salesperson","delivery_status"]

final_cols = []
for c in original_cols:
    final_cols.append(c)
    if c in sanitized_map:
        final_cols.append(sanitized_map[c])

df_final = df[final_cols]

df_final.to_excel(OUT, index=False, sheet_name="Sanitized")
print("Rows:", len(df_final))
print("Columns:", df_final.columns.tolist())
print("Wrote:", OUT)

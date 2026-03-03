#1 
money_pattern = r"\b\d[\d ]*,\d{2}\b"
#2
item_block = r"(?ms)^\s*(\d+)\.\s*\n(.*?)\n\s*([0-9]+,[0-9]{3})\s*x\s*([0-9 ]+,\d{2})\s*\n\s*([0-9 ]+,\d{2})\s*\n\s*Стоимость\s*\n\s*([0-9 ]+,\d{2})\s*$"
#3
total_pattern = r"^ИТОГО:\s*\n\s*([0-9 ]+,\d{2})\s*$"
#4
dt_pattern = r"^Время:\s*([0-9]{2}\.[0-9]{2}\.[0-9]{4}\s+[0-9]{2}:[0-9]{2}:[0-9]{2})\s*$"
#5
pay_pattern = r"^Банковская карта:\s*$"
#6
import re
import json
with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 1️⃣ Барлық бағаларды алу
prices = re.findall(r"\d[\d ]*,\d{2}", text)

# 2️⃣ Дата мен уақыт
dt_match = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})", text)
datetime_value = dt_match.group(1) if dt_match else None

# 3️⃣ Payment method
payment = "CARD" if "Банковская карта" in text else None

# 4️⃣ Total
total_match = re.search(r"ИТОГО:\s*\n\s*([\d ]+,\d{2})", text)
total_value = total_match.group(1) if total_match else None

# 5️⃣ Product names (жол басында номер бар жолдар)
product_names = re.findall(r"\d+\.\n(.+)", text)

# 6️⃣ JSON шығару
result = {
    "datetime": datetime_value,
    "payment_method": payment,
    "total": total_value,
    "product_names": product_names,
    "prices_found": prices
}

print(json.dumps(result, ensure_ascii=False, indent=2))

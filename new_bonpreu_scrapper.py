import requests
from bs4 import BeautifulSoup
import json
import re
from io import StringIO
import sys

def parse_float(text):
    text = text.replace(',', '.')
    match = re.search(r'([\d.]+)', text)
    return float(match.group(1)) if match else None

def scrape_food(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get product name
    name_tag = soup.find('h1', class_='_display_xy0eg_1')
    name = name_tag.get_text(strip=True) if name_tag else None

    # Get price per kg
    price_tag = soup.find('span', class_='_display_xy0eg_1')
    price = None
    if price_tag:
        price_text = price_tag.get_text()
        price = parse_float(price_text)

    # Get nutrition table
    table = soup.find('table')
    nutrition = {}
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2:
                key = cols[0].get_text(strip=True)
                val = cols[1].get_text(strip=True)
                nutrition[key] = val

    # Map Catalan keys to JSON fields
    # Handle both possible keys for saturated fats
    saturated_fats = (
        nutrition.get('de les quals saturats', '') or
        nutrition.get('dels quals saturats', '')
    )

    # Handle both possible keys for calories
    calories_key = 'Valor energètic' if 'Valor energètic' in nutrition else 'Valors energètics'
    calories_val = nutrition.get(calories_key, '')
    calories = parse_float(calories_val.split('/')[-1]) if calories_val else None

    result = {
        "name": name,
        "price_per_kg_in_eur": price,
        "calories_per_100g_in_kcal": calories,
        "carbs_per_100g_in_g": parse_float(nutrition.get('Hidrats de carboni', '')),
        "sugars_per_100g_in_g": parse_float(nutrition.get('dels quals sucres', '')),
        "fats_per_100g_in_g": parse_float(nutrition.get('Greixos', '')),
        "saturated_fats_per_100g_in_g": parse_float(saturated_fats),
        "dietay_fiber_per_100g_in_g": parse_float(nutrition.get('Fibra alimentària', '')),
        "protein_per_100g_in_g": parse_float(nutrition.get('Proteïnes', '')),
        "salt_per_100g_in_g": parse_float(nutrition.get('Sal', '')),
        "glycemic_index": -1,  # Not available on page, set manually or infer if possible
        "nova_category": -1    # Not available on page, set manually or infer if possible
    }

    print(json.dumps(result, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    results = []
    while True:
        url = input("Enter product URL (or leave empty to finish): ").strip()
        if not url:
            break
        try:
            # Capture printed JSON as dict

            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            scrape_food(url)
            sys.stdout = old_stdout

            data = json.loads(mystdout.getvalue())
            results.append(data)
        except Exception as e:
            print(f"Error processing {url}: {e}")

    if results:
        with open("scraped_products.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(results)} products to scraped_products.json")
    else:
        print("No products scraped.")
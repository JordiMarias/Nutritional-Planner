import requests
from bs4 import BeautifulSoup
import re
import json
import sys

def parse_nutrition_table(soup):
    # Find the table with nutritional info
    table = soup.find('table')
    if not table:
        return {}

    nutrition = {}
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) != 2:
            continue
        label = cols[0].get_text(strip=True).lower()
        value = cols[1].get_text(strip=True).replace(',', '.')
        # Extract numbers from value
        if 'greixos' in label and 'saturats' not in label:
            match = re.search(r'([\d.]+)\s*g', value)
            if match:
                nutrition['fats_per_100g_in_g'] = float(match.group(1))
        elif 'saturats' in label:
            match = re.search(r'([\d.]+)\s*g', value)
            if match:
                nutrition['saturated_fats_per_100g_in_g'] = float(match.group(1))
        elif 'hidrats de carboni' in label and 'sucres' not in label:
            match = re.search(r'([\d.]+)\s*g', value)
            if match:
                nutrition['carbs_per_100g_in_g'] = float(match.group(1))
        elif 'sucres' in label:
            match = re.search(r'([\d.]+)\s*g', value)
            if match:
                nutrition['sugars_per_100g_in_g'] = float(match.group(1))
        elif 'proteïnes' in label:
            match = re.search(r'([\d.]+)\s*g', value)
            if match:
                nutrition['protein_per_100g_in_g'] = float(match.group(1))
        elif 'fibra' in label:
            match = re.search(r'([\d.]+)\s*g', value)
            if match:
                nutrition['dietay_fiber_per_100g_in_g'] = float(match.group(1))
        elif 'sal' in label:
            match = re.search(r'([\d.]+)\s*g', value)
            if match:
                nutrition['salt_per_100g_in_g'] = float(match.group(1))
    return nutrition

def get_product_name(soup):
    h1 = soup.find('h1')
    if h1:
        return h1.get_text(strip=True)
    return "Unknown"

def main(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    name = get_product_name(soup)
    nutrition = parse_nutrition_table(soup)

    # Fill missing fields with 0
    fields = [
        'carbs_per_100g_in_g',
        'sugars_per_100g_in_g',
        'fats_per_100g_in_g',
        'saturated_fats_per_100g_in_g',
        'dietay_fiber_per_100g_in_g',
        'protein_per_100g_in_g',
        'salt_per_100g_in_g'
    ]
    for field in fields:
        if field not in nutrition:
            nutrition[field] = 0

    # Add static/dummy values for glycemic_index and nova_category
    nutrition['glycemic_index'] = -1
    nutrition['nova_category'] = -1

    result = {
        "name": name,
        **nutrition
    }

    print(json.dumps(result, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bonpreu_scrapper.py <product_url>")
        sys.exit(1)
    main(sys.argv[1])
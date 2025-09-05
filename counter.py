import json

def load_products(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def ask_grams_for_each(products):
    grams_eaten = []
    for product in products:
        while True:
            try:
                grams = float(input(f"How many grams of '{product['name']}' did you eat? (0 if none): "))
                if grams < 0:
                    print("Please enter a non-negative number.")
                    continue
                grams_eaten.append(grams)
                break
            except ValueError:
                print("Please enter a valid number.")
    return grams_eaten

def compute_totals(products, grams_eaten):
    totals = {
        "calories": 0,
        "carbs": 0,
        "sugars": 0,
        "fats": 0,
        "saturated_fats": 0,
        "dietay_fiber": 0,
        "protein": 0,
        "salt": 0
    }
    for product, grams in zip(products, grams_eaten):
        factor = grams / 100.0
        totals["calories"] += (product["calories_per_100g_in_kcal"] or 0) * factor
        totals["carbs"] += (product["carbs_per_100g_in_g"] or 0) * factor
        totals["sugars"] += (product["sugars_per_100g_in_g"] or 0) * factor
        totals["fats"] += (product["fats_per_100g_in_g"] or 0) * factor
        totals["saturated_fats"] += (product["saturated_fats_per_100g_in_g"] or 0) * factor
        totals["dietay_fiber"] += (product["dietay_fiber_per_100g_in_g"] or 0) * factor
        totals["protein"] += (product["protein_per_100g_in_g"] or 0) * factor
        totals["salt"] += (product["salt_per_100g_in_g"] or 0) * factor
    return totals

def print_totals(totals):
    print("\nTotal nutrients consumed:")
    print(f"Calories: {totals['calories']:.2f} kcal")
    print(f"Carbs: {totals['carbs']:.2f} g")
    print(f"Sugars: {totals['sugars']:.2f} g")
    print(f"Fats: {totals['fats']:.2f} g")
    print(f"Saturated fats: {totals['saturated_fats']:.2f} g")
    print(f"Dietary fiber: {totals['dietay_fiber']:.2f} g")
    print(f"Protein: {totals['protein']:.2f} g")
    print(f"Salt: {totals['salt']:.2f} g")

if __name__ == "__main__":
    products = load_products("scraped_products.json")
    grams_eaten = ask_grams_for_each(products)
    totals = compute_totals(products, grams_eaten)
    print_totals(totals)
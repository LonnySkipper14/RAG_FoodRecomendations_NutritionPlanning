import pandas as pd

def calculate_bmr(weight_kg, height_cm, age_years, gender):
    if gender == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age_years + 5
    elif gender == "female":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age_years - 161
    else:
        raise ValueError("Gender must be 'male' or 'female'.")

def calculate_daily_calories(weight, height, age, gender, activity_level, goal):
    bmr = calculate_bmr(weight, height, age, gender)
    activity_factors = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }
    factor = activity_factors.get(activity_level)
    if not factor:
        raise ValueError("Invalid activity level.")
    
    calories = bmr * factor

    if goal == "bulking":
        calories *= 1.2
    elif goal == "cutting":
        calories *= 0.8
    elif goal != "maintenance":
        raise ValueError("Goal must be 'maintenance', 'bulking', or 'cutting'.")
    
    return round(calories, 2)

def split_calories_by_mealtime(total_calories):
    return {
        "breakfast": round(total_calories * 0.25),
        "lunch": round(total_calories * 0.35),
        "dinner": round(total_calories * 0.30),
        "snack": round(total_calories * 0.10),
    }

def recommend_meals_json(json_path, calorie_target, tolerance=100, category=None):
    try:
        df = pd.read_json(json_path)
    except Exception as e:
        raise ValueError(f"Failed to read JSON: {e}")

    df.columns = df.columns.str.strip().str.lower()
    required_cols = ["name", "calories"]
    if category:
        required_cols.append("category")

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in the dataset.")

    if category:
        df = df[df["category"].str.lower() == category.lower()]

    recommended = df[abs(df["calories"] - calorie_target) <= tolerance]
    return recommended[["name", "calories"]].sort_values(by="calories")

def main():
    try:
        weight = float(input("Enter your weight (kg): "))
        height = float(input("Enter your height (cm): "))
        age = int(input("Enter your age (years): "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    print("\nSelect your gender:")
    print("1. Male")
    print("2. Female")
    gender_input = input("Enter number (1/2): ").strip()
    gender_map = {"1": "male", "2": "female"}
    gender = gender_map.get(gender_input)

    print("\nSelect your activity level:")
    print("1. Sedentary (little or no exercise)")
    print("2. Light (light exercise 1–3 days/week)")
    print("3. Moderate (moderate exercise 3–5 days/week)")
    print("4. Active (hard exercise 6–7 days/week)")
    print("5. Very Active (very hard exercise or physical job)")
    activity_input = input("Enter number (1–5): ").strip()
    activity_map = {
        "1": "sedentary",
        "2": "light",
        "3": "moderate",
        "4": "active",
        "5": "very_active"
    }
    activity_level = activity_map.get(activity_input)

    print("\nSelect your goal:")
    print("1. Maintenance")
    print("2. Bulking")
    print("3. Cutting")
    goal_input = input("Enter number (1/2/3): ").strip()
    goal_map = {"1": "maintenance", "2": "bulking", "3": "cutting"}
    goal = goal_map.get(goal_input)

    total_calories = calculate_daily_calories(weight, height, age, gender, activity_level, goal)
    print(f"\nYour daily calorie requirement ({goal}): {total_calories} kcal")

    calories_by_meal = split_calories_by_mealtime(total_calories)
    print("\nCalorie distribution per mealtime:")
    for meal, cal in calories_by_meal.items():
        print(f"- {meal.title()}: {cal} kcal")

    dataset_path = "dataset_ai_alibaba.json"
    tolerance = 150

    print("\nRecommended meals per mealtime:")
    for meal, target_cal in calories_by_meal.items():
        print(f"\n{meal.title()} (calorie target: {target_cal} kcal):")
        try:
            recommendations = recommend_meals_json(dataset_path, target_cal, tolerance, category="makanan")
            if recommendations.empty:
                print("  Sorry, no suitable food found.")
            else:
                print(recommendations.to_string(index=False))
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    main()

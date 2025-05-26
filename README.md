# 🥗 Nutrition Planning Tool

This Python script provides a simple and interactive way to help users calculate their daily caloric needs based on personal data and dietary goals. It then recommends meals based on those caloric needs from a JSON dataset.

## 🚀 Features

* Calculates **Basal Metabolic Rate (BMR)** using the Mifflin-St Jeor Equation.
* Determines daily calorie requirements based on:

  * Activity level (e.g., sedentary, moderate, active)
  * Dietary goal (maintenance, bulking, or cutting)
* Splits daily calories into recommended portions for:

  * Breakfast
  * Lunch
  * Dinner
  * Snack
* Recommends meals using a JSON dataset containing nutritional information.

## 🧠 How It Works

1. User inputs personal data: weight, height, age, gender, activity level, and dietary goal.
2. The script calculates the total daily calorie requirement.
3. The daily calories are split by meal time using standard distribution percentages.
4. Based on each mealtime’s calorie target, the script reads a JSON file (`dataset_ai_alibaba.json`) and suggests food items that fit the target within a defined tolerance.

## 🛠 Requirements

* Python 3.x
* `pandas` library

Install dependencies using:

```bash
pip install pandas
```

## 📁 Dataset

The script expects a JSON file named `dataset_ai_alibaba.json` with the following structure:

```json
[
  {
    "name": "Grilled Chicken",
    "calories": 350,
    "category": "makanan"
  },
  ...
]
```

**Required columns:**

* `name`
* `calories`
* Optional: `category` (e.g., `"makanan"`)

## ⚙️ Usage

Run the script using:

```bash
python NutritionPlanning.py
```

Follow the interactive prompts to enter:

1. Weight (kg)
2. Height (cm)
3. Age (years)
4. Gender
5. Activity level
6. Dietary goal

Meal recommendations will be displayed for each meal period based on the dataset.

## 📌 Notes

* If no suitable food is found within the specified calorie range, the script will notify the user.
* The default tolerance for matching calories is ±150 kcal.

## 👨‍⚕️ Disclaimer

This tool is for **informational purposes only** and not intended to replace professional dietary advice.

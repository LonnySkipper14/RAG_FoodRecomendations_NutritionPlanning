import pandas as pd
import os
import openai as OpenAI

def calculate_bmr(weight_kg, height_cm, age_years, gender="male"):
    if gender == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age_years + 5
    elif gender == "female":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age_years - 161
    else:
        raise ValueError("Gender harus 'male' atau 'female'")

def calculate_daily_calories(weight, height, age, gender="male", activity_level="moderate", goal="maintenance"):
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
        raise ValueError("Level aktivitas tidak valid.")
    calories = bmr * factor
    if goal == "bulking":
        calories *= 1.2
    elif goal == "cutting":
        calories *= 0.8
    elif goal != "maintenance":
        raise ValueError("Goal harus 'maintenance', 'bulking', atau 'cutting'")
    return round(calories, 2)

def split_calories_by_mealtime(total_calories):
    return {
        "sarapan": round(total_calories * 0.25),
        "makan_siang": round(total_calories * 0.35),
        "makan_malam": round(total_calories * 0.30),
        "camilan": round(total_calories * 0.10),
    }

def recommend_meals_json(json_path, calorie_target, tolerance=100, category=None):
    try:
        df = pd.read_json(json_path)
    except Exception as e:
        raise ValueError(f"Gagal membaca JSON: {e}")

    df.columns = df.columns.str.strip().str.lower()
    required_cols = ["name", "calories"]
    if category:
        required_cols.append("category")

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Kolom '{col}' tidak ditemukan di dataset.")

    if category:
        df = df[df["category"].str.lower() == category.lower()]

    recommended = df[abs(df["calories"] - calorie_target) <= tolerance]
    return recommended[["name", "calories"]].sort_values(by="calories")

# Inisialisasi client OpenAI dengan API key dari environment variable
client = OpenAI.OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

def ask_openai_with_dataset(prompt, dataset_recommendations=None):
    system_message = "You are a helpful assistant providing food recommendations based on the given dataset."
    
    dataset_text = ""
    if dataset_recommendations is not None and not dataset_recommendations.empty:
        dataset_text = "Here are some food options from the dataset:\n"
        for _, row in dataset_recommendations.iterrows():
            dataset_text += f"- {row['name']} ({row['calories']} kcal)\n"
    else:
        dataset_text = "No specific dataset recommendations available."

    full_prompt = f"{dataset_text}\nUser question: {prompt}"

    try:
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": full_prompt}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Terjadi kesalahan saat menghubungi OpenAI API: {e}"

def main():
    try:
        weight = float(input("Masukkan berat badan Anda (kg): "))
        height = float(input("Masukkan tinggi badan Anda (cm): "))
        age = int(input("Masukkan usia Anda: "))
    except ValueError:
        print("Input tidak valid, mohon masukkan angka yang benar.")
        return

    gender = input("Masukkan gender Anda (male/female): ").strip().lower()
    if gender not in ["male", "female"]:
        print("Gender harus 'male' atau 'female'.")
        return

    print("Pilih level aktivitas Anda:")
    print("sedentary (tidak aktif)")
    print("light (ringan)")
    print("moderate (sedang)")
    print("active (aktif)")
    print("very_active (sangat aktif)")
    activity = input("Masukkan level aktivitas: ").strip().lower()
    if activity not in ["sedentary", "light", "moderate", "active", "very_active"]:
        print("Level aktivitas tidak valid.")
        return

    print("Pilih tujuan Anda:")
    print("1. Maintenance (mempertahankan berat badan)")
    print("2. Bulking (menambah massa)")
    print("3. Cutting (mengurangi massa)")
    goal_input = input("Masukkan pilihan tujuan (1/2/3): ").strip()
    goal_map = {"1": "maintenance", "2": "bulking", "3": "cutting"}
    goal = goal_map.get(goal_input)
    if not goal:
        print("Pilihan tujuan tidak valid.")
        return

    total_calories = calculate_daily_calories(weight, height, age, gender, activity, goal)
    print(f"\nKebutuhan kalori harian Anda ({goal}): {total_calories} kcal")

    kalori_per_waktu = split_calories_by_mealtime(total_calories)
    print("Distribusi kalori per waktu makan:")
    for waktu, kalori in kalori_per_waktu.items():
        print(f"- {waktu.title()}: {kalori} kcal")

    # Path dataset JSON
    dataset_path = "dataset_ai_alibaba.json"
    tolerance = 150

    # Ambil rekomendasi makanan dari dataset berdasarkan total kalori harian
    rekomendasi_dataset = recommend_meals_json(dataset_path, total_calories, tolerance, category="makanan")
    
    # User bisa request pertanyaan/rekomendasi khusus ke OpenAI
    custom_prompt = input("\nMasukkan pertanyaan atau request rekomendasi ke OpenAI (atau tekan Enter untuk lewati): ").strip()
    
    if custom_prompt:
        jawaban_openai = ask_openai_with_dataset(custom_prompt, rekomendasi_dataset)
        print("\nJawaban dari OpenAI (berdasarkan dataset):")
        print(jawaban_openai)
    else:
        print("\nLewati OpenAI.")

    # Rekomendasi dari dataset per waktu makan
    print("\nRekomendasi menu per waktu makan dari dataset:")
    for waktu, kalori in kalori_per_waktu.items():
        print(f"\n{waktu.title()} (target kalori: {kalori} kcal):")
        try:
            rekomendasi = recommend_meals_json(dataset_path, kalori, tolerance, category="makanan")
            if rekomendasi.empty:
                print("  Maaf, tidak ada rekomendasi makanan yang sesuai.")
            else:
                print(rekomendasi.to_string(index=False))
        except Exception as e:
            print(f"  Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()

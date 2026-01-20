import joblib
import pandas as pd

# Зареждане на модела веднъж (глобално или в рамките на класа/сървиса)
try:
    model = joblib.load("role_model.joblib")
    print("✅ Моделът е зареден успешно.")
except FileNotFoundError:
    print("❌ Файлът role_model.joblib не е намерен. Първо стартирайте training скрипта.")
    exit()

def get_recommended_role(main_interest, lang, exp_level, city):
    """
    Приема данни за потребител и връща предсказана роля.
    """
    # Важно: Имената на колоните трябва да съвпадат точно с тези при обучението!
    input_data = pd.DataFrame([{
        "MainInterest": main_interest,
        "Lang": lang,
        "ExpLevel": exp_level,
        "City": city
    }])
    
    # Предсказание
    prediction = model.predict(input_data)
    
    # Може да вземете и вероятностите, за да видите колко е сигурен моделът
    # probabilities = model.predict_proba(input_data)
    
    return prediction[0]

# Тест
if __name__ == "__main__":
    role = get_recommended_role("Python", "Bulgarian", "Junior", "Sofia")
    print(f"Препоръчана роля: {role}")
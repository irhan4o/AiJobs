from db import get_connection
from repository import get_last_profiles
from repository import get_last_profiles, find_jobs_by_role_and_city

def ask_questions():
    print("Кратък въпросник за профил:")

    name = input("Име: ")
    main_interest = input("Какво ти е по-интересно (Web, Data, DevOps, Support)? ")
    lang = input("Кой език ти е най-силен (Python, C#, JavaScript и т.н.)? ")
    exp = input("Ниво (начинаещ, среден, напреднал): ")
    city = input("Град (или remote): ")

    profile = {
        "name": name,
        "main_interest": main_interest.lower(),
        "lang": lang.lower(),
        "exp": exp.lower(),
        "city": city.lower()
    }
    return profile

def recommend_role(profile):
    interest = profile["main_interest"].lower()
    lang = profile["lang"].lower()
    level = profile["exp"].lower()   # или какъвто е реалният ключ


    scores = {
        "Junior Data Analyst / Python": 0,
        "Junior Web Developer (JavaScript)": 0,
        "Junior Software Developer": 0,
    }

    # интерес
    if "data" in interest or "анализ" in interest:
        scores["Junior Data Analyst / Python"] += 3
    if "web" in interest:
        scores["Junior Web Developer (JavaScript)"] += 3
    if "devops" in interest or "backend" in interest or "software" in interest:
        scores["Junior Software Developer"] += 3

    # език
    if "python" in lang:
        scores["Junior Data Analyst / Python"] += 2
        scores["Junior Software Developer"] += 1
    if "js" in lang or "javascript" in lang:
        scores["Junior Web Developer (JavaScript)"] += 2
    if "c#" in lang or "csharp" in lang:
        scores["Junior Software Developer"] += 2

    # ниво
    if "начинаещ" in level:
        scores["Junior Data Analyst / Python"] += 1
        scores["Junior Web Developer (JavaScript)"] += 1
        scores["Junior Software Developer"] += 1
    elif "среден" in level:
        scores["Junior Software Developer"] += 1
    elif "напреднал" in level:
        scores["Junior Software Developer"] += 2

    # показване на скоровете
    print("\nТочки по роли:")
    for role_name, score in scores.items():
        print(f"- {role_name}: {score}")

    # избор на най-висок скор
    best_role = max(scores, key=scores.get)
    if scores[best_role] == 0:
        best_role = "Junior Software Developer"

    return best_role


def save_profile_to_db(profile):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO UserProfiles (Name, MainInterest, Lang, ExpLevel, City)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(
        query,
        profile["name"],
        profile["main_interest"],
        profile["lang"],
        profile["exp"],
        profile["city"],
    )

    conn.commit()
    conn.close()


def main():
    profile = ask_questions()
    

    role = recommend_role(profile)
    print(f"\nПодходяща стартова позиция за теб: {role}")

    save_profile_to_db(profile)

    print("\nПодходящи обяви за тази роля:")
    jobs = find_jobs_by_role_and_city(role, profile["city"])
    if not jobs:
        print("Няма намерени обяви в момента.")
    else:
        for title, company, city, link in jobs:
            print(f"- {title} @ {company} ({city}) -> {link}")

if __name__ == "__main__":
    main()

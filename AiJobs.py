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
    interest = profile["main_interest"]
    lang = profile["lang"]

    if "data" in interest or "анализ" in interest:
        return "Junior Data Analyst / Python"
    if "web" in interest and ("js" in lang or "javascript" in lang):
        return "Junior Web Developer (JavaScript)"
    return "Junior Software Developer"

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

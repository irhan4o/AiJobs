from db import get_connection
from repository import get_last_profiles, find_jobs_by_role_and_city
import joblib
import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from googlesearch import search

console = Console()

def ask_questions():
    console.print("\n[bold magenta]📋 Кратък въпросник за профил:[/bold magenta]")
    name = console.input("👤 Име: ")
    main_interest = console.input("💡 Какво ти е по-интересно (Web, Data, DevOps)? ")
    lang = console.input("💻 Кой език ти е най-силен (Python, JS, C#)? ")
    exp = console.input("📊 Ниво (начинаещ, среден, напреднал): ")
    city = console.input("🏙 Град (или remote): ")
    
    return {
        "name": name,
        "main_interest": main_interest.lower(),
        "lang": lang.lower(),
        "exp": exp.lower(),
        "city": city.lower()
    }

def recommend_role(profile):
    try:
        model = joblib.load("role_model.joblib")
        console.print("✅ [green]Използвам ML модел за препоръка[/green]")
        
        input_df = pd.DataFrame([[
            profile["main_interest"],
            profile["lang"],
            profile["exp"],
            profile["city"]
        ]], columns=["MainInterest", "Lang", "ExpLevel", "City"])
        
        prediction = model.predict(input_df)[0]
        console.print(f"🤖 [bold green]ML моделът предсказва: {prediction}[/bold green]")
        return prediction
        
    except:
        console.print("⚠️  [yellow]Ползвам ръчна точкова система[/yellow]")
        return recommend_role_rules(profile)

def recommend_role_rules(profile):
    interest = profile["main_interest"]
    lang = profile["lang"]
    level = profile["exp"]

    scores = {
        "Junior Data Analyst / Python": 0,
        "Junior Web Developer (JavaScript)": 0,
        "Junior Software Developer": 0,
    }

    if "data" in interest or "анализ" in interest:
        scores["Junior Data Analyst / Python"] += 3
    if "web" in interest:
        scores["Junior Web Developer (JavaScript)"] += 3
    if any(x in interest for x in ["devops", "backend", "software"]):
        scores["Junior Software Developer"] += 3

    if "python" in lang:
        scores["Junior Data Analyst / Python"] += 2
        scores["Junior Software Developer"] += 1
    if any(x in lang for x in ["js", "javascript"]):
        scores["Junior Web Developer (JavaScript)"] += 2
    if any(x in lang for x in ["c#", "csharp"]):
        scores["Junior Software Developer"] += 2

    if "начинаещ" in level:
        for role in scores: scores[role] += 1
    elif "среден" in level or "напреднал" in level:
        scores["Junior Software Developer"] += 2

    console.print("\n📊 [bold]Точки по роли:[/bold]")
    for role, score in scores.items():
        console.print(f"  - {role}: {score}")

    best_role = max(scores, key=scores.get)
    if scores[best_role] == 0:
        best_role = "Junior Software Developer"
    return best_role

def save_profile_to_db(profile, role):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO UserProfiles (Name, MainInterest, Lang, ExpLevel, City, RecommendedRole)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, profile["name"], profile["main_interest"], 
                  profile["lang"], profile["exp"], profile["city"], role)
    conn.commit()
    conn.close()
    console.print("💾 [green]Профилът е запазен![/green]")

def search_real_jobs(role, city):
    # Почисти ролята за търсене
    clean_role = role.replace("/", "").replace("(", "").replace(")", "").lower()
    
    # По-добри ключови думи за България
    queries = [
        f'{clean_role} {city} jobs.bg',
        f'{clean_role} {city} "софия" jobs',
        f'{clean_role} {city} "работа"',
        f'{clean_role} вакансия {city}',
    ]
    
    console.print(f"🔍 [blue]Търся {clean_role} в {city}...[/blue]")
    
    all_jobs = []
    for query in queries[:2]:  # пробвай 2 query-то
        try:
            for url in search(query, num_results=3, lang="bg"):
                if any(site in url.lower() for site in ["jobs.bg", "topcv.bg", "linkedin.com", "zapo.bg"]):
                    domain = url.split('/')[2].replace('www.', '')
                    title = f"{clean_role.title()} на {domain}"
                    all_jobs.append((title[:50], "🌐 Онлайн", city, url))
                    if len(all_jobs) >= 4: 
                        break
            if len(all_jobs) >= 4: break
        except:
            continue
    
    return all_jobs[:5]  # max 5 обяви

def main():
    console.print(Panel("🤖 AI Career Advisor v2.0", style="bold cyan"))
    
    profile = ask_questions()
    console.print("\n[bold yellow]🎯 Анализирам...[/bold yellow]")
    
    role = recommend_role(profile)
    console.print(f"\n[bold green]🚀 Препоръка: {role}[/bold green]")
    
    save_profile_to_db(profile, role)
    
    local_jobs = find_jobs_by_role_and_city(role, profile["city"])
    web_jobs = search_real_jobs(role, profile["city"])
    
    all_jobs = local_jobs + web_jobs
    
    if not all_jobs:
        console.print("[red]❌ Няма намерени обяви[/red]")
    else:
        table = Table(title=f"🎯 {len(all_jobs)} обяви", box=None)
        table.add_column("Източник", style="cyan", no_wrap=True)
        table.add_column("Позиция", style="magenta")
        table.add_column("Град", style="green")
        table.add_column("Линк", style="blue underline")
        
        for title, source, city, link in all_jobs:
            table.add_row(source, title, city, link)
        
        console.print(table)

if __name__ == "__main__":
    main()

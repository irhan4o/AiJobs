from db import get_connection

def get_last_profiles(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT TOP (?) Id, Name, MainInterest, Lang, ExpLevel, City, CreatedAt
        FROM UserProfiles
        ORDER BY Id DESC
    """
    cursor.execute(query, limit)
    rows = cursor.fetchall()
    conn.close()
    return rows

def find_jobs_by_role_and_city(role_tag: str, city: str, limit: int = 5):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT TOP (?) Title, Company, City, Link
        FROM Jobs
        WHERE RoleTag = ? AND (City = ? OR ? = 'remote')
        ORDER BY CreatedAt DESC
    """
    cursor.execute(query, limit, role_tag, city, city)
    rows = cursor.fetchall()
    conn.close()
    return rows

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

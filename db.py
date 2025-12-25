import pyodbc

def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-6CGBDLC;"    # точно както е в SSMS
        "DATABASE=CareerMatcher;"    # или името на твоята база
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

if __name__ == "__main__":
    conn = get_connection()
    print("Connection OK")
    conn.close()

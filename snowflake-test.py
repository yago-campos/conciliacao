import snowflake.connector

try:
    conn = snowflake.connector.connect(
        user='BARATONA',
        password='y4T#8pLz@3QmW$9K',
        account='lia24005.us-east-1',
        warehouse='WH_BARATONA',
        database='BARATONA',
        schema='TRANSIENT'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT();")
    print(cursor.fetchall())
    print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro na conexão: {e}")
import snowflake.connector

try:
    conn = snowflake.connector.connect(
        user='',
        password='',
        account='',
        warehouse='',
        database='',
        schema=''
    )
    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT();")
    print(cursor.fetchall())
    print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro na conexão: {e}")
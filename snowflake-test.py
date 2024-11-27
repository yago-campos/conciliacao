import snowflake.connector

try:
    conn = snowflake.connector.connect(
        user='yagocampos',
        password='R4tF1sh3r$Snowflake',
        account='xzqggdu-fua20629',
        warehouse='DEV',
        database='DEV_DB',
        schema='PUBLIC'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT();")
    print(cursor.fetchall())
    print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro na conexão: {e}")
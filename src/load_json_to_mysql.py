import json
import os
from db_config import get_connection


def load_json_to_mysql(json_path):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    with open(json_path, "r") as f:
        jdata = json.load(f)

    cols = jdata["cols"]
    data = jdata["data"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS json_to_sql_table")

    create_sql = f"""
    CREATE TABLE json_to_sql_table (
        id INT PRIMARY KEY AUTO_INCREMENT,
        {", ".join([f"`{c}` TEXT" for c in cols])}
    )
    """

    cursor.execute(create_sql)

    insert_sql = f"INSERT INTO json_to_sql_table ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))})"

    cursor.executemany(insert_sql, data)
    conn.commit()
    conn.close()

    print("JSON data successfully loaded into MySQL.")

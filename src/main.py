print(">>> MAIN.PY IS RUNNING")
import os

from load_json_to_mysql import load_json_to_mysql
from transform_data import (
    read_from_mysql,
    clean_email,
    clean_postal_zip,
    encode_phone
)

JSON_PATH = "data/sample_data_for_assignment.json"

def main():
    load_json_to_mysql(JSON_PATH)

    df = read_from_mysql()
    df = clean_email(df)
    df = clean_postal_zip(df)
    df = encode_phone(df)

    print("\nFinal Clean DataFrame:\n")
    print(df)

if __name__ == "__main__":
    main()

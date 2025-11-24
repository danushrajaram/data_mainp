import pandas as pd
from db_config import get_connection
import re

def read_from_mysql():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM json_to_sql_table", conn)
    conn.close()
    return df

def clean_email(df):
    df["email"] = df["email"].apply(lambda x: x.split("@")[0] + "@gmail.com")
    return df

def clean_postal_zip(df):
    def to_int(val):
        cleaned = re.sub(r"\D", "", str(val))
        return int(cleaned) if cleaned else 0
    df["postalZip"] = df["postalZip"].apply(to_int)
    return df

def encode_phone(df):
    def encode(p):
        digits = re.sub(r"\D", "", p)
        result = []
        for i in range(0, len(digits) - 1, 2):
            pair = int(digits[i:i+2])
            if pair < 65:
                result.append("O")
            else:
                result.append(chr(pair))
        return "".join(result)

    df["coded_phone_number"] = df["phone"].apply(encode)
    df.drop(columns=["phone"], inplace=True)
    return df

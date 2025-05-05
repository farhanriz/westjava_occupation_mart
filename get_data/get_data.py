# import libraries
import requests
import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv(dotenv_path=Path(Path(__file__).resolve().parent.parent / "cred.env"))

# db configuration
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

# API and output DB configuration
API_URL = "https://data.jabarprov.go.id/api-backend/bigdata/disdukcapil_2/od_15922_jml_penduduk__kelompok_pekerjaan_jk_v2?limit=500"
SCHEMA_NAME = "dbt"
TABLE_NAME = "westjava_occupation"

# Fetch data from API
def fetch_data(url):
    print("Fetching data from API")
    response = requests.get(url)
    response.raise_for_status()  # raises an error for bad status codes
    print("Data fetched successfully")
    json_data = response.json()
    return json_data.get('data') or json_data.get('result')

# Create schema and table 
def create_table(cursor, schema, table):
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {schema}.{table} (
            id SERIAL PRIMARY KEY,
            province_name TEXT,
            occupation_group TEXT,
            gender TEXT,
            value INTEGER,
            unit TEXT,
            year INTEGER,
            updated_at TIMESTAMPTZ DEFAULT (NOW() AT TIME ZONE 'UTC'),
            UNIQUE (province_name, occupation_group, gender, year)
        )
    """)

# Insert or update data
def insert_data(cursor, schema, table, data):
    sql = f"""
        INSERT INTO {schema}.{table} 
        (province_name, occupation_group, gender, value, unit, year)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (province_name, occupation_group, gender, year)
        DO UPDATE SET updated_at = (NOW() AT TIME ZONE 'Asia/Jakarta')
    """
    for item in data:
        cursor.execute(sql, (
            item.get('nama_provinsi'),
            item.get('kelompok_pekerjaan'),
            item.get('jenis_kelamin'),
            item.get('jumlah_penduduk'),
            item.get('satuan'),
            item.get('tahun')
        ))

def main():
    try:
        data = fetch_data(API_URL)
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                create_table(cursor, SCHEMA_NAME, TABLE_NAME)
                insert_data(cursor, SCHEMA_NAME, TABLE_NAME, data)
        print("Data inserted")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        dbname="kpr_vs_ngontrak",
        user="postgres",              # ganti sesuai user kamu
        password="your_password",     # ganti password kamu
        host="localhost",
        port="5432"
    )

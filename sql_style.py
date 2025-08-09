# sql_style.py
import duckdb
import pandas as pd

def execute_sql_on_data(df: pd.DataFrame, sql_query: str):
    """
    Пример SQL-запроса:
    SELECT category, SUM(sales) as total_sales
    FROM df 
    WHERE date > '2023-01-01'
    GROUP BY category
    """
    return duckdb.query(sql_query).df()
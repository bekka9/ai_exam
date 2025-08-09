# data_processing.py
import pandas as pd
import polars as pl
import duckdb

def process_data(file_path: str, file_type: str = 'parquet'):
    # Чтение данных
    if file_type == 'parquet':
        df_pd = pd.read_parquet(file_path)
        df_pl = pl.read_parquet(file_path)
    else:  # CSV
        df_pd = pd.read_csv(file_path)
        df_pl = pl.read_csv(file_path)
    
    # Анализ данных (пример)
    analysis = duckdb.sql(f"""
        SELECT 
            category, 
            AVG(price) AS avg_price,
            COUNT(*) AS count
        FROM df_pd
        GROUP BY category
        ORDER BY avg_price DESC
    """).df()
    
    # Фильтрация и преобразования
    filtered = df_pl.filter(
        pl.col('date').is_between('2023-01-01', '2023-12-31')
    ).with_columns(
        (pl.col('price') * 1.2).alias('price_with_tax')
    )
    
    return analysis, filtered.to_pandas()
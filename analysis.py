# analysis.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

def analyze_data(df: pd.DataFrame):
    # Базовые статистики
    stats = df.describe(percentiles=[0.25, 0.5, 0.75, 0.99])
    
    # Поиск аномалий (пример)
    z_scores = stats.zscore(df['value'])
    anomalies = df[(z_scores > 3) | (z_scores < -3)]
    
    # Визуализация
    plt.figure(figsize=(12, 6))
    sns.boxplot(x=df['category'], y=df['value'])
    plt.xticks(rotation=45)
    plt.savefig('boxplot.png', bbox_inches='tight')
    
    return stats, anomalies
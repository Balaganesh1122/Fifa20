import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def get_player_clusters(df):
    skill_cols = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
    data = df[skill_cols].dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data)

    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)

    data = data.copy()
    data['cluster'] = clusters

    return data, kmeans

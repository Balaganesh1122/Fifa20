import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances

def find_similar_players(df, player_name, top_n=5):
    skill_cols = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']

    df_clean = df.dropna(subset=skill_cols).reset_index(drop=True)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean[skill_cols])

    if player_name not in df_clean['short_name'].values:
        return []

    idx = df_clean[df_clean['short_name'] == player_name].index[0]

    distances = euclidean_distances(
        [X_scaled[idx]],
        X_scaled
    )[0]

    df_clean['distance'] = distances
    similar = df_clean.sort_values('distance').iloc[1:top_n+1]

    return similar[['short_name', 'overall', 'age', 'club']]

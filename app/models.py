import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from fuzzywuzzy import process
import os

def recommend(anime_name, start=0, end=20):
    if anime_name == "":
        return []
    
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'anime.csv'))
    df_copy = df.copy()

    df['genre'] = df['genre'].str.replace('"', '').str.replace("'", '').str.strip().fillna('')
    df['type'] = df['type'].fillna('')
    df['rating'] = df['rating'].fillna(0)
    df['members'] = df['members'].fillna(0)
    df['episodes'] = df['episodes'].replace('Unknown', 0)  # Replace 'Unknown' with 0
    df['episodes'] = pd.to_numeric(df['episodes'], errors='coerce').fillna(0)

    vectorizer = CountVectorizer(tokenizer=lambda x: x.split(', '))
    genre_matrix = vectorizer.fit_transform(df['genre'])

    scaler = MinMaxScaler()
    df[['rating', 'members', 'episodes']] = scaler.fit_transform(df[['rating', 'members', 'episodes']])

    combined_features = pd.concat([pd.DataFrame(genre_matrix.toarray()), df[['rating', 'members', 'episodes']]], axis=1)
    cosine_sim = cosine_similarity(combined_features)

    def get_recommendations(anime_name, cosine_sim=cosine_sim, df=df):
        match = process.extractOne(anime_name, df['name'])
        if match[1] < 80:
            return []

        anime_name = match[0]
        idx = df[df['name'] == anime_name].index[0]

        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_anime_indices = [i[0] for i in sim_scores[start:end+1]]

        recommended_anime = []
        for anime_idx in sim_anime_indices:
            anime_info = {
                'anime_id': df_copy.iloc[anime_idx]['anime_id'],
                'name': df_copy.iloc[anime_idx]['name'],
                'genre': df_copy.iloc[anime_idx]['genre'],
                'rating': df_copy.iloc[anime_idx]['rating'],
                'episodes': df_copy.iloc[anime_idx]['episodes'],
                'type': df_copy.iloc[anime_idx]['type'],
            }

            recommended_anime.append(anime_info)

        return recommended_anime

    recommended_anime = get_recommendations(anime_name)
    return recommended_anime


if __name__ == '__main__':
    print(recommend('Naruto'))

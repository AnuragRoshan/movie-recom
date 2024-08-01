import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    return "https://via.placeholder.com/500x750?text=No+Poster"

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        return [], []  # Movie not found

    # Retrieve nearest neighbors from the similarity_data
    top_indices = similarity_data['neighbors'][index]
    top_movies = movies.iloc[top_indices]
    
    recommended_movie_names = top_movies['title'].tolist()
    recommended_movie_posters = [fetch_poster(movie_id) for movie_id in top_movies['movie_id']]

    return recommended_movie_names, recommended_movie_posters

# Streamlit App
st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity_data = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        if i < len(recommended_movie_names):
            with col:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])

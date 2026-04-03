import streamlit as st
import pickle
import requests

API_KEY = "77f1c91a0b22ff6d7c9f57b017f5c775"

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

@st.cache_data
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()

        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        return None
    except:
        return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:10]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)

        if poster:
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(poster)

        if len(recommended_movies) == 5:
            break

    return recommended_movies, recommended_posters


st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommender System")

movie_titles = movies['title'].values
selected_movie = st.selectbox("Select a movie", movie_titles)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(len(names)):
        with cols[i]:
            search_url = f"https://www.google.com/search?q={names[i].replace(' ', '+')}"

            st.markdown(
                f"""
                <div style="text-align:center">
                    <a href="{search_url}" target="_blank">
                        <img src="{posters[i]}" width="200" style="border-radius:10px;">
                    </a>
                    <p>{names[i]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
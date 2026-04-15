import pickle
import streamlit as st
import requests

# ---------------- FETCH POSTER ---------------- #
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US"

        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raises error if bad response

        data = response.json()

        # Handle missing poster
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"

    except Exception as e:
        print("Error:", e)
        return "https://via.placeholder.com/300x450?text=Error"


# ---------------- RECOMMEND FUNCTION ---------------- #
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


# ---------------- STREAMLIT UI ---------------- #
st.header('🎬 Movie Recommender System')

# Load data
import gdown
import os

if not os.path.exists("movie_list.pkl"):
    gdown.download("https://drive.google.com/uc?id=1WccG_XWJc6uwIuxdZokl8sIh4kolPNdm", "movie_list.pkl", quiet=False)

if not os.path.exists("similarity.pkl"):
    gdown.download("https://drive.google.com/uc?id=1lPmUl5K7lfZ6q9vdjdJzWsp27DjL3wd2", "similarity.pkl", quiet=False)

movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

st.write(movies.head())
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Select a movie from dropdown",
    movie_list
)

# Button
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    cols = [col1, col2, col3, col4, col5]

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])






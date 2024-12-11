import streamlit as st
import requests
import pickle
from googleapiclient.discovery import build
from streamlit_option_menu import option_menu

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# YouTube API key
API_KEY = '{Your_Youtube_API}'

def fetch_poster(movie_title):
    """Fetch movie poster URL using OMDb API."""
    url = f"http://www.omdbapi.com/?t={movie_title}&{OMDb API_KEY}"
    response = requests.get(url).json()
    poster_url = response.get("Poster", "https://via.placeholder.com/300x450?text=No+Image")
    return poster_url

def details(movie_title):
    """Fetch movie details using OMDb API."""
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey=7c04a58c"
    response = requests.get(url).json()
    data_details = {
        "date": response.get("Released", "Unknown"),
        "revenue": response.get("BoxOffice", "Unknown"),
        "runtime": response.get("Runtime", "Unknown"),
    }
    return data_details

def recommend(movie):
    """Recommend movies based on similarity."""
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    movie_details = []

    for i in distances[1:11]:  # Adjusted to show 10 recommendations (instead of 5)
        movie_title = movies.iloc[i[0]].title
        recommended_movie_posters.append(fetch_poster(movie_title))
        movie_details.append(details(movie_title))
        recommended_movie_names.append(movie_title)

    return recommended_movie_names, recommended_movie_posters, movie_details

def get_trailer(movie_name):
    """Return the YouTube video ID for trailers."""
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    search_response = youtube.search().list(
        q=f"{movie_name} trailer", part='id,snippet', maxResults=1
    ).execute()
    video_id = search_response['items'][0]['id']['videoId']
    return f'https://www.youtube.com/watch?v={video_id}'

# Streamlit app configuration
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Welcome", "Recommendations"],
        icons=["house", "film", "envelope"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Welcome":
    st.markdown(
        """
        <style>
        .welcome-container {
            text-align: center;
            padding: 50px;
            background: url("https://img.freepik.com/premium-photo/winter-landscape-with-snowy-landscape-sunset_363412-676.jpg?ga=GA1.1.1264330772.1733318452&semt=ais_hybrid");
            background-size: cover;
            color: white;
        }
        .welcome-title {
            font-size: 48px;
            margin-bottom: 20px;
        }
        .welcome-text {
            font-size: 24px;
            margin-bottom: 20px;
        }
        .carousel {
            display: flex;
            overflow-x: auto;
            scroll-behavior: smooth;
        }
        .carousel img {
            width: 300px;
            height: 450px;
            margin: 10px;
            border-radius: 10px;
        }
        </style>
        <div class="welcome-container">
            <div class="welcome-title">🎬 Welcome to the Movie Recommendation System! 🎬</div>
            <div class="welcome-text">
                Discover Your Next Favorite Movie<br>
                Our recommendation system helps you find movies you'll love.<br>
                Just select a movie you like, and we'll suggest similar movies for you to enjoy.<br>
                You can also watch trailers directly from our app!
            </div>
        </div>
        """, unsafe_allow_html=True
    )

elif selected == "Recommendations":
    st.title("Movie Recommendations")
    movie_list = movies['title'].values
    selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

    # If recommendations have already been calculated, use session state
    if 'recommended_movie_names' not in st.session_state:
        st.session_state.recommended_movie_names = []
        st.session_state.recommended_movie_posters = []
        st.session_state.movie_details = []

    if st.button('Show Recommendation'):
        with st.spinner('Loading...'):
            recommended_movie_names, recommended_movie_posters, movie_details = recommend(selected_movie)

            # Save recommendations to session state
            st.session_state.recommended_movie_names = recommended_movie_names
            st.session_state.recommended_movie_posters = recommended_movie_posters
            st.session_state.movie_details = movie_details

    # Display recommendations from session state
    if st.session_state.recommended_movie_names:
        with st.expander("Recommended Movies", expanded=True):
            cols = st.columns(5)  # Create 5 columns
            for i in range(10):  # Loop for 10 recommendations
                col = cols[i % 5]  # Loop through the columns
                col.text(st.session_state.recommended_movie_names[i])
                col.image(st.session_state.recommended_movie_posters[i])
                movie_data = st.session_state.movie_details[i]
                col.write(f"Release date: {movie_data['date']}")
                col.write(f"Revenue: {movie_data['revenue']}")
                col.write(f"Runtime: {movie_data['runtime']}")

    movie_name = st.text_input('Enter the name of the movie:')
    if st.button('Search Trailer'):
        trailer_url = get_trailer(movie_name)
        st.video(trailer_url)  # Embed the trailer video


import streamlit as st
import pickle
import numpy as np

import requests



st.title('Movie Recommendation System')



movies_df = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))




def get_data(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=52dfe5cf697d26c8fbf39eb01f85b7aa&language=en-US'.format(movie_id)
    response = requests.get(url)
    data = response.json()
    # st.text(data)
    # st.text(url)

    return data



def fetch_poster(movie_id):
    data = get_data(movie_id)

    poster = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return poster




def fetch_tagline(movie_id):
    data = get_data(movie_id)

    tagline = data['tagline']
    return tagline




def fetch_overview(movie_id):
    data = get_data(movie_id)

    overview = data['overview']
    return overview




def fetch_popularity(movie_id):
    data = get_data(movie_id)

    popularity = data['popularity']
    return popularity




def fetch_release_date(movie_id):
    data = get_data(movie_id)

    release_date = data['release_date']
    return release_date




def fetch_runtime(movie_id):
    data = get_data(movie_id)

    runtime = data['runtime']
    return runtime




def fetch_vote_average(movie_id):
    data = get_data(movie_id)

    vote_average = data['vote_average']
    return vote_average




def fetch_vote_count(movie_id):
    data = get_data(movie_id)

    vote_count = data['vote_count']
    return vote_count




def fetch_genres(movie_id):
    data = get_data(movie_id)

    genres = (data['genres'])

    # st.write(genres)

    movie_genres = list()
    for i in genres:
        # st.write(i)
        for k,v in i.items():
            # st.write(v)
            if k == 'name':
                movie_genres.append(v)
                # st.write(v)

    return movie_genres




def fetch_trailer(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/videos?api_key=52dfe5cf697d26c8fbf39eb01f85b7aa&language=en-US".format(movie_id)
    response = requests.get(url)
    st.write(type(response))




def recommend(movie_id):
    movie_index = movies_df[movies_df['english_title'] == movie_id].index
    distances = similarity[ movie_index ]

    temp = sorted(list(enumerate(distances[0])),
                  reverse = True,
                  key = lambda x : x[1]
                 )[1:6]

    row_index_movie = [i[0] for i in temp]
    
    rec_movies_id = movies_df.loc[row_index_movie, 'movie_id'].to_list()
    
    rec_movies = movies_df.loc[row_index_movie, 'english_title'].to_list()

    rec_movies_posters  = [fetch_poster(i) for i in rec_movies_id]

    rec_movies_tagline = [fetch_tagline(i) for i in rec_movies_id]

    rec_movies_overview = [fetch_overview(i) for i in rec_movies_id]
    
    rec_movies_popularity = [fetch_popularity(i) for i in rec_movies_id]

    rec_movies_release_date = [fetch_release_date(i) for i in rec_movies_id]

    rec_movies_runtime = [fetch_runtime(i) for i in rec_movies_id]

    rec_movies_vote_average = [fetch_vote_average(i) for i in rec_movies_id]

    rec_movies_vote_count = [fetch_vote_count(i) for i in rec_movies_id]

    rec_movies_fetch_genres = [fetch_genres(i) for i in rec_movies_id]

    return rec_movies_id, rec_movies, rec_movies_posters, rec_movies_tagline, rec_movies_overview, rec_movies_popularity, rec_movies_release_date, rec_movies_runtime, rec_movies_vote_average, rec_movies_vote_count, rec_movies_fetch_genres




selected_movie = st.selectbox(
    'Which Movie Would You Like To Watch?',
    movies_df['english_title'].values
    )




if st.button('Recommend'):
    rec_m_id, rec_m, rec_m_posters, rec_m_tagline, rec_m_overview, rec_m_popularity, rec_m_release_date, rec_m_runtime, rec_m_vote_average, rec_movies_vote_count, rec_m_fetch_genres = recommend(selected_movie)

    for i in range(len(rec_m)):

        st.header(rec_m[i])
        st.image(rec_m_posters[i])

        st.markdown('Tagline : ')
        st.subheader(rec_m_tagline[i])

        st.markdown('Overview : ')
        st.write(rec_m_overview[i])

        # st.markdown('Release Date : ')
        # st.text(rec_m_release_date[i])

        # st.markdown('Runtime : ')
        # st.text(rec_m_runtime[i])

        # st.markdown('Popularity : ')
        # st.text(rec_m_popularity[i])

        # st.markdown('Vote Average : ')
        # st.text(rec_m_vote_average[i])

        # st.markdown('Vote Count : ')
        # st.text(rec_movies_vote_count[i])

        col1, col2 = st.columns(2)
        col1.metric(label = 'Release Date', value = rec_m_release_date[i])
        col2.metric(label = 'Runtime', value = rec_m_runtime[i])

        col1, col2, col3 = st.columns(3)
        col1.metric(label = 'Popularity', value = rec_m_popularity[i])
        col2.metric(label = 'Vote Average', value = rec_m_vote_average[i])
        col3.metric(label = 'Vote Count', value = rec_movies_vote_count[i])

        # st.write(rec_m_fetch_genres[i])
        st.markdown('Genres : ')
        # genres = list()
        for j in rec_m_fetch_genres[i]:
            # genres.append(j)
            st.write(j)
        # st.markdown(genres)


        st.text("")
        st.text("")
        st.text("")
        st.text("")

        # fetch_trailer(i)
import streamlit as st
import requests
import pandas as pd

st.title("Music Streaming Database Web Application")

# Flask backend URL
FLASK_URL = "https://music-streaming-flask-backend.onrender.com/query"

# Sidebar for table schema
with st.sidebar:
    st.header("Database Schema")
    
    # Collapsible sections for each table
    with st.expander("albums", expanded=False):
        st.write("""
        - **album_id**: character varying(255), not null (Primary Key)
        - **name**: character varying(350), not null
        - **album_type**: character varying(50), not null, default 'album'
        - **release_date**: date
        - **total_tracks**: integer, not null, default 0
        - **popularity**: integer, not null, default 0
        - **label**: character varying(150), not null, default 'Unknown'
        """)
    
    with st.expander("tracks", expanded=False):
        st.write("""
        - **track_id**: character varying(255), not null (Primary Key)
        - **name**: character varying(350), not null
        - **album_id**: character varying(255), not null (Foreign Key to albums(album_id))
        - **track_number**: integer, not null
        - **duration_ms**: integer, not null, default 0
        - **popularity**: integer, not null, default 0
        - **explicit**: boolean, not null, default false
        - **disc_number**: integer, not null, default 1
        """)
    
    with st.expander("artists", expanded=False):
        st.write("""
        - **artist_id**: character varying(255), not null (Primary Key)
        - **name**: character varying(200), not null
        - **popularity**: integer, not null, default 0
        - **followers**: integer, not null, default 0
        """)
    
    with st.expander("genres", expanded=False):
        st.write("""
        - **genre_id**: integer, not null (Primary Key)
        - **name**: character varying(50), not null (Unique)
        """)
    
    with st.expander("artist_genres", expanded=False):
        st.write("""
        - **artist_id**: character varying(255), not null (Foreign Key to artists(artist_id))
        - **genre_id**: integer, not null (Foreign Key to genres(genre_id))
        - **Primary Key**: (artist_id, genre_id)
        """)
    
    with st.expander("album_artists", expanded=False):
        st.write("""
        - **album_id**: character varying(255), not null (Foreign Key to albums(album_id))
        - **artist_id**: character varying(255), not null (Foreign Key to artists(artist_id))
        - **Primary Key**: (album_id, artist_id)
        """)
    
    with st.expander("track_artists", expanded=False):
        st.write("""
        - **track_id**: character varying(255), not null (Foreign Key to tracks(track_id))
        - **artist_id**: character varying(255), not null (Foreign Key to artists(artist_id))
        - **Primary Key**: (track_id, artist_id)
        """)
    
    with st.expander("audio_features", expanded=False):
        st.write("""
        - **track_id**: character varying(255), not null (Primary Key, Foreign Key to tracks(track_id))
        - **danceability**: double precision, not null, default 0
        - **energy**: double precision, not null, default 0
        - **key**: integer, not null, default 0
        - **loudness**: double precision, not null, default -60
        - **mode**: integer, not null, default 0
        - **speechiness**: double precision, not null, default 0
        - **acousticness**: double precision, not null, default 0
        - **instrumentalness**: double precision, not null, default 0
        - **liveness**: double precision, not null, default 0
        - **valence**: double precision, not null, default 0
        - **tempo**: double precision, not null, default 0
        - **time_signature**: integer, not null, default 4
        """)

# Text area for SQL query input
query = st.text_area("Enter your SQL query:", "SELECT * FROM artists LIMIT 5;")

# Button to execute the query
if st.button("Execute Query"):
    try:
        # Send the query to the Flask backend
        response = requests.post(FLASK_URL, json={"query": query})
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the response
        data = response.json()

        if "error" in data:
            st.error(f"Error: {data['error']}")
        elif "message" in data:
            st.success(f"{data['message']} (Rows affected: {data['rows_affected']})")
        else:
            # Display the results in a table
            df = pd.DataFrame(data)
            st.write("Query Results:")
            st.dataframe(df)

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to execute query: {e}")

# Note about potential 500 Internal Server Error
st.markdown("""
**Note**: If the app gives a 500 Internal Server Error, it is likely due to Render winding down the free tier backend due to inactivity. Please wait 5–10 minutes after getting the error for it to go live again.
""")
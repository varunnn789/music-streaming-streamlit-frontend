import streamlit as st
import requests
import pandas as pd

st.title("Music Streaming Database Query Interface")

# Flask backend URL
FLASK_URL = "https://music-streaming-flask-backend.onrender.com/query"  # Replace with your Render URL

# Text area for SQL query input
query = st.text_area("Enter your SQL query:", "SELECT * FROM artists LIMIT 5")

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
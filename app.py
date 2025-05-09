import streamlit as st
import requests

# Page setup
st.set_page_config(page_title="The Court Oracle")
st.title("The Court Oracle")
st.markdown("Welcome to your God Mode command center for NBA fantasy and betting insights.")

# Odds API key
API_KEY = "d6b340f5f051e9885b02c4d27cf8f32f"
url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?regions=us&markets=h2h,spreads,totals&apiKey={API_KEY}"

# Fetch live odds
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    for game in data:
        teams = game["teams"]
        time = game["commence_time"]
        st.subheader(f"{teams[0]} vs {teams[1]}")
        st.caption(f"Starts at: {time}")
        for book in game["bookmakers"]:
            st.markdown(f"**{book['title']}**")
            for market in book["markets"]:
                st.markdown(f"_{market['key'].capitalize()}_")
                for outcome in market["outcomes"]:
                    st.write(f"{outcome['name']}: {outcome['price']}")
        st.markdown("---")
else:
    st.error("Odds API request failed. Check your key or wait a moment.")

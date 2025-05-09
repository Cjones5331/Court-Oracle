import streamlit as st
import requests
from datetime import datetime

# Page setup
st.set_page_config(page_title="The Court Oracle", layout="centered")
st.title("The Court Oracle")
st.markdown("Your live command center for NBA fantasy, Vegas lines, and player intelligence.")

# Odds API key and endpoint
API_KEY = "d6b340f5f051e9885b02c4d27cf8f32f"  # << REPLACE this with your actual Odds API key
url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?regions=us&markets=spreads&apiKey={API_KEY}"

# Fetch data
try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        if data:
            st.subheader("**Live NBA Matchups**")
            for game in data:
                if "teams" in game and "commence_time" in game:
                    teams = game["teams"]
                    start_time = datetime.fromisoformat(game["commence_time"].replace("Z", "+00:00"))
                    
                    st.markdown(f"### {teams[0]} vs {teams[1]}")
                    st.caption(f"**Tip-off:** {start_time.strftime('%I:%M %p')}")

                    for book in game.get("bookmakers", []):
                        st.markdown(f"**{book['title']}**")
                        for market in book.get("markets", []):
                            st.markdown(f"_{market['key']}_")
                            for outcome in market.get("outcomes", []):
                                st.write(f"{outcome['name']}: {outcome['price']}")
                        st.markdown("----")
        else:
            st.warning("No NBA data currently available.")
    else:
        st.error("Failed to retrieve data from The Odds API. Check your API key or plan limit.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

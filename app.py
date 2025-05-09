import streamlit as st
import requests
from datetime import datetime

# Page setup
st.set_page_config(page_title="The Court Oracle", layout="centered")
st.title("The Court Oracle")
st.markdown("Welcome to your **God Mode** command center for NBA fantasy + betting insights.")

# Divider
st.markdown("---")

# API setup
API_KEY = "d6b340f5f051e9885b02c4d27cf8f32f"
url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?regions=us&markets=h2h&apiKey={API_KEY}"

# Fetch odds
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    st.subheader("**Live NBA Matchups**")

    for game in data:
        teams = game["teams"]
        start_time = datetime.fromisoformat(game["commence_time"].replace("Z", "+00:00"))
        st.markdown(f"### {teams[0]} vs {teams[1]}")
        st.caption(f"**Tip-off:** {start_time.strftime('%b %d, %I:%M %p')}")

        for book in game["bookmakers"]:
            st.markdown(f"**{book['title']}**")
            for market in book["markets"]:
                st.markdown(f"• _{market['key'].upper()}_")
                for outcome in market["outcomes"]:
                    st.write(f"{outcome['name']}: `{outcome['price']}`")

        st.markdown("----")

    # Footer timestamp
    st.caption(f"Last updated: {datetime.now().strftime('%b %d, %Y %I:%M %p')}")
else:
    st.error("Odds API request failed. Check your API key or quota.")

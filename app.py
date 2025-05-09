import streamlit as st
import requests
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="The Court Oracle", layout="centered")

# --- HEADER ---
st.title("The Court Oracle")
st.caption("Your live command center for NBA fantasy, Vegas lines, and player intelligence.")
st.markdown("---")

# --- API SETUP ---
API_KEY = "d6b340f5f051e9885b02c4d27cf8f32f"
url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?regions=us&markets=h2h,spreads,totals,player_points&apiKey={API_KEY}"

# --- DATA FETCH ---
response = requests.get(url)
if response.status_code != 200:
    st.error("Failed to retrieve data from The Odds API. Check your API key or plan limit.")
    st.stop()

data = response.json()

# --- HELPER FUNCTIONS ---
def format_time(iso_str):
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime('%A, %b %d at %I:%M %p')
    except:
        return "Time Unavailable"

def display_outcomes(outcomes):
    for outcome in outcomes:
        name = outcome.get("name", "N/A")
        price = outcome.get("price", "N/A")
        line = outcome.get("point", "")
        display = f"â¢ **{name}**: `{price}`"
        if line:
            display += f" (Line: {line})"
        st.markdown(display)

# --- MAIN LOOP ---
for game in data:
    if "teams" not in game or "commence_time" not in game:
        continue

    teams = game["teams"]
    tipoff = format_time(game["commence_time"])
    st.markdown(f"## {teams[0]} vs {teams[1]}")
    st.caption(f"**Tip-off:** {tipoff}")

    for book in game.get("bookmakers", []):
        book_title = book.get("title", "Unknown Bookmaker")
        st.markdown(f"**{book_title}**")

        for market in book.get("markets", []):
            key = market.get("key", "unknown_market").replace("_", " ").title()
            st.markdown(f"**{key}**")
            display_outcomes(market.get("outcomes", []))

    st.markdown("---")

# --- FOOTER ---
st.caption(f"Last updated: {datetime.now().strftime('%b %d, %Y %I:%M %p')}")

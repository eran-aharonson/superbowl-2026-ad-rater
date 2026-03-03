import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="Superbowl LX 2026 AI Ad Rater", layout="wide")

st.title("🏈 Superbowl LX 2026 AI Ad Rater")

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(WORKING_DIR, "Superbowl 2026 AI commercials")
RESULTS_FILE = os.path.join(WORKING_DIR, "ratings.csv")

if not os.path.exists(VIDEO_DIR):
    st.error(f"Directory '{VIDEO_DIR}' not found. Please create it and add some videos.")
    st.stop()

# Helper mapping for nicer video names
def get_friendly_name(filename):
    lower_f = filename.lower()
    if "six pack" in lower_f:
        return "Anthropic - Six Pack"
    elif "mom" in lower_f:
        return "Anthropic - Communicate with Mom"
    elif "base44" in lower_f:
        return "Base44 - It's App to You"
    elif "gemini" in lower_f:
        return "Google - Gemini New Home"
    elif "openai" in lower_f or "codex" in lower_f:
        return "OpenAI - Build Things"
    elif "business idea" in lower_f:
        return "Anthropic - Business Idea"
    elif "copilot" in lower_f or "microsoft" in lower_f:
        return "Microsoft - Copilot 365"
    else:
        # Fallback to wiping out extensions and cleaning up common characters
        return filename.replace(".mp4", "").replace(".mov", "").replace("_", " ").strip()


videos = sorted([f for f in os.listdir(VIDEO_DIR) if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))])

if not videos:
    st.warning(f"No video files found in '{VIDEO_DIR}'.")
    st.stop()

# Load globally saved ratings
if os.path.exists(RESULTS_FILE):
    ratings_df = pd.read_csv(RESULTS_FILE)
else:
    ratings_df = pd.DataFrame(columns=["Video", "FriendlyName", "Rating"])

# Session state array to keep transient ratings until "Save All" is hit
if "current_ratings" not in st.session_state:
    st.session_state.current_ratings = {}

# Pre-populate session state with any existing global ratings for completeness
# (If user has rated before, show their old ratings)
# REMOVED: In a multi-user environment we should not pre-fill current_ratings
# with the entire global database, otherwise "Save All" will resubmit everyone else's votes.
# We only track fresh interactions in this session.


st.divider()
st.subheader("Rate the Ads")

# Interactive list of videos in a grid
cols_per_row = 3
for i in range(0, len(videos), cols_per_row):
    cols = st.columns(cols_per_row)
    for j in range(cols_per_row):
        if i + j < len(videos):
            video = videos[i + j]
            friendly_name = get_friendly_name(video)
            
            with cols[j]:
                st.markdown(f"#### {friendly_name}")
                video_path = os.path.join(VIDEO_DIR, video)
                with open(video_path, 'rb') as video_file:
                    video_bytes = video_file.read()
                st.video(video_bytes)
                
                # Rating directly underneath
                def on_star_click(vid=video):
                    # The callback runs before the rest of the script. We grab the value from session state
                    val = st.session_state[f"star_{vid}"]
                    if val is not None:
                        # Streamlit feedback is 0-indexed (0=1 star, 4=5 stars)
                        st.session_state.current_ratings[vid] = val + 1
                        
                st.feedback(
                    "stars", 
                    key=f"star_{video}", 
                    on_change=on_star_click, 
                )

st.divider()

# Only show "Save All Ratings" at the absolute bottom
st.subheader("Save Your Selections")
if st.button("Save All Votes globally", type="primary", use_container_width=True):
    # Convert session state dictionary into df
    new_rows = []
    
    # In a real app we'd have a user ID. For now we append to existing rows to track multi-votes.
    for vid, rating in st.session_state.current_ratings.items():
        # Only add to the CSV if a rating was actually given
        if pd.notna(rating) and rating > 0:
            fname = get_friendly_name(vid)
            new_rows.append({"Video": vid, "FriendlyName": fname, "Rating": rating})
        
    if new_rows:
        new_df = pd.DataFrame(new_rows)
        # We append, assuming each "Save All" is a new user's submission session
        combined_df = pd.concat([ratings_df, new_df], ignore_index=True)
        combined_df.to_csv(RESULTS_FILE, index=False)
        st.success(f"✅ Saved {len(new_rows)} ratings successfully!")
        
        # Reload to update leaderboard
        st.rerun()
    else:
        st.warning("No ratings to save. Please review and score at least one commercial.")

st.divider()

# The leaderboard displays the globally saved results from the CSV
if not ratings_df.empty:
    st.subheader("🏆 Global Leaderboard")
    
    # Filter out any lingering null/0 ratings just in case they snuck in
    valid_ratings_df = ratings_df[ratings_df["Rating"].notna() & (ratings_df["Rating"] > 0)]
    
    if not valid_ratings_df.empty:
        # Group by the video to calculate average rating and vote count
        grouped_df = valid_ratings_df.groupby("FriendlyName").agg(
            Average_Rating=('Rating', 'mean'),
            Votes=('Rating', 'count')
        ).reset_index()
        
        # Sort by highest average, then highest votes
        display_df = grouped_df.sort_values(by=["Average_Rating", "Votes"], ascending=[False, False]).reset_index(drop=True)
        display_df.index += 1 # 1-based index for rankings
        
        # Format the average rating to 1 decimal place
        display_df["Average_Rating"] = display_df["Average_Rating"].round(1)
        
        st.dataframe(
            display_df, 
            use_container_width=True,
            column_config={
                "FriendlyName": "Commercial",
                "Average_Rating": st.column_config.NumberColumn(
                    "⭐ Average Rating",
                    help="1-5 stars",
                    format="%.1f"
                ),
                "Votes": st.column_config.NumberColumn(
                    "👥 Total Votes",
                    help="Number of people who voted"
                )
            }
        )
    else:
        st.info("No valid ratings have been recorded yet.")

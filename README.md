# Superbowl LX 2026 AI Ad Rater 🏈

A Streamlit application that allows users to watch and rate AI-generated Superbowl commercials.

## Features
- View multiple video commercials directly in the browser
- Rate commercials out of 5 stars
- Persistent real-time global leaderboard with average ratings and total vote counts

## Local Development

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Add your video files (e.g. `*.mp4`) into a folder named `Superbowl 2026 AI commercials` in the root directory.

3. Run the app:
```bash
streamlit run app.py
```

## Deployment on Streamlit Community Cloud

Since this repo has video files (which are large and often exceeded GitHub's limits), the actual `Superbowl 2026 AI commercials/` folder is listed in `.gitignore` and not uploaded here. 

To deploy this properly on Streamlit Cloud:
1. Connect you GitHub account to Streamlit Community Cloud and create a new app pointing to this repo.
2. Because the video files are missing from GitHub, you'll need to either:
   - Host the videos on a platform (like YouTube, an S3 bucket, etc.) and change the code to load them via URL.
   - Or upload the videos via a file uploader inside the app.
   - Or use Git LFS (Large File Storage) to push the videos to GitHub so Streamlit can access them (though GitHub has limits on repository size).

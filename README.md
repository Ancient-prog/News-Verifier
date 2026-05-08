# News Verifier — AI Fake News Detection

## Deploy to Render (Free — Step by Step)

### Step 1 — Push to GitHub
1. Go to [github.com](https://github.com) and create a **free account** (if you don't have one)
2. Click **New repository** → name it `news-verifier` → click **Create repository**
3. Upload these 4 files into the repo:
   - `server.py`
   - `index.html`
   - `requirements.txt`
   - `Procfile`

### Step 2 — Deploy on Render
1. Go to [render.com](https://render.com) and sign up for free
2. Click **New +** → **Web Service**
3. Connect your GitHub account → select your `news-verifier` repo
4. Fill in the settings:
   - **Name**: `news-verifier`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn server:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120`
5. Click **Advanced** → **Add Environment Variable**:
   - Key: `GEMINI_API_KEY`
   - Value: `AIzaSyCkUXlyV0MkZcL5A4Pcq8a6Ea5GW9VERec`
6. Click **Create Web Service**

### Step 3 — Get your link
After 2–3 minutes Render will give you a live URL like:
```
https://news-verifier.onrender.com
```
Open that on any phone or laptop — no Python installation needed!

## Local Development
```bash
pip install flask google-genai gunicorn
python server.py
# Open http://localhost:8000
```

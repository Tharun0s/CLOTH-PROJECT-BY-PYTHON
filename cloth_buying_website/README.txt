# Threadly - Simple Clothing Buying Website

## Features
- Responsive clothing store page with product photos
- Product category filters
- Buy Now checkout form
- Python Flask backend
- SQLite database file (`database/cloth_store.db`) stores products and orders
- Admin orders page at `/admin`
- Demo admin password: `123456789`

## Run on Windows
1. Install Python 3.10+.
2. Open Command Prompt in this project folder.
3. Install requirements:
   `pip install -r requirements.txt`
4. Start the app:
   `python app.py`
5. Open `http://127.0.0.1:5000` in your browser.
6. Admin orders: `http://127.0.0.1:5000/admin` (password `123456789`).

## Database
The app uses SQLite, so no separate SQL server password is needed. The database file is included in `database/cloth_store.db`. A MySQL-compatible starter schema is included at `database/schema.sql`; the running app currently uses SQLite.

## Product photos
The demo uses Unsplash image URLs, so an internet connection is needed for the photos to load. Replace the URLs in `app.py` if you want to use your own images.

## Important
This is a learning/demo project. Before deploying publicly, replace the Flask secret key, use secure password hashing, validate orders server-side against database product prices, and configure production hosting.

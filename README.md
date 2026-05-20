# 🏡 NestFinder Pakistan

A Streamlit web app for browsing and booking rental homes across Pakistan.
Built with a curated dataset of 50 properties spanning 21 cities, from
luxury Karachi beachfront villas to wooden cabins in Hunza.

## Features

- 50 realistic listings across Islamabad, Lahore, Karachi, Hunza, Skardu, Murree, Naran, Swat, Gwadar, and more
- Filter by city, property type, guest capacity, max price, or keyword
- Live price summary that reacts to selected dates
- Booking confirmation with auto-generated reference codes
- "My Bookings" dashboard with search, status, and cancellation
- Mobile-friendly responsive layout
- Custom typography (Playfair Display + DM Sans) with a navy / gold theme

## Project structure

```
nestfinder/
├── app.py              # Main Streamlit app
├── properties.json     # 50-property dataset
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── .gitignore          # Ignores runtime bookings.json
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501

## Deploy to Streamlit Community Cloud (free)

1. **Push to GitHub**
   ```bash
   cd nestfinder
   git init
   git add .
   git commit -m "Initial commit: NestFinder Pakistan"
   git branch -M main
   git remote add origin https://github.com/<your-username>/nestfinder.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io and sign in with GitHub
   - Click **"New app"**
   - Repository: `<your-username>/nestfinder`
   - Branch: `main`
   - Main file path: `app.py`
   - Click **Deploy**

3. **Wait ~2 minutes** for the first build. You'll get a public URL like
   `https://nestfinder-xxxx.streamlit.app`.

### Notes about deployment

- **Bookings persistence**: Streamlit Community Cloud's filesystem is ephemeral,
  so `bookings.json` resets when the app restarts. For real persistence in
  production, swap the `load_bookings()` / `save_bookings()` functions for a
  cloud database (Firebase, Supabase, MongoDB Atlas, or Google Sheets via
  `st.connection`). The app already gracefully falls back to session state
  if the filesystem is read-only.
- **Custom domain**: Available on Streamlit Cloud paid plans, or proxy through
  Cloudflare for free.
- **Sleep policy**: Free apps sleep after ~7 days of inactivity. They wake up
  on the first new request (5-10 second delay).

## Deploy elsewhere

### Hugging Face Spaces

1. Create a new Space, SDK = **Streamlit**
2. Upload all files (or connect to your GitHub repo)
3. The Space auto-builds and gives you `https://huggingface.co/spaces/<user>/nestfinder`

### Render / Railway

Add a `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```
Then connect your GitHub repo on either platform.

### Docker (any host)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

## Customising the data

To add or modify properties, edit `properties.json` directly. Each entry
needs these fields:

```json
{
  "id": 51,
  "name": "Your Property Name",
  "city": "Lahore",
  "location": "Lahore, DHA Phase 5",
  "type": "Villa",
  "bedrooms": 3,
  "bathrooms": 2,
  "guests": 6,
  "price": 12000,
  "emoji": "🏡",
  "amenities": ["WiFi", "AC", "Pool"],
  "description": "Short description text.",
  "rating": 4.7,
  "host": "Host name",
  "image": "https://picsum.photos/seed/nestfinder51/800/450"
}
```

The `image` URL can be any publicly accessible image. Picsum gives stable
random images per seed; for real photos, host them on Cloudinary, ImageKit,
or any CDN.

## Going from demo to production

If you want this to become a real product, here's the upgrade path:

1. **Real listings data**: Pakistan's major portals (Zameen, Graana, Ilaan)
   do not offer public APIs. Options:
   - Partner directly with property managers and onboard listings manually
   - Use a paid scraping API (RapidAPI marketplace)
   - Build host-side onboarding so property owners list themselves
2. **Real payments**: Integrate Easypaisa / JazzCash / Stripe instead of the
   current dropdown
3. **Auth**: Add `streamlit-authenticator` or migrate to a framework like FastAPI + Next.js
4. **Database**: Replace JSON files with PostgreSQL or Firestore
5. **Notifications**: Email confirmations via SendGrid, SMS via Twilio Pakistan

## Tech stack

- Streamlit (UI)
- Python 3.10+
- JSON for data storage (demo)
- Picsum for placeholder images
- Playfair Display + DM Sans (Google Fonts)

## License

For demo and educational purposes. Adapt freely for your own projects.

---

Built in Islamabad, Pakistan. 🇵🇰

# GlobeTrotter

A personalized multi-city travel planning platform built with **Django**. This frontend-first package runs independently with SQLite while the MySQL backend is being developed.

GlobeTrotter helps users create trips, manage destinations and activities, organize itineraries, track estimated expenses, view plans on a calendar, and share trips with others.

## Features

* User authentication
* Create and manage trips
* Multi-city itinerary planning
* Destination & activity search
* Activity scheduling
* Trip budget & expense tracking
* Calendar / timeline view
* Public trip sharing
* User profile & saved destinations

## Tech Stack

* **Backend:** Django, Python
* **Database:** MySQL 
* **Frontend:** HTML, CSS, JavaScript
* **Charts:** Chart.js

## Getting Started

### Frontend-only mode (recommended while the backend is in progress)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

This package defaults to `FRONTEND_ONLY=True`, which uses a local SQLite database only for Django's built-in framework tables. No MySQL server is required to render and test the frontend screens.

### Switch back to MySQL later

Set `FRONTEND_ONLY=False` in `.env` and provide the `DB_*` values for the backend environment.


## Project Status

🚧 Currently under development.

## Author

**Godani Shubham**Backend developer

GitHub: [@GodaniShubham](https://github.com/GodaniShubham)

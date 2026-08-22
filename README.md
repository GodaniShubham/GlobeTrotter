<div align="center">

  <img src="https://www.odoo.com/web/static/img/odoo_logo.svg" alt="Odoo Logo" width="150" />
  <h1>GlobeTrotter × Odoo Travel Suite</h1>
  
  <p>
    <strong>A personalized, AI-powered multi-city travel planning platform built with Django.</strong>
  </p>

  <p>
    <a href="#features">Features</a> •
    <a href="#demo-video">Demo Video</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#tech-stack">Tech Stack</a>
  </p>

</div>

---

## 🌟 Overview

GlobeTrotter helps users create trips, manage destinations and activities, organize itineraries, track estimated expenses, view plans on a calendar, and instantly generate full multi-day plans using AI.

Originally a frontend-first package, this system is now a fully integrated backend platform leveraging the Groq LLaMA 3 API for intelligent trip building and the Wikipedia REST API for automated image sourcing.

---

## 🎥 Demo Video

> **[Watch the full GlobeTrotter × Odoo Demo Video Here (Click to Play)](#)** 
*(Replace with actual YouTube/Vimeo link)*

<a href="#">
  <img src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?q=80&w=2000&auto=format&fit=crop" alt="GlobeTrotter Video Thumbnail" width="100%" style="border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
</a>

---

## ✨ Core Features

### 🤖 AI-Powered Itinerary Generation
Stop planning manually. Tell GlobeTrotter your destination, pace, and interests, and the **Groq AI** integration will automatically build a realistic, day-by-day JSON itinerary and save it to your database.

### 🖼️ Automated Wikipedia Image Fetching
When the AI generates a trip, our backend automatically queries the **Wikipedia API** to fetch high-quality cover images for your destination and thumbnails for every single activity. No manual photo sourcing needed.

### 🛡️ Secure OTP Email Authentication
Custom-designed, mobile-responsive "GlobeTrotter × Odoo" email templates power a robust 6-digit OTP (One-Time Password) system for safe and reliable password recovery.

### 📊 Dynamic Admin & Analytics Dashboard
A dedicated, secure `/admin-panel/` built for platform administrators. Track rolling 8-week user growth, view the most popular destinations, manage users, and track platform adoption in real-time.

### 🗺️ Full Travel Suite
- **Multi-city Planner:** Drag-and-drop itinerary building for complex trips.
- **Budget Tracking:** Keep an eye on estimated expenses across cities.
- **Public Sharing:** Generate public links to share your itineraries with friends.

---

## 🖼️ Gallery

<div align="center">
  <img src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600&auto=format&fit=crop" width="48%" alt="Beach Destination" style="border-radius: 8px;"/>
  <img src="https://images.unsplash.com/photo-1499856871958-5b9627545d1a?q=80&w=600&auto=format&fit=crop" width="48%" alt="Paris Destination" style="border-radius: 8px;"/>
</div>

---

## 🛠️ Tech Stack

- **Backend Framework:** Django (Python 3.13)
- **Database:** SQLite (Local Dev) / MariaDB (Production)
- **AI Integration:** Groq API (LLaMA 3 70B)
- **Image Sourcing:** Wikipedia REST API
- **Frontend:** Vanilla HTML, CSS, JavaScript (Mobile-First Responsive)
- **Charting:** Custom CSS/JS HTML Charts

---

## 🚀 Getting Started

Follow these instructions to run GlobeTrotter locally on your machine.

### 1. Clone & Setup Environment

```bash
git clone https://github.com/GodaniShubham/GlobeTrotter.git
cd GlobeTrotter
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add the following keys:
```ini
DEBUG=True
USE_LOCAL_DB=1
GROQ=your_groq_api_key_here
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 4. Database Setup & Seed
Apply migrations and seed the database with 30+ Indian cities and a default itinerary:
```bash
python manage.py migrate
python seed_db.py
```

### 5. Run the Server
```bash
python manage.py runserver
```
Open `http://127.0.0.1:8000/` in your browser.

**Admin Access:**  
Navigate to `/admin-panel/`  
**Email:** `admin@globetrotter.com`  
**Password:** `admin123`

---

## 👨‍💻 Author

**Godani Shubham** — Backend Developer  
GitHub: [@GodaniShubham](https://github.com/GodaniShubham)

<div align="center">
  <p><i>Building the future of travel planning with Odoo.</i></p>
</div>

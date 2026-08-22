# GlobeTrotter × Odoo

> **A focused multi-city travel planning workspace for building trips, shaping itineraries, discovering places, tracking budgets, and sharing travel ideas.**

<div align="center">

**Plan the route. Shape the days. Travel your way.**

</div>

---

## Product at a glance

GlobeTrotter is a Django-based travel planning platform built around one idea: **the traveller stays in control of the journey**.

The application brings trip creation, a manual itinerary builder, destination and activity discovery, budget planning, calendar views, public itinerary sharing, community features, account recovery, and an administrator workspace into one product.

The current codebase contains these Django applications:

`accounts` · `activities` · `community` · `core` · `destinations` · `expenses` · `trips` · `transport` · `admin_panel`

---

## What you can do

| Area | What it provides |
|---|---|
| **Trip planning** | Create a trip with dates, then build the journey step by step. |
| **Manual itinerary builder** | Add cities, set exact arrival/departure dates, add activities, choose times, attach notes, and set custom costs. |
| **Destination discovery** | Browse/search cities from the travel catalogue. |
| **Activity discovery** | Explore activities associated with destinations. |
| **Budget** | Track planned travel spend and activity costs. |
| **Calendar** | Review the journey in a calendar-oriented view. |
| **Community** | Publish travel conversations, reply, like, save, share, report, and receive community notifications. |
| **Password recovery** | Recover access using the configured password-recovery flow and OTP pages. |
| **Admin workspace** | Manage users, cities, activities, analytics, and administrative settings from `/admin-panel/`. |

---

## The planning flow

```text
Create Trip
    │
    ├── Trip name
    ├── Start / end date
    └── Trip note
         │
         ▼
Manual Itinerary Builder
         │
         ├── Add destination
         │      ├── Arrival
         │      └── Departure
         │
         ├── Add activity
         │      ├── Day
         │      ├── Start / end time
         │      ├── Cost
         │      └── Notes
         │
         ▼
Preview
   ├── Itinerary
   ├── Calendar
   └── Budget
```

The manual planner is structured around explicit user choices rather than silently changing the traveller's plan.

---

## Community workspace

The community module is wired as a full product area rather than a static feed.

Current routes cover:

```text
/community/
/community/new/
/community/saved/
/community/post/<id>/
/community/post/<id>/reply/
/community/post/<id>/like/
/community/post/<id>/save/
/community/post/<id>/share/
/community/post/<id>/report/
/community/post/<id>/updates/
/community/notifications/
/community/notifications/read/
```
> **[Watch the full GlobeTrotter × Odoo Demo Video Here (Click to Play)](#)** 
*([https://drive.google.com/file/d/1AR_jGWX2f2O3xJr2DHjf-QO8d0M1PFWn/view?usp=sharing])*

This gives the product a social layer for asking questions, exchanging itineraries, discussing destinations, and keeping track of community activity.

---

## Admin workspace

Administrative functionality lives under:

```text
/admin-panel/
```

The repository contains dedicated admin views/templates for:

- Dashboard
- Users
- User details
- Cities
- City creation/editing
- Activities
- Activity creation/editing
- Analytics
- Settings

The admin area is kept separate from the traveller-facing workspace so the two experiences can evolve independently.

---

## Technical architecture

```text
Browser
   │
   ▼
Django URL Router
   │
   ├── accounts
   ├── trips
   ├── destinations
   ├── activities
   ├── expenses
   ├── community
   ├── transport
   ├── core
   └── admin_panel
   │
   ▼
Django Models / Database
```

Frontend rendering is template-based with shared HTML/CSS/JavaScript and page-specific assets where needed.

The project contains utility modules for AI generation and image fetching in:

```text
core/ai_generator.py
core/image_fetcher.py
```

---

## Tech stack

### Backend

- Python
- Django
- Django ORM
- Django authentication/session stack
- CSRF-protected forms

### Frontend

- HTML templates
- CSS
- Vanilla JavaScript
- Responsive layouts
- Shared application shell with page-specific styling

### Data & integrations

- Relational database through Django ORM
- Pillow for image handling
- `requests` for HTTP integrations
- Environment-based configuration via `python-dotenv`

Current dependency file:

```text
Django~=5.0.0
PyMySQL>=1.2.0
python-dotenv>=1.2.3
requests>=2.31.0
Pillow>=10.0.0
```

---

## Project structure

```text
GlobeTrotter/
├── accounts/              # Authentication, profiles, recovery
├── activities/            # Activity catalogue
├── admin_panel/           # Custom administrative workspace
├── community/             # Posts, replies, reactions, notifications
├── config/                # Django project configuration and routing
├── core/                  # Shared utilities / integrations
├── destinations/          # City and destination catalogue
├── expenses/              # Expense and budget domain
├── static/                # CSS, JavaScript, images, admin assets
├── templates/             # Shared and page-specific templates
├── transport/             # Transport domain
├── trips/                 # Trips, stops, itinerary, calendar
├── manage.py
└── requirements.txt
```

---

## Local setup

### 1. Clone the repository

```bash
git clone https://github.com/GodaniShubham/GlobeTrotter.git
cd GlobeTrotter
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment

Create a local `.env` file from the repository's example configuration when available.

Keep secrets out of Git. Typical configuration in this project includes:

- `APP_PASSWORD`
- `DB_HOST`
- `DB_NAME`
- `DB_PASSWORD`
- `DB_PORT`
- `DB_USER`
- `DEBUG`
- `FRONTEND_ONLY`
- `SECRET_KEY`

**Never commit passwords, API keys, or local environment files.**

### 5. Apply migrations

```bash
python manage.py migrate
```

If your checkout includes the catalogue/setup seed command, run the relevant seed command after migrations.

### 6. Start Django

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## Important development routes

| Route | Purpose |
|---|---|
| `/` | Landing page |
| `/login/` | Sign in |
| `/signup/` | Create account |
| `/dashboard/` | Travel dashboard |
| `/trips/new/` | Start a new trip |
| `/trips/` | Trip library |
| `/trip/builder/?trip=<id>` | Manual itinerary builder |
| `/trip/itinerary/?trip=<id>` | Itinerary preview |
| `/discover/cities/` | City discovery |
| `/discover/activities/` | Activity discovery |
| `/trip/budget/?trip=<id>` | Budget view |
| `/trip/calendar/?trip=<id>` | Calendar view |
| `/community/` | Community |
| `/community/notifications/` | Notifications |
| `/admin-panel/` | Custom admin workspace |

---

## Development checks

Before committing changes:

```bash
python manage.py check
```

After schema/model changes:

```bash
python manage.py makemigrations
python manage.py migrate
```

For a clean repository state:

```bash
git status
```

Keep generated artifacts, temporary implementation notes, local databases, secrets, and environment files out of the production repository unless intentionally required.

---

## Design direction

GlobeTrotter follows an editorial travel-workspace aesthetic:

- Odoo-inspired collaboration
- GlobeTrotter-led brand identity
- Purple / teal brand accents
- Spacious cards and calm surfaces
- Strong travel typography
- Handwritten editorial accents used selectively
- Responsive desktop and mobile layouts
- Functional UI before decoration

The product should feel like a **well-designed travel desk**, not a spreadsheet.

---

## Current capabilities detected in this build

- ✅ Admin Panel
- ✅ Community
- ✅ Manual Itinerary Builder
- ✅ City Discovery
- ✅ Activity Discovery
- ✅ Trip Budget
- ✅ Trip Calendar
- ✅ Password Recovery

---

## Contributor principles

1. Preserve backend contracts when refining templates.
2. Prefer compatible trip-specific URL patterns when evolving routes.
3. Keep ownership checks on user-owned trip and community resources.
4. Preserve CSRF protection on state-changing forms and requests.
5. Add migrations through Django instead of rewriting applied migration history.
6. Keep feature-specific styling isolated so the shared application shell remains stable.

---

## Project

**Repository:** `GodaniShubham/GlobeTrotter`  
**Product:** `GlobeTrotter × Odoo`  
**Focus:** Multi-city travel planning, itinerary building, discovery, budgeting, community, and administration.

<div align="center">

### Plan the route. Shape the days. Travel freely.

</div>

GLOBETROTTER COMMUNITY — END-TO-END INTEGRATION
=================================================

This package adds a real database-backed community feature. It uses Django ORM and therefore writes to whichever DB the project is configured to use (MySQL for the backend developer, SQLite for local frontend-only mode).

Included backend:
- community/models.py
- community/forms.py
- community/views.py
- community/admin.py
- community/migrations/0001_initial.py
- community/tests.py
- config/settings.py (adds the community app)
- config/urls.py (adds community endpoints)

Included frontend:
- templates/pages/community.html
- templates/pages/community_new_post.html
- templates/pages/community_post.html
- templates/pages/community_saved.html
- static/css/community.css
- static/js/community.js

COMMUNITY FLOWS
---------------
1. Public community feed
   /community/
   - search by title/body/city
   - category filters
   - popular conversations
   - post list is loaded from SQL

2. Create post
   /community/new/
   - login required
   - CSRF protected Django form
   - validates title/body
   - saves author/category/city/body into CommunityPost

3. Post detail
   /community/post/<id>/
   - real post + replies
   - reply form writes CommunityReply to SQL
   - like/save actions write CommunityLike / CommunitySave
   - report form writes CommunityReport
   - author/staff can soft-delete a post

4. Saved posts
   /community/saved/
   - login required
   - shows posts saved by the current user from SQL

5. Admin
   /admin/
   - CommunityPost, CommunityReply, CommunityReport, CommunityLike, CommunitySave are registered

DATABASE
--------
The migration creates the community tables. When the backend developer merges this into the MySQL-backed project, run:

    python manage.py migrate

The tables are then created in the configured MySQL database. No SQLite data is copied to MySQL; both environments use the same models/migrations.

LOCAL SQLITE
------------
If FRONTEND_ONLY=True in config/settings.py, Django uses frontend.sqlite3 automatically. The same community models will write to that local SQLite database after:

    python manage.py migrate

IMPORTANT
---------
Do not replace an existing config/settings.py or config/urls.py blindly if those files have newer backend changes. Merge the community app, then ensure 'community' is in INSTALLED_APPS and the community URL patterns are present.

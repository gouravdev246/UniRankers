## Goal
Allow logged-in students to add achievements (CGPA, badge, skills, certificate photo). Each submission awards points (e.g., certificate = 10, skill = 5, badge = 3, CGPA mapped). Leaderboard updates automatically from stored data.

## Model Updates
1. Extend `leaderboard.models.Achievement`:
   - Add `category='BADGE'` to `CATEGORY_CHOICES`.
   - Add `certificate_image = ImageField(upload_to='certificates/', blank=True, null=True)`.
   - Optionally add `cgpa = DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)` to store numeric CGPA cleanly.

## Media Settings
1. Configure media in `unirank/settings.py`:
   - `MEDIA_URL = '/media/'`, `MEDIA_ROOT = BASE_DIR / 'media'`.
2. Serve media in dev: in `unirank/urls.py` add static serving when `DEBUG`.

## Forms & Views
1. Forms (`leaderboard/forms.py`):
   - `AchievementForm` with fields appropriate to category; include `certificate_image`.
2. Views (`leaderboard/views.py`):
   - `@login_required add_achievement_view(request)`:
     - `GET`: render form.
     - `POST`: validate, compute points via helper, save `Achievement(user=request.user, ...)`.
   - Points helper:
     - `CERTIFICATION`: 10 points
     - `SKILL`: 5 points per new skill
     - `BADGE`: 3 points
     - `CGPA`: map to points (proposal: `points = round(cgpa * 10)`) to keep CGPA significant but balanced.
3. URLs (`leaderboard/urls.py`):
   - Add `path('add/', views.add_achievement_view, name='add_achievement')`.

## Templates (Orange/White)
1. Add `templates/add_achievement.html`:
   - Orange gradient header; Bootstrap form with category selector showing context help.
   - File input for certificate image; numeric input for CGPA; text inputs for title/details.
   - Success message and link to Leaderboard/Dashboard.

## Dashboard Integration
- Add a “Add Achievement” button on `dashboard.html` linking to `leaderboard:add_achievement`.
- Optional: list recent achievements for the current user.

## Validation
- Upload certificate images stored under `media/certificates/` and accessible in dev.
- Submitting achievements updates points; refreshing `/leaderboard/` reflects new totals.
- Form handles category-specific fields gracefully and prevents missing required inputs.

## Deliverables
- Model changes (with migrations), media settings, static media serving in dev.
- Achievement form, view, URL, and orange-themed template.
- Dashboard button linking to the submission page.

Confirm and I’ll implement the model/setting updates, views, forms, URLs, templates, and point rules, then verify end-to-end.
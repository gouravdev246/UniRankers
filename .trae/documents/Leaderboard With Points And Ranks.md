## Goal
Build a leaderboard where students see their rank based on points computed from certifications, skills, CGPA, etc., and fetch data from the database.

## Data Model
1. Use existing custom user model `users.models.User` as the owner of achievements.
2. Add an `Achievement` model (new app `leaderboard` or inside `users`):
   - Fields: `user (FK to users.User)`, `category (choices: CERTIFICATION, SKILL, CGPA, OTHER)`, `title`, `details`, `value (e.g., hours, level, cgpa)`, `points (int)`, `created_at`.
   - Optionally add `Certification`/`Skill` models if you prefer more structure; but a single `Achievement` is sufficient initially.
3. Points strategy:
   - Certifications: base points per certification; tiered bonus by level.
   - Skills: points by proficiency level (Beginner/Intermediate/Advanced).
   - CGPA: map to points (e.g., `points = int(cgpa * 100)` or tiered buckets).
   - Store computed `points` per achievement row; keep rules in a service/helper.

## Query & Ranking
1. Aggregate points per student:
   - `User.objects.annotate(total_points=Coalesce(Sum('achievements__points'), 0)).order_by('-total_points', 'name')`.
   - Prefetch achievements for optional detail display.
2. Ranking number:
   - Use Python enumeration to derive `rank` in the template, or annotate with `Window(Rank())` if needed.
3. Pagination:
   - `Paginator(users_qs, 25)` to keep pages fast.

## Routes & Views
1. Create `leaderboard/views.py` with `leaderboard_view(request)`:
   - Enforces read-only access; public page.
   - Executes the aggregation query and hands `users_with_points` + pagination to the template.
2. `leaderboard/urls.py`:
   - `path('leaderboard/', views.leaderboard_view, name='leaderboard')`.
3. Include routes:
   - In `unirank/unirank/urls.py`, include `leaderboard.urls`.
   - Update navbar link in `templates/base.html` to `{% url 'leaderboard' %}`.

## Template (Orange/White)
1. Use existing `templates/leaderboard.html` extending `base.html`.
2. Design:
   - Orange gradient header with page title and brief description.
   - Table with columns: `Rank`, `Name`, `Total Points`, optional `Top Achievement`.
   - Orange-accented badges for categories; hover states consistent with `--orange-*` vars.
3. Responsive:
   - Collapsible cards on mobile; sticky header for table on desktop.

## Admin & Data Entry
1. Register `Achievement` in admin for manual entry initially.
2. Optional: add forms/pages to submit achievements.
3. Optional: service to compute points from raw inputs (CGPA, skill level) and store into `Achievement.points`.

## Performance & Integrity
- Index `Achievement.user` and `category`.
- Use `Coalesce` to avoid `NULL` totals.
- Guard against duplicate counting via unique constraints if applicable.

## Validation
- Seed a few achievements and verify:
  - Leaderboard orders by `total_points`.
  - Rank numbers are correct and stable across pages.
  - Pagination works and is fast.
  - Navbar link navigates to the page.

## Deliverables
- `Achievement` model and admin registration.
- `leaderboard_view` + `leaderboard/urls.py` inclusion.
- Styled `leaderboard.html` (orange/white theme).
- Navbar link fixed to the new route.

Confirm and I’ll implement the models, views, URLs, and template, wire the orange theme, and ensure the data fetch and ranking work end-to-end.
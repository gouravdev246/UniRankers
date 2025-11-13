## Goal
Create a modern, responsive user profile page with an orange/white theme that matches the existing site styles and Bootstrap usage.

## Page Layout
1. Use `templates/profile.html` extending `base.html`.
2. Hero header with user avatar placeholder (initials circle), name, and a subtle orange gradient accent.
3. Main content as a Bootstrap card/grid showing key details:
   - Name, email, phone number (from `request.user`)
   - Join date if available (`created_at`)
4. Action row with “Edit Profile” and “Logout” buttons.

## Data Display
- Swap any `first_name` usage to the custom field `{{ request.user.name }}`.
- Show `{{ request.user.email }}` and `{{ request.user.phone_number }}` when present, with empty-state text if missing.

## Theme & Styles
- Reuse existing CSS variables from `base.html` (e.g., `--orange-primary`, `--orange-light`).
- Apply Bootstrap 5 classes with a few utility classes:
  - Headers and accents: orange gradient background, white text.
  - Cards: white background with soft orange shadow/border on hover.
  - Buttons: primary orange and outline-white variants.
- Keep styles inline within the template or within `base.html` blocks; no new static files.

## Routes & Views
- Keep `users/urls.py` `path('profile/', views.profile_view, name='profile')`.
- Ensure `@login_required` on `profile_view` remains; it renders `profile.html` and passes `request.user`.

## Optional Edit Flow
1. Add `edit_profile_view` (`GET` shows form, `POST` saves) with `login_required`.
2. Create `users/forms.py` `ModelForm` for `User` (`fields=['name','phone_number','email']`).
3. URL: `path('profile/edit/', views.edit_profile_view, name='edit_profile')`.
4. Template `templates/edit_profile.html`: minimal Bootstrap form using orange accents.

## Accessibility & Responsive
- Ensure sufficient contrast on orange backgrounds.
- Mobile-first layout: avatar/name stack on small screens; grid becomes single column.
- Use semantic tags and aria-labels for action buttons.

## Validation
- Logged-in user sees `users/profile/` with correct data and theme.
- Logged-out user redirected to login.
- Form saves updates; messages/alerts confirm success.
- Verify on common breakpoints (sm, md, lg).

## Deliverables
- Updated `profile.html` with orange/white design.
- (Optional) `edit_profile_view`, `ModelForm`, URL, and `edit_profile.html`.

Confirm this plan and I’ll implement it immediately.
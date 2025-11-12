## Goal
Make the Add Achievement form dynamically show relevant fields based on selected category (Certification, Skill, Badge, CGPA), and validate accordingly.

## UI Changes
1. Wrap each field in identifiable containers in `templates/add_achievement.html` (title, details, value, cgpa, certificate image).
2. Add a small JavaScript snippet that:
   - Listens to category select changes.
   - Shows/hides containers per category.
   - Updates the label text for the generic `value` field (e.g., “Skill”, “Badge”, “Certificate code”).
   - Sets/clears the `required` attribute on inputs to help users (server still validates).

## Server Validation
1. Extend `leaderboard/forms.py:AchievementForm.clean` to enforce category-specific requirements:
   - Certification: require `certificate_image`; optionally require `value`.
   - Skill: require `value` (skill name/level).
   - Badge: require `value`.
   - CGPA: require `cgpa` and allow other fields to be empty.

## No Model Changes
- Reuse existing fields: `title`, `details`, `value`, `cgpa`, `certificate_image`.

## Validation
- Test each category selection to ensure the right fields appear and submit successfully.
- Leaderboard totals update accordingly.

Proceeding to implement these changes immediately.
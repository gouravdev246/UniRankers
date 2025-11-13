## Overview
Design and implement a high‑impact Home page that fits the existing Bootstrap 5 setup and the orange gradient brand style already present in `templates/base.html`. Use lightweight, GPU‑accelerated CSS transitions with a small IntersectionObserver script for scroll reveals. Avoid heavy libraries by default; offer GSAP via CDN as an optional enhancement if desired.

## UI Structure
1. Hero Section
- Full‑viewport hero with gradient/duotone background and optional video/image overlay
- Bold headline, concise subheading, primary CTA and secondary CTA
- Subtle parallax of decorative layers using `transform: translate3d` driven by scroll

2. Features Section
- 4 feature cards (e.g., Leaderboard, Portfolio, Mentorship, Achievements)
- Inline SVG or Bootstrap Icons via CDN; hover micro‑interactions (lift, glow)
- Clear titles with short descriptions; responsive grid using Bootstrap

3. Visual Elements
- Brand‑aligned gradient tokens (orange primary/dark/light) expanded into a modern palette
- Soft glassmorphism panels and conic/radial gradient shapes for depth
- Scroll‑triggered reveals (fade+slide); reduced motion respected

## Accessibility & Compliance
- Semantic landmarks (`header`, `main`, `section`), accessible buttons/links
- Color contrast ≥ 4.5:1; visible focus rings; keyboard‑navigable cards
- `prefers-reduced-motion` CSS to disable animation; `alt` text for images/video

## Performance Targets
- 60fps animations using `opacity`/`transform` only; `will-change` selectively
- Lazy‑load imagery (`loading="lazy"`), async decode, optimal media sizes
- `content-visibility: auto` for below‑the‑fold (with graceful fallback)

## Cross‑Browser
- Works on modern Chrome, Safari, Firefox, Edge
- Degrades gracefully if `IntersectionObserver`/`content-visibility` not present

## Implementation Plan
### Files to Add (under project BASE_DIR `unirank/`)
- `static/css/home.css` – page styles, gradients, animations, responsive rules
- `static/js/home.js` – IntersectionObserver for reveals, optional parallax
- `static/img/` – placeholder hero image/video poster; simple SVG icons if needed

### Existing Files to Update
- `templates/base.html`
  - Load Django static: `{% load static %}` and include `home.css`/`home.js` on home route only or universally (minimal overhead)
  - Optionally include Bootstrap Icons CDN for card icons
- `templates/home.html`
  - Replace current minimal markup with:
```
{% extends 'base.html' %}
{% load static %}
{% block content %}
<header class="hero">
  <div class="hero-bg">
    <div class="bg-layer layer-1"></div>
    <div class="bg-layer layer-2"></div>
  </div>
  <div class="hero-content container">
    <h1 class="reveal">Level up your university journey</h1>
    <p class="subheading reveal">Showcase achievements, climb leaderboards, and connect with mentors.</p>
    <div class="cta reveal">
      <a href="{% url 'signup' %}" class="btn btn-signup">Get Started</a>
      <a href="{% url 'leaderboard' %}" class="btn btn-login">View Leaderboard</a>
    </div>
  </div>
</header>
<main>
  <section class="features container">
    <div class="row g-4">
      <div class="col-12 col-md-6 col-lg-3">
        <article class="feature-card reveal">
          <div class="icon">...</div>
          <h3>Leaderboard</h3>
          <p>Track rankings and celebrate progress.</p>
        </article>
      </div>
      <div class="col-12 col-md-6 col-lg-3">
        <article class="feature-card reveal">
          <div class="icon">...</div>
          <h3>Portfolio</h3>
          <p>Curate projects, certificates, and achievements.</p>
        </article>
      </div>
      <div class="col-12 col-md-6 col-lg-3">
        <article class="feature-card reveal">
          <div class="icon">...</div>
          <h3>Mentorship</h3>
          <p>Connect with mentors to accelerate growth.</p>
        </article>
      </div>
      <div class="col-12 col-md-6 col-lg-3">
        <article class="feature-card reveal">
          <div class="icon">...</div>
          <h3>Achievements</h3>
          <p>Collect and share verified certificates.</p>
        </article>
      </div>
    </div>
  </section>
</main>
{% endblock %}
```

### CSS Key Points (`static/css/home.css`)
- Gradient tokens:
```
:root {
  --orange-primary:#ff8c42; --orange-dark:#ff7b2d; --orange-light:#ffeee1;
  --bg-1: conic-gradient(from 180deg at 50% 50%, #fff 0%, #ffe0cc 50%, #fff 100%);
}
.hero {min-height: 100vh; position: relative; overflow: clip;}
.hero-bg .bg-layer {position:absolute; inset:-10% -10%; filter:blur(40px);}
.layer-1 {background: var(--bg-1); transform: translate3d(0,0,0);}
.layer-2 {background: radial-gradient(1200px circle at 10% 10%, #ffd3b3 0, transparent 60%);
  mix-blend-mode:multiply;}
.hero-content {position:relative; padding-top: 20vh;}
.reveal {opacity:0; transform: translateY(16px); will-change: opacity, transform;}
.reveal.is-visible {opacity:1; transform:none; transition:opacity .5s ease, transform .5s ease;}
.feature-card {background:#fff; border-radius:16px; padding:24px; box-shadow:0 10px 30px rgba(0,0,0,.06);
  transition: transform .2s ease, box-shadow .2s ease;}
.feature-card:hover {transform: translateY(-4px); box-shadow:0 16px 36px rgba(255,140,66,.25);}
@media (prefers-reduced-motion: reduce) {
  .reveal, .feature-card {transition:none;}
}
```

### JS (`static/js/home.js`)
- Scroll reveals & optional parallax:
```
document.addEventListener('DOMContentLoaded',()=>{
  const io = 'IntersectionObserver' in window ? new IntersectionObserver((entries)=>{
    entries.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('is-visible'); io.unobserve(e.target);} });
  },{threshold:0.15}) : null;
  document.querySelectorAll('.reveal').forEach(el=>{ if(io){ io.observe(el);} else {el.classList.add('is-visible');} });
  const layers = document.querySelectorAll('.bg-layer');
  let lastY = window.scrollY;
  window.addEventListener('scroll', ()=>{
    const y = window.scrollY; const dy = y - lastY; lastY = y;
    layers.forEach((l,i)=>{ l.style.transform = `translate3d(0,${y* (i?0.06:0.03)}px,0)`; });
  }, {passive:true});
});
```

### Optional GSAP Enhancement
- If approved, include GSAP via CDN in `base.html` and replace the simple reveal with GSAP timelines for finer control. Only added if you want more complex choreography.

## Routing & Integration
- `unirank/unirank/views.py:6` already renders `home.html`
- No backend changes needed; purely presentational

## Validation
- Visual check across mobile/tablet/desktop using responsive mode
- Lighthouse audit for performance and accessibility
- Verify `prefers-reduced-motion` behavior and keyboard navigation

## Milestones
1. Add static assets and wire up CSS/JS in `base.html`
2. Implement hero layout and parallax layers
3. Build feature cards with icons and hover states
4. Add scroll reveals and reduced‑motion support
5. Responsive tuning, accessibility pass, and performance audit

## Deliverables
- Updated `home.html` with hero and features
- New `home.css` and `home.js` optimized for 60fps
- Optional GSAP choreography (if requested)

## Notes
- No external build system required; assets loaded via Django static
- We will ensure image/video assets are optimized and lazy‑loaded where applicable
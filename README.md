# SitePulse AI — Immersive Construction Intelligence Experience

A cinematic, scroll-driven construction-tech website inspired by the visual storytelling approach of interactive 3D studios. This is an original SitePulse design, not a copy of Lusion's branding or assets.

## Run locally
1. Open this folder in VS Code.
2. In CMD:
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install -r requirements.txt
   python app.py
   ```
3. Visit http://127.0.0.1:5000

## Included
- Full-screen cinematic hero with layered construction imagery and 3D CSS building visualization
- Interactive pointer parallax, animated scan frames, scroll reveal transitions and responsive navigation
- Editorial story sections and project feature cards
- Project metrics and canvas progress chart
- Site photo upload, SQLite inspection records, engineer verification endpoint and CSV export
- Mobile responsive layouts

## Important prototype limitation
The inspection estimator in `app.py` is a demo placeholder, not computer vision. Replace it with a site-calibrated model and require human review before financial or contractual use. Project metrics are illustrative.

## External assets
Google Fonts and construction photography are loaded from external URLs. An internet connection is needed for those visual assets. The core Flask app and local interactions run locally.

## Production checklist
Add authentication, roles, project isolation, secure image storage, audit logging, CSRF protection, upload scanning, HTTPS, backups, BIM/schedule integration, and a calibrated computer-vision pipeline.

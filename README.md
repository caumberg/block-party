# Block Party modular development candidate

This is a **development-only, losslessly extracted** version of the supplied `check109.html`. The original inline style and script blocks have been moved into `css/` and `js/` in the exact original execution order. No live deployment has been performed.

## Running
Serve this folder from an HTTP server (for example `python -m http.server 8080`), then open `http://localhost:8080/`. Do not open as `file://` because browser and Android WebView resource rules differ.

## Important
The large base64-encoded embedded engine remains in one JavaScript file. This is a first safe extraction, **not yet a full semantic refactor** of engine/campaign/economy modules. The next phase should separate that engine and establish gameplay regression tests before deployment.

This package must be tested in the actual Android WebView and against the current Supabase environment before any merge to `main`.

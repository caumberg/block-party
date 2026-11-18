# Block Party modularization

Development branch only. Do not merge until runtime and Android WebView tests pass.

## First extraction
- Move inline styles into ordered CSS files.
- Move inline scripts into ordered JavaScript files.
- Preserve source execution order and game behavior.
- Keep the embedded engine intact until its dependencies can be tested.

## Acceptance tests
- Level 150 obstacle win awards stars and persists after reload.
- All campaign progress, wallet balances, and power-up selections persist.
- Arcade, versus, and campaign modes load correctly.
- Android APK/WebView resolves external assets.

The development ZIP was generated separately; it has not yet been committed to this branch.

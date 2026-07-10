# Nursing Education Platform

CAT Testing Studio is the first runnable product surface for the Harrity nursing education platform.

It is designed around three product loops:

1. Assess learners with NCLEX-aligned adaptive practice.
2. Map every response to concepts, lessons, rationales, and client-needs categories.
3. Convert missed concepts into focused remediation and educator visibility.

## Run Locally

```shell
npm run dev
```

Open `http://127.0.0.1:8765`.

No package install is required for the current prototype because the app is dependency-free HTML, CSS, and JavaScript.

## Test The CAT Engine

```shell
npm test
```

The deterministic engine test verifies the default four-item adaptive path, ability updates, session export, weak-concept detection, readiness gates, and blueprint coverage matrix.

## Current Surface

- CAT Practice: starts a four-item adaptive smoke test.
- Results: shows score, ability estimate, weak concepts, remediation, coverage, and review queue.
- Export: exposes session evidence as JSON.
- Content Map: shows item-to-concept-to-lesson mapping.
- Control Plane: shows mapping gates and blueprint category depth.

## Code Organization

- `public/index.html`: app shell, layout, and styles.
- `public/app.js`: browser UI rendering and interaction state.
- `public/cat-engine.js`: CAT selection, scoring, remediation, export, gate, and coverage logic.
- `public/data.js`: NCLEX blueprint, build path, and seeded item bank.
- `test/cat-engine.test.mjs`: deterministic engine checks.

## Product Boundary

This is a CAT-style simulator for nursing education product development. It is not an official NCLEX scoring engine.

## Next Engineering Work

- Persist sessions and learners.
- Add item exposure controls, stopping rules, and mastery thresholds.
- Add educator item authoring/import validation.
- Add cohort analytics and remediation assignment workflow.

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

## Current Surface

- CAT Practice: starts a four-item adaptive smoke test.
- Results: shows score, ability estimate, weak concepts, remediation, coverage, and review queue.
- Export: exposes session evidence as JSON.
- Content Map: shows item-to-concept-to-lesson mapping.
- Control Plane: shows mapping gates and blueprint category depth.

## Product Boundary

This is a CAT-style simulator for nursing education product development. It is not an official NCLEX scoring engine.

## Next Engineering Work

- Persist sessions and learners.
- Separate item, concept, lesson, and blueprint data into importable JSON files.
- Add item exposure controls, stopping rules, and mastery thresholds.
- Add educator item authoring/import validation.
- Add cohort analytics and remediation assignment workflow.

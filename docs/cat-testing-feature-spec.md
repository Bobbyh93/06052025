# CAT Testing Feature Specification

## Purpose

Build the CAT testing feature as the assessment engine for the Harrity nursing education platform. The feature must connect item delivery, concept diagnosis, remediation, and educator readiness controls.

## Current Prototype

The runnable prototype lives at:

- `packages/nursing-education-platform/public/index.html`

It demonstrates:

- NCLEX-RN client-needs category mapping
- CAT-style next-item selection by blueprint gap and difficulty match
- Ability estimate changes after each response
- Result summary, weak concepts, remediation plan, and review queue
- Session evidence export as JSON
- Educator gates and blueprint coverage matrix

## Required Production Entities

- `Learner`
- `CATSession`
- `CATResponse`
- `AssessmentItem`
- `Concept`
- `LearningObjective`
- `MicroLesson`
- `BlueprintCategory`
- `RemediationAssignment`
- `ItemExposureRecord`

## Item Metadata Contract

Every scored item should include:

- Stable item ID
- Status: draft, review, approved, retired
- NCLEX client-needs category
- Clinical judgment step
- Primary and secondary concept IDs
- Lesson/remediation IDs
- Difficulty estimate
- Item format
- Correct response and scoring rule
- Correct and incorrect rationales
- Misconception tags
- Source/evidence reference

## CAT Engine Requirements

The engine should:

1. Start from a learner ability estimate or diagnostic default.
2. Select only approved items eligible for the learner and session scope.
3. Avoid repeat exposure according to configured lookback rules.
4. Balance blueprint coverage against ability/difficulty match.
5. Update ability and concept-level mastery after each response.
6. Stop based on configured rules: max items, precision threshold, mastery threshold, or exhaustion of eligible pool.
7. Emit a session evidence object for analytics and educator review.

## Remediation Requirements

After each session, the system should:

- Identify missed concepts and misconception tags.
- Rank remediation by clinical risk, miss frequency, blueprint weight, and retention risk.
- Assign the smallest useful set of micro-lessons.
- Schedule targeted retest using alternate eligible items.
- Promote mastery only after successful re-demonstration.

## Educator Controls

The educator/control-plane view should show:

- Item-bank depth by NCLEX category
- Items missing concepts, lessons, rationales, or scoring metadata
- Weak/high-risk concepts by learner and cohort
- Item exposure and repeat-use warnings
- Distractor performance and item retirement candidates

## Non-Goals For The Prototype

The prototype does not claim:

- Official NCLEX scoring equivalence
- Psychometric calibration
- Secure exam delivery
- Production persistence
- LMS integration

## Next Engineering Slice

1. Move embedded sample data into JSON modules.
2. Add a typed CAT session model and deterministic selector tests.
3. Add persistent session save/load.
4. Add item exposure and repeat-item prevention.
5. Add educator item import validation.

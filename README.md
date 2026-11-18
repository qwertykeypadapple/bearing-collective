# Bearing Collective

A horizontal, auto-playing story of a federated bearing-fault experiment built on [Flower](https://flower.ai): five virtual plants learn bearing faults together without sharing raw vibration data.

Live: https://qwertykeypadapple.github.io/bearing-collective/

- Data: [CWRU Bearing Data Center](https://engineering.case.edu/bearingdatacenter) (40 official recordings, one lab rig, seeded damage).
- Results: 45 Flower 1.22 simulations, five seeds, 30 rounds each. `data.js` holds the summary numbers.
- `index.html` asks 13 simple questions; each chart is revealed as the answer.
- `story.html` is the auto-playing horizontal story; `scroll.html` is the older vertical-scroll version.
- `video-src/` renders the cover video (`python3 render.py` with the site served on port 5199).

A lab result, not field validation.

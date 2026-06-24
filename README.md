# Robits

Robits is a neon robot arena shooter — twin-stick combat with wall-crawling
and crazy gravity. Pilot your robot, equip weapons, and fight across a series
of levels, all running right in the browser with 3D graphics.

## Tech

- HTML5 + JavaScript, no build step required
- Real-time 3D rendering (Three.js) with `.glb` robot models
- Sound effects and music in `audio/`
- Level definitions in `levels/`
- Installable as a PWA via `manifest.json`

## Running it

Open `index.html` in a modern browser, or serve the folder locally:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

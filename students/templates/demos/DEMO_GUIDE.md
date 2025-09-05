
# Demo Development Guide

This guide explains how to create new physics demos for the Django-based platform.

## Structure of a Demo

Each demo consists of three core files:

1. **theory.html** – contains the theoretical explanation and is divided into scenes using <h3> headers with IDs.
2. **controls.html** – contains the interactive controls for the demo.
3. **script.js** – contains the demo logic, scene management, and animation/interaction.

## Scene System

- Each scene is defined by an `<h3 id="scene-...">` header in `theory.html`.
- Scenes automatically populate the scene selector (`<select id="scene-selector">`).
- Selecting a scene scrolls to the corresponding section and updates the active header.
- Deep linking (`#scene-X`) is supported and automatically activates the correct scene.

## How to Create a New Demo

1. Copy the `/template/` folder and rename it (e.g., `/motion-plot/`).
2. Edit `theory.html`:
   - Add your `<h2>` main title.
   - Add `<h3 id="scene-1">`, `<h3 id="scene-2">`, etc., for each scene.
3. Edit `controls.html`:
   - Place interactive elements (sliders, buttons, etc.).
4. Edit `script.js`:
   - Implement the simulation logic and connect controls.
   - Scene switching is already integrated if you use IDs like `scene-1`, `scene-2`, etc.

## Notes

- Maintain 8:5 aspect ratio for the canvas where applicable.
- The currently active scene is highlighted and bolded.
- Smooth scrolling is applied when switching scenes via selector, deep link, or header click.


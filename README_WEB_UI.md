# SpiritForge Web UI

This folder contains a static browser-based UI companion for **SpiritForge: Creature Battle Balance Simulator**.

It does not replace the Python submission. It is an extra visual interface that makes the project logic easier to demonstrate.

## How to use locally

Open `index.html` in a browser.

The app will try to load:

- `data/creatures.txt`
- `data/skills.txt`

If the browser blocks local file fetching, the app uses embedded fallback data, so it can still run.

## Recommended GitHub Pages setup

Put this entire `docs` folder in the root of your GitHub repository.

Then use GitHub Pages with:

- Branch: `main`
- Folder: `/docs`

## What the UI demonstrates

- Creature and skill database tables
- Type effectiveness chart as a multi-dimensional list
- Matchup preview
- Turn order based on speed
- Damage calculation based on attack, skill power, defense, and type multiplier
- Single battle log
- Multiple simulation balance report
- Built-in system tests

# Schedule Wallpaper

Desktop app that displays your weekly schedule as a live wallpaper using a PyQt5 controller + Flask server + React client.

## Project Structure

```
├── client/          # React (Vite) client source
├── desktop/         # PyQt5 desktop application
├── server/          # Flask backend + compiled client
├── data/            # Excel schedules, config, and images
├── main.py          # Entry point
└── requirements.txt
```

## Setup

### Python dependencies

```bash
pip install -r requirements.txt
```

### Client dependencies

```bash
cd client
npm install
```

## Build

Build the React client (outputs to `server/static/`):

```bash
cd client
npm run build
```

Then copy wallpaper images to `server/static/img/`:

```bash
# PowerShell
Copy-Item client/public/img/* server/static/img/ -Force
```

## Run

```bash
python main.py
```

Click **Init Server** in the app to start the Flask backend on `localhost:5000`.

## Features

- **Weekly schedule** displayed as a wallpaper overlay (React + Vanilla Tilt)
- **Week A / Week B** switching between two Excel schedules
- **Recycle Bin widget** — view, restore, or empty the Windows recycle bin
- **Config toggles** — blur background, show/hide trash widget, music player (AIMP)
- **Glass blur UI** — glassmorphism theme on both the desktop app and web client

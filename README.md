<div align="center">

<img src="Images/Spotify.svg" width="120" alt="Spotify Logo">

# 🎵 Spotify Live Banner

### Show off what you're jamming to, right on your GitHub profile! 🎧

![Preview](https://spotify-live-banner.vercel.app/?spin=false&scan=true&eq_color=rainbow&theme=dark)

<p>Ever wanted your GitHub profile to scream "Look at my awesome music taste!"? Well, now it can! This widget displays your current Spotify track in real-time with cool animations. It's like having a mini music player on your profile! 🎶</p>

---

[![Made with Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Flask Framework](https://img.shields.io/badge/Framework-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Uses Spotify API](https://img.shields.io/badge/API-Spotify-1DB954?style=for-the-badge&logo=spotify&logoColor=white)](https://developer.spotify.com/documentation/web-api/)
[![Last.fm](https://img.shields.io/badge/Last.fm-000000?style=for-the-badge&logo=lastdotfm&logoColor=D51007)](https://www.last.fm/api)
[![Top Language](https://img.shields.io/github/languages/top/SahooShuvranshu/Spotify-Live-Banner?style=for-the-badge&color=blueviolet)](https://github.com/SahooShuvranshu/Spotify-Live-Banner)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel%20App-0070F3.svg?style=for-the-badge&logo=vercel)](https://spotify-live-banner.vercel.app)
[![GitHub License](https://img.shields.io/badge/License-GPL--3.0-success.svg?style=for-the-badge)](https://github.com/SahooShuvranshu/Spotify-Live-Banner/blob/main/LICENSE)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/SahooShuvranshu/Spotify-Live-Banner?style=for-the-badge&logo=git&color=orange)](https://github.com/SahooShuvranshu/Spotify-Live-Banner/commits/main)

[![GitHub Stars](https://img.shields.io/github/stars/SahooShuvranshu/Spotify-Live-Banner?style=for-the-badge&color=FFD700&logo=star)](https://github.com/SahooShuvranshu/Spotify-Live-Banner/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/SahooShuvranshu/Spotify-Live-Banner?style=for-the-badge&logo=git&color=E91E63)](https://github.com/SahooShuvranshu/Spotify-Live-Banner/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/SahooShuvranshu/Spotify-Live-Banner?style=for-the-badge&logo=issue&color=red)](https://github.com/SahooShuvranshu/Spotify-Live-Banner/issues)

</div>

---

<div align="center">
   <h3>Visitors 👀:</h3>
   <img src="https://count.getloli.com/@SpotifyLiveBanner?theme=3d-num&darkmode=1" alt="Visitor Counter" />
</div>

---

### ✨ Features at a Glance

- 🎵 **Real-time Updates** - Shows what you're listening to RIGHT NOW.
- 🎨 **Premium Aesthetics** - High-end Glassmorphism, Dark mode, and Animated gradients.
- 🌈 **Adaptive Theming** - Matches banner colors to your current album art automatically.
- 🆓 **100% Free & Open Source** - Deploy on free platforms, own your data.
- ⚡ **Optimized Performance** - Pure SVG generation for zero latency and high compatibility.
- 🔒 **Privacy First** - You control your API keys and playback data.

---
<br>

<details open>

## 🚀 Quick Start & Deployment

Think of this like ordering a pizza: first you grab the ingredients, then you get your secret recipe keys, and finally, you bake it in the cloud! 🍕

<summary><b>🍕 1. Order the Ingredients (Clone Repo)</b></summary>

```bash
git clone https://github.com/SahooShuvranshu/Spotify-Live-Banner.git
cd Spotify-Live-Banner/source
```
</details>

<details open>

<summary><b>🎫 2. Get Your VIP Pass (API Keys)</b></summary>

We made it SUPER easy with a web tool!

👉 **[Get Token Here](https://spotify-refresh-token-generator.onrender.com)** 👈

Or use Last.fm:

- Visit **[Last.fm API](https://www.last.fm/api/account/create)** to get your key.
</details>

<details open>

<summary><b>🚀 3. Bake to Cloud (Deploy)</b></summary>

#### ⚡ Vercel (Recommended - Never Sleeps!)
[![Deploy to Vercel](https://img.shields.io/badge/Deploy%20to-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/new/clone?repository-url=https://github.com/SahooShuvranshu/Spotify-Live-Banner)

#### 🛤️ Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2FSahooShuvranshu%2FSpotify-Live-Banner)

#### ✨ Render
[![Deploy to Render](https://img.shields.io/badge/Deploy%20to-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/deploy?repo=https://github.com/SahooShuvranshu/Spotify-Live-Banner)
</details>

<details open>

<summary><b>🏠 Local Hosting (For Power Users)</b></summary>

Want to run it on your own machine? It's simple:
1. **Clone the Repo:**
   ```bash
   git clone https://github.com/SahooShuvranshu/Spotify-Live-Banner.git
   cd Spotify-Live-Banner/source
   ```
2. **Setup Secrets:** Create a `.env` file in the `source` folder and add your Spotify/Last.fm keys.
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Fire it up:**
   ```bash
   DEV_SERVER=1 python main.py
   ```
</details>

<br>

---

## 🎨 Personalize Your Widget

You can customize almost everything by adding parameters to your URL!

### 📋 Customization Table

| Parameter | Options | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `recently_playing` | `true`, `false` | `false` | Fallback to last track if not live. |
| `adaptive` | `true`, `false` | `false` | Match colors to album art. |
| `blur` | `true`, `false` | `false` | Blurred background effect. |
| `theme` | `light`, `dark`, `glass` | `light` | Visual aesthetic style. |
| `spin` | `true`, `false` | `false` | Vinyl record animation. |
| `eq_color` | `Hex`, `rainbow` | `1DB954` | Visualizer bar color. |

---

## 🎭 Style Gallery

Choose the look that fits your profile! Click a category to see the magic. ✨

<details open>
<summary><b>🌈 Core Aesthetics (Light, Dark, Glass)</b></summary>

```text
Default (Clean and Simple):
https://spotify-live-banner.vercel.app/
```
![Default Style](https://spotify-live-banner.vercel.app/)

```text
Midnight Mode (For Dark Theme Profiles):
https://spotify-live-banner.vercel.app/?theme=dark
```
![Dark Mode](https://spotify-live-banner.vercel.app/?theme=dark)

```text
iOS Glass (Modern Glassmorphism):
https://spotify-live-banner.vercel.app/?theme=glass
```
![Glass Mode](https://spotify-live-banner.vercel.app/?theme=glass)
</details>

<details open>
<summary><b>🧠 Intelligent Effects (Adaptive, Blur, Recent)</b></summary>

```text
Adaptive Glass (Tints to match album art):
https://spotify-live-banner.vercel.app/?theme=glass&adaptive=true
```
![Adaptive Glass](https://spotify-live-banner.vercel.app/?theme=glass&adaptive=true)

```text
Artwork Blur (Deep immersive background):
https://spotify-live-banner.vercel.app/?blur=true
```
![Blur Mode](https://spotify-live-banner.vercel.app/?blur=true)

```text
Recently Played (Never show an empty banner):
https://spotify-live-banner.vercel.app/?recently_playing=true
```
![Recently Played](https://spotify-live-banner.vercel.app/?recently_playing=true)
</details>

<details open>
<summary><b>🎨 Visual Accents (Spin, Rainbow, Scan)</b></summary>

```text
Vinyl Player (Spinning Record):
https://spotify-live-banner.vercel.app/?spin=true
```
![Spin](https://spotify-live-banner.vercel.app/?spin=true)

```text
Rainbow Visualizer (Prism Audio):
https://spotify-live-banner.vercel.app/?eq_color=rainbow
```
![Rainbow Color](https://spotify-live-banner.vercel.app/?eq_color=rainbow)

```text
Custom Hex Color (e.g. Deep Blue):
https://spotify-live-banner.vercel.app/?eq_color=0000FF
```
![Hex Color](https://spotify-live-banner.vercel.app/?eq_color=0000FF)

```text
Spotify Scan Code (Mobile Playback):
https://spotify-live-banner.vercel.app/?scan=true
```
![Scan Code](https://spotify-live-banner.vercel.app/?scan=true)
</details>

<details open>
<summary><b>🔥 Ultimate Mode (Everything enabled!)</b></summary>

```text
The Works (Spin + Scan + Dark + Rainbow):
https://spotify-live-banner.vercel.app/?spin=true&scan=true&theme=dark&eq_color=rainbow
```
![All Styles Mix](https://spotify-live-banner.vercel.app/?spin=true&scan=true&eq_color=rainbow&theme=dark)
</details>

---

## 🛠️ Integration & Usage

Ready to show off? Copy the snippets below and replace `https://your-url.com/` with your actual hosted URL.

### Markdown Snippet (Best for GitHub Profile)
```markdown
[![Listening](https://your-url.com/)](https://your-url.com/about)
```

### HTML Implementation
```html
<a href="https://your-url.com/about">
  <img src="https://your-url.com/" alt="Live Status" />
</a>
```

---

## 📁 Project Structure

```text
.
├── .github/
│   ├── CODE_OF_CONDUCT.md     # Community standards
│   ├── CONTRIBUTING.md        # How to help
│   ├── GEMINI.md              # Project memory
│   └── SECURITY.md            # Security policy
├── Images/                    # Static assets (logos)
├── source/                    # Main Application Source
│   ├── app/
│   │   ├── modules/           # Core logic (API, Parsing)
│   │   ├── static/            # Base64 static assets
│   │   └── templates/         # SVG and HTML templates
│   ├── main.py                # Entry point
│   └── requirements.txt       # App dependencies
├── app.json                   # Heroku deployment config
├── railway.json               # Railway deployment config
├── render.yaml                # Render deployment config
└── README.md                  # This beautiful file!
```

---

## 🌟 Star History

<a href="https://www.star-history.com/?repos=SahooShuvranshu%2FSpotify-Live-Banner&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=SahooShuvranshu/Spotify-Live-Banner&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=SahooShuvranshu/Spotify-Live-Banner&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=SahooShuvranshu/Spotify-Live-Banner&type=date&legend=top-left" />
 </picture>
</a>

## 🤝 Community & Support

We are growing! This project is powered by the open-source community. If you enjoy using this banner, consider giving us a star!

- **Official Email**: [connect.crystalstudio@gmail.com](mailto:connect.crystalstudio@gmail.com)
- **Discord**: Join our community for real-time help! [Invite Link](https://discord.gg/EdbUJHNv9J)
- **Issues**: Found a bug? [Report it here](https://github.com/SahooShuvranshu/Spotify-Live-Banner/issues)
- **Contribute**: Check out our [Contributing Guide](CONTRIBUTING.md)!

---

<div align="center">
  <p>&copy; 2026 SahooShuvranshu. All rights reserved.</p>
  <p>Inspired by <a href="https://github.com/tthn0/Spotify-Readme">Spotify-Readme</a> by <a href="https://github.com/tthn0">tthn0</a> 🚀</p>
  <p><i>Independent Open Source Project. Not affiliated with Spotify AB or Last.fm.</i></p>
</div>

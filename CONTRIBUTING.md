# Contributing to Spotify Live Banner

[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)
[![Open Source Love](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red.svg?style=for-the-badge)](https://github.com/SahooShuvranshu/Spotify-Live-Banner)
[![Help Wanted](https://img.shields.io/badge/Help-Wanted-blue.svg?style=for-the-badge)](https://github.com/SahooShuvranshu/Spotify-Live-Banner/issues)

First off, thank you for considering contributing to the Spotify Live Banner! It's people like you that make the open-source community such an amazing place to learn, inspire, and create. 🌟

---

## 🚀 How Can I Contribute?

### Reporting Bugs 🐛
If you find a bug, please open an issue and include:
- A clear, descriptive title.
- Steps to reproduce the bug.
- What you expected to happen vs what actually happened.
- Screenshots if applicable.

### Suggesting Enhancements ✨
We love new ideas! If you have a suggestion for a new theme, parameter, or technical optimization, please open an issue with the "enhancement" label.

### Pull Requests 🛠️
1.  **Fork** the repository and create your branch from `main`.
2.  **Install dependencies**: `pip install -r source/requirements.txt`.
3.  **Make your changes**: Ensure your code follows the project's style.
4.  **Type Checking**: We use `mypy`. Please run `cd source && mypy .` before committing.
5.  **Commit**: Use clear and concise commit messages.
6.  **Push**: Push to your fork and submit a pull request.

---

## 💻 Technical Setup

### Development Environment
```bash
git clone https://github.com/SahooShuvranshu/Spotify-Live-Banner.git
cd Spotify-Live-Banner/source
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the App
```bash
DEV_SERVER=1 python main.py
```

---

## 📜 Style Guidelines
- **Python**: Follow PEP 8. Use type hints for all functions.
- **Templates**: Keep SVG templates clean and optimized.
- **Documentation**: Update `README.md` and `about.html` if you add new features.

---

## 🏆 Recognition
Contributors who have their PRs merged will be added to our contributors list. We appreciate every bit of help!

**Happy coding!** 🎧🔥

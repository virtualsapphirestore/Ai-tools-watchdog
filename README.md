# AI Tools Watchdog 🕵️‍♂️

**Automated Daily AI Tool Reviews** powered by Google Gemini.

## About
This project runs a daily automation that:
1.  **Scouts** for trending AI tools.
2.  **Analyzes** them using Google's Gemini Pro model.
3.  **Publishes** a short, concise review to [this site](https://virtualsapphirestore.github.io/Ai-tools-watchdog/).

## How it Works
- **Scraper**: `src/scraper.py` runs daily via GitHub Actions.
- **AI**: Generates unbiased summaries and verdicts.
- **Updates**: Content is automatically appended to `index.md`.

## Credits
Maintained by [virtualsapphirestore](https://github.com/virtualsapphirestore).

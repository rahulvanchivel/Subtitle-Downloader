**Subtitle Downloader (Powered by OpenSubtitles API)
**
A Python-based CLI tool that automatically searches and downloads subtitles for any language from OpenSubtitles.com.
It’s lightweight, fast, and handles multi-episode downloads with progress tracking and error handling.

------------------------------------------------------------------------------------------------

**🧭 Features**

✅ Works for any language (English, Tamil, Czech, etc.)
✅ Uses the official OpenSubtitles API v1
✅ Downloads subtitles for multiple episodes in one go
✅ Creates an organized Subtitles/ folder automatically
✅ Built-in error handling & retry logic
✅ Command-line interface with progress bar

------------------------------------------------------------------------------------------------

⚙️ Tech Stack

| Library               | Purpose                          |
| --------------------- | -------------------------------- |
| `requests`            | API calls and subtitle downloads |
| `tqdm`                | Progress bar                     |
| `os`, `sys`, `time`   | File system & rate limiting      |
| **OpenSubtitles API** | Subtitle source                  |

------------------------------------------------------------------------------------------------

**🧩 How It Works**

Logs into your OpenSubtitles account using your API key.

Searches for subtitles in the specified language.

Downloads .srt files episode by episode.

Saves them neatly inside a Subtitles/ folder.

Displays a full summary after completion.

------------------------------------------------------------------------------------------------

**📂 Project Structure**

SubtitleDownloader/
│
├── subtitles_downloader.py     # main script
├── Subtitles/                  # created automatically
│   ├── Show_S1E1.srt
│   ├── Show_S1E2.srt
│   └── ...
└── README.md

------------------------------------------------------------------------------------------------

**🚀 How to Use**

1️⃣ Install dependencies
    pip install requests tqdm

2️⃣ Add your OpenSubtitles credentials

Edit these lines in subtitle.py:

  USERNAME = "your_username"
  PASSWORD = "your_password"
  API_KEY = "your_api_key"


You can create a free OpenSubtitles API key here:
👉 https://www.opensubtitles.com/en/consumers

------------------------------------------------------------------------------------------------

**🌍 Download Subtitles in Any Language**

By default, the script is set to Czech ("cs"):

LANGUAGE = "cs"


But you can change this line to download any language:

LANGUAGE = "en"  # English
LANGUAGE = "ta"  # Tamil
LANGUAGE = "fr"  # French
LANGUAGE = "es"  # Spanish
LANGUAGE = "de"  # German
LANGUAGE = "hi"  # Hindi


📘 You can find the full list of supported language codes here:
https://www.opensubtitles.com/docs/api/html/

------------------------------------------------------------------------------------------------

**🧠 Example Run**

=== Subtitle Downloader ===
API: OpenSubtitles.com | Language: en
Logging in to OpenSubtitles...
Login successful!
Enter TV Show Name: Breaking Bad
Enter Season Number: 1
Enter Number of Episodes: 7

**🟩 Then it begins downloading:**

Searching for Breaking Bad S1E1...
✅ Downloaded: Subtitles/Breaking Bad_S1E1.srt
Searching for Breaking Bad S1E2...
❌ No subtitles found for Episode 2

**📊 At the end:**

=== Download Summary ===
Total episodes: 7
Successfully downloaded: 6
Failed: 1
✅ Files saved to /path/to/Subtitles

------------------------------------------------------------------------------------------------

**🛠 Error Handling**

Handles invalid login or missing tokens

Gracefully skips missing subtitles

Retries on API timeouts

Waits 2 seconds between requests to avoid rate limits

------------------------------------------------------------------------------------------------

🔐 Security Tips

Don’t commit your real credentials or API key.
Instead, use environment variables:

import os
USERNAME = os.getenv("OS_USERNAME")
PASSWORD = os.getenv("OS_PASSWORD")
API_KEY = os.getenv("OS_API_KEY")

Add .env or config.json to .gitignore before pushing to GitHub.

------------------------------------------------------------------------------------------------

🧑‍💻 Author

Rahul Vanchivel
Software Developer | Automation Enthusiast
✨ “Because even subtitles deserve automation.” ✨

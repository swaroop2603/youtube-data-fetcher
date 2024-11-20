
# YouTube Data Fetcher

The **YouTube Data Fetcher** script retrieves video details and comments from a given YouTube channel using the YouTube Data API. The data is exported into an Excel file for easy analysis.

## Features

- Fetches video details (title, description, views, likes, comments, etc.) from a YouTube channel.
- Retrieves top-level comments and their replies, including metadata like author names, publish dates, and like counts.
- Exports data into a structured Excel file with separate sheets for videos and comments.

---

## Prerequisites

- Python 3.8 or later.
- A valid YouTube Data API v3 key. You can obtain one from the [Google Cloud Console](https://console.cloud.google.com/).

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/youtube-data-fetcher.git
cd youtube-data-fetcher
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Install required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

---

## Configuration

1. Create a `.env` file in the project root and add your API key:

   ```
   YOUTUBE_API_KEY=your_api_key_here
   ```

2. Ensure your API key has sufficient quota to fetch video and comment details.

---

## Usage

### 1. Run the Script

Run the `main.py` script:

```bash
python main.py
```

### 2. Outputs

- The script will create an Excel file named **YouTube_Data.xlsx** in the project directory.
- The Excel file will include:
  - **Video Data** sheet: Video details such as title, description, published date, view count, like count, etc.
  - **Comments Data** sheet: Top-level comments, replies, author names, and more.

---

## Example

Here's a sample execution:

1. The script prompts you to enter a YouTube channel URL:
   ```
   Enter the YouTube channel URL: https://www.youtube.com/@ExampleChannel
   ```

2. The script retrieves video and comment data:
   ```
   Fetching videos for channel: ExampleChannel
   Fetched 10 videos.
   Fetching comments for video: "Example Video Title" (Video ID: abc123)
   ```

3. The data is exported successfully:
   ```
   Data successfully exported to YouTube_Data.xlsx
   ```

---

## Error Handling

- If the script encounters any issues (e.g., invalid API key, missing permissions, network issues), it will log detailed error messages.
- Logs are written to `app.log` in UTF-8 format.

---

## Troubleshooting

1. **UnicodeEncodeError:**
   - If you encounter issues with special characters (e.g., emojis), ensure the logging configuration uses `UTF-8` encoding.

2. **Quota Limits:**
   - Ensure your YouTube Data API project has sufficient daily quota.

---



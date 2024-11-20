import logging
from decouple import config
from youtube_data_fetcher import YouTubeDataFetcher
from data_exporter import export_to_excel
import sys
import re

# Setup Logging
# Logs will be written to both console and a log file (app.log)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),  # Log file with UTF-8 encoding
        logging.StreamHandler(sys.stdout)                 # Console log with sys.stdout
    ]
)
def main():
    """
    Main function to fetch YouTube data and export it to an Excel file.
    """
    logging.info("Starting YouTube Data Fetcher...")

    # Load the API key from environment variables
    api_key = config("YOUTUBE_API_KEY", default=None)
    if not api_key:
        logging.error("Missing YouTube API key. Please set it in the environment variables.")
        return

    # Initialize YouTube data fetcher with the API key
    fetcher = YouTubeDataFetcher(api_key)
    # Prompt the user to input the YouTube channel URL (e.g., channel handle or URL format)
    channel_url = input("Enter the YouTube Channel URL (e.g., https://www.youtube.com/@ChannelHandle): ")
    # Validate the input URL
    if not re.match(r"^https?://(www\.)?youtube\.com/(@[a-zA-Z0-9_-]+|channel/[a-zA-Z0-9_-]+)$", channel_url):
        print("Error: Please enter a valid YouTube Channel URL (e.g., https://www.youtube.com/@ChannelHandle).")
        exit()


    # Step 1: Fetch channel details (ID and name)
    channel_details = fetcher.get_channel_details(channel_url)
    if not channel_details:
        logging.error("Failed to fetch channel details. Exiting.")
        return

    channel_id = channel_details['channel_id']
    channel_name = channel_details['channel_name']
    logging.info(f"Fetched channel details: ID = {channel_id}, Name = {channel_name}")

    # Step 2: Fetch the videos for the given channel
    videos = fetcher.fetch_videos(channel_id)
    logging.info(f"Fetched {len(videos)} videos.")

    # Step 3: Fetch comments for each video
    all_comments = []
    for video in videos:
        video_id = video['Video ID']
        logging.info(f"Fetching comments for video: {video['Title']} ({video_id})")
        comments = fetcher.fetch_comments(video_id)
        all_comments.extend(comments)  # Accumulate all comments
        logging.info(f"Fetched {len(comments)} comments for video: {video_id}")

    # Step 4: Export videos and comments to an Excel file
    output_file = f"YouTube_{channel_name}.xlsx"
    export_to_excel(videos, all_comments, filename=output_file)
    logging.info(f"Data successfully exported to {output_file}")

if __name__ == "__main__":
    main()

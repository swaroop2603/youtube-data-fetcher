import logging
from decouple import config
from src.youtube_data_fetcher import YouTubeDataFetcher
from src.data_exporter import export_to_excel
from src.utils.validators import is_valid_youtube_url
from src.utils.logger import setup_logging

def main():
    """
    Main function to fetch YouTube data and export it to an Excel file.
    """
    # Initialize logging
    setup_logging()

    logging.info("Starting YouTube Data Fetcher...")

    # Load the API key from environment variables
    api_key = config("YOUTUBE_API_KEY", default=None)
    if not api_key:
        logging.error("Missing YouTube API key. Please set it in the .env file.")
        return

    # Initialize YouTube data fetcher
    fetcher = YouTubeDataFetcher(api_key)

    # Input YouTube channel URL
    channel_url = input("Enter the YouTube Channel URL (e.g., https://www.youtube.com/@ChannelHandle): ")
    if not is_valid_youtube_url(channel_url):
        logging.error("Invalid YouTube URL. Exiting.")
        return

    # Fetch channel details
    channel_details = fetcher.get_channel_details(channel_url)
    if not channel_details:
        logging.error("Failed to fetch channel details. Exiting.")
        return

    channel_id = channel_details['channel_id']
    channel_name = channel_details['channel_name']
    logging.info(f"Fetched channel details: ID = {channel_id}, Name = {channel_name}")

    # Fetch videos
    videos = fetcher.fetch_videos(channel_id)
    logging.info(f"Fetched {len(videos)} videos.")

    # Fetch comments
    all_comments = []
    for video in videos:
        video_id = video['Video ID']
        logging.info(f"Fetching comments for video: {video['Title']} ({video_id})")
        comments = fetcher.fetch_comments(video_id)
        all_comments.extend(comments)
        logging.info(f"Fetched {len(comments)} comments for video: {video_id}")

    # Export data to Excel
    output_file = f"YouTube_{channel_name}.xlsx"
    export_to_excel(videos, all_comments, filename=output_file)
    logging.info(f"Data successfully exported to {output_file}")

if __name__ == "__main__":
    main()

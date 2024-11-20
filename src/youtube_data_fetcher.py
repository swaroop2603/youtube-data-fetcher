from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import isodate
import logging
from typing import List, Dict, Optional


class YouTubeDataFetcher:
    """
    Class to handle all interactions with the YouTube Data API.
    """

    def __init__(self, api_key: str):
        """
        Initialize the YouTube Data Fetcher.

        Args:
            api_key (str): YouTube API key for authentication.
        """
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=api_key)  # Initialize the API client

    def get_channel_details(self, handle_url: str) -> Optional[Dict[str, str]]:
        """
        Fetch the channel ID and channel name using the YouTube Data API from a channel handle (URL).

        Args:
            handle_url (str): URL of the YouTube channel.

        Returns:
            Optional[Dict[str, str]]: Dictionary containing 'channel_id' and 'channel_name' if found, else None.
        """
        try:
            # Extract handle from the URL (e.g., "@CricketMajestic1019")
            handle = handle_url.split('@')[1]
            
            # Search for the channel using the handle
            response = self.youtube.search().list(
                q=handle, part="snippet", type="channel", maxResults=1
            ).execute()

            if not response['items']:
                logging.info("No channel found for the provided handle.")
                return None

            # Extract channel ID and name
            channel_id = response['items'][0]['id']['channelId']
            channel_name = response['items'][0]['snippet']['title']

            return {"channel_id": channel_id, "channel_name": channel_name}
        except Exception as e:
            logging.error(f"Error fetching channel details: {e}")
            return None

    def fetch_videos(self, channel_id: str) -> List[Dict[str, str]]:
        """
        Fetch all videos for a given channel ID.

        Args:
            channel_id (str): YouTube channel ID.

        Returns:
            List[Dict[str, str]]: List of videos with metadata.
        """
        try:
            videos = []
            next_page_token = None

            # Paginate through all videos in the channel
            while True:
                response = self.youtube.search().list(
                    channelId=channel_id,
                    part="id,snippet",
                    maxResults=50,
                    order="date",  # Sort by newest first
                    pageToken=next_page_token
                ).execute()

                for item in response.get("items", []):
                    if item["id"]["kind"] == "youtube#video":
                        video_id = item["id"]["videoId"]
                        video_details = self.fetch_video_details(video_id)  # Fetch additional details
                        videos.append({
                            "Video ID": video_id,
                            "Title": item["snippet"]["title"],
                            "Description": item["snippet"]["description"],
                            "Published Date": item["snippet"]["publishedAt"],
                            "View Count": video_details.get("view_count"),
                            "Like Count": video_details.get("like_count"),
                            "Comment Count": video_details.get("comment_count"),
                            "Duration": self.format_iso_duration(video_details.get("duration")),
                            "Thumbnail URL": item["snippet"]["thumbnails"]["high"]["url"]
                        })

                next_page_token = response.get("nextPageToken")  # Get the token for the next page
                if not next_page_token:
                    break

            return videos
        except HttpError as e:
            logging.error(f"API error fetching videos: {e}")
            return []

    def fetch_video_details(self, video_id: str) -> Dict[str, str]:
        """
        Fetch detailed information for a single video.

        Args:
            video_id (str): YouTube video ID.

        Returns:
            Dict[str, str]: Video statistics and duration.
        """
        try:
            response = self.youtube.videos().list(
                id=video_id,
                part="statistics,contentDetails"
            ).execute()
            if not response.get('items'):
                return {}

            item = response["items"][0]
            return {
                "view_count": item["statistics"].get("viewCount", "0"),
                "like_count": item["statistics"].get("likeCount", "0"),
                "comment_count": item["statistics"].get("commentCount", "0"),
                "duration": item["contentDetails"].get("duration", "N/A")
            }
        except HttpError as e:
            logging.error(f"Error fetching video details for {video_id}: {e}")
            return {}

    def fetch_comments(self, video_id: str) -> List[Dict[str, str]]:
        """
        Fetch all comments for a given video.

        Args:
            video_id (str): YouTube video ID.

        Returns:
            List[Dict[str, str]]: List of comments with metadata.
        """
        try:
            comments = []
            next_page_token = None

            # Paginate through all comments in the video
            while True:
                response = self.youtube.commentThreads().list(
                    videoId=video_id,
                    part="snippet,replies",
                    maxResults=100,
                    pageToken=next_page_token
                ).execute()

                comments = []  # List to store all comments and replies
                comment_author_map = {}  # Dictionary to map Comment ID to Author Name

                for item in response['items']:
                    # Process top-level comment
                    top_comment = item['snippet']['topLevelComment']['snippet']
                    comment_id = item['id']
                    author_name = top_comment['authorDisplayName']

                    # Add top-level comment to the list
                    comments.append({
                        'Video Id': video_id,
                        'Comment Id': comment_id,
                        'Comment text': top_comment['textDisplay'],
                        'Author name': author_name,
                        'Published date': top_comment['publishedAt'],
                        'Like count': top_comment['likeCount'],
                        'Reply to': None
                    })

                    # Update the mapping of Comment ID to Author Name
                    comment_author_map[comment_id] = author_name

                    # Process replies if available
                    if 'replies' in item:
                        for reply in item['replies']['comments']:
                            reply_snippet = reply['snippet']
                            reply_to_id = item['id']  # Parent comment ID

                            # Add reply comment to the list
                            comments.append({
                                'Video Id': video_id,
                                'Comment Id': reply['id'],
                                'Comment text': reply_snippet['textDisplay'],
                                'Author name': reply_snippet['authorDisplayName'],
                                'Published date': reply_snippet['publishedAt'],
                                'Like count': reply_snippet['likeCount'],
                                'Reply to': comment_author_map.get(reply_to_id, "Unknown") 
                            })
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break
            return comments
        except HttpError as e:
            logging.error(f"API error fetching comments for {video_id}: {e}")
            return []

    def format_iso_duration(self, iso_duration: str) -> str:
        """
        Converts an ISO 8601 duration to a human-readable format (HH:MM:SS).

        Args:
            iso_duration (str): Duration in ISO 8601 format.

        Returns:
            str: Human-readable duration.
        """
        try:
            duration = isodate.parse_duration(iso_duration)
            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            remainder = total_seconds % 3600
            minutes = remainder // 60
            seconds = remainder % 60
            if hours > 0:
                return f"{hours:02}:{minutes:02}:{seconds:02}"
            return f"{minutes:02}:{seconds:02}"
        except Exception as e:
            logging.error(f"Error converting time: {e}")
            return "N/A"

import os
import pandas as pd
import logging
from typing import List, Dict

def export_to_excel(video_data: List[Dict[str, str]], comments_data: List[Dict[str, str]], filename: str = "YouTube_ChannelName.xlsx"):
    """
    Export video and comments data to an Excel file, stored in the 'output' folder.

    Args:
        video_data (List[Dict[str, str]]): List of video metadata.
        comments_data (List[Dict[str, str]]): List of comments metadata.
        filename (str): Output filename for the Excel file.
    """
    try:
        # Ensure the 'output' folder exists
        os.makedirs('output', exist_ok=True)
        
        # Construct the full file path
        file_path = os.path.join('output', filename)
        
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # Write videos data to the first sheet
            pd.DataFrame(video_data).to_excel(writer, index=False, sheet_name="Video Data")
            # Write comments data to the second sheet
            pd.DataFrame(comments_data).to_excel(writer, index=False, sheet_name="Comments Data")
        
        logging.info(f"Data successfully exported to {file_path}")
    except Exception as e:
        logging.error(f"Error exporting data to Excel: {e}")

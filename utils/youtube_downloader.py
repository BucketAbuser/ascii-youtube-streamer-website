import logging
import os
import tempfile

import yt_dlp

logger = logging.getLogger(__name__)

def download_youtube_video_with_metadata(yt_url, format='best'):
    """
    Download a YouTube video and extract metadata.
    """
    temp_dir = tempfile.mkdtemp()

    try:
        ydl_opts = {
            'format': format,
            'outtmpl': os.path.join(temp_dir, '%(id)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'logger': logger,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Starting download for URL: {yt_url}")
            info_dict = ydl.extract_info(yt_url, download=True)

            if not info_dict:
                raise ValueError("Error with specified video")

            metadata = {
                'title': info_dict.get('title'),
                'duration': info_dict.get('duration'),
                'view_count': info_dict.get('view_count'),
                'like_count': info_dict.get('like_count'),
            }

            video_filename = ydl.prepare_filename(info_dict)
            video_filename = os.path.abspath(video_filename)

        if not os.path.exists(video_filename):
            raise FileNotFoundError(
                f"Downloaded file not found: {video_filename}")

        file_size = os.path.getsize(video_filename)

        if file_size == 0:
            raise ValueError(f"Downloaded file is empty: {video_filename}")

        logger.info(
            f"Downloaded video to {video_filename} ({file_size} bytes)")

        return video_filename, metadata

    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        raise

    finally:
        # Clean up temporary directory if it's empty
        if os.path.exists(temp_dir) and not os.listdir(temp_dir):
            os.rmdir(temp_dir)

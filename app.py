from flask import Flask, request, Response, render_template
import logging
import os
import shutil
import time

from ascii_video.ascii_converter import AsciiVideo
from ascii_video.video_processor import extract_frames
from utils.youtube_downloader import download_youtube_video_with_metadata

app = Flask(__name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Constants
DEFAULT_WIDTH = 90
MIN_WIDTH = 20
MAX_WIDTH = 300  # Adjust as needed

HELP_MESSAGE = (
    "\nUsage:\n\n"
    "If you know the YouTube URL:\n"
    "\tcurl 'WEBSITE.COM/?yt_url=<YouTube_URL>&color=<true|false>&width=<integer>'\n\n"
    "If you want to search based on a query:\n"
    "\tcurl 'WEBSITE.COM/?yt_search=<SEARCH_QUERY>&color=<true|false>&width=<integer>'\n\n"
    "Parameters:\n"
    "- yt_url: (Optional) URL of the YouTube video to convert to ASCII.\n"
    "- search: (Optional) Search query.\n"
    "- color: (Optional) Enable color in ASCII output. Accepts 'true', '1', 'yes', 'on'. Default is 'false'.\n"
    f"- width: (Optional) Width of the ASCII video in characters. Must be an integer between {MIN_WIDTH} and {MAX_WIDTH}. Default is {DEFAULT_WIDTH}.\n\n"
)


@app.route('/')
def capture_text():
    """
    Main route for processing requests.
    """
    yt_url = request.args.get('yt_url')
    yt_search = request.args.get('yt_search')
    color_param = request.args.get('color', 'false').lower()
    width_param = request.args.get('width', str(DEFAULT_WIDTH))

    # Determine if color should be enabled
    color = color_param in ['true', '1', 'yes', 'on']

    # Parse and validate the width parameter
    try:
        video_width = int(width_param)

        if video_width < MIN_WIDTH:
            logger.warning(
                f"Specified width {video_width} is below the minimum: {MIN_WIDTH}. Setting to {MIN_WIDTH}.")
            video_width = MIN_WIDTH
            
        elif video_width > MAX_WIDTH:
            logger.warning(
                f"Specified width {video_width} is above the maximum: {MAX_WIDTH}. Setting to {MAX_WIDTH}.")
            video_width = MAX_WIDTH

    except ValueError:
        logger.warning(f"Invalid width parameter '{width_param}'. Using default width {DEFAULT_WIDTH}.")
        video_width = DEFAULT_WIDTH

    # Check if the request is from a browser or a terminal
    user_agent = request.headers.get('User-Agent', '').lower()
    is_browser = any(browser_keyword in user_agent for browser_keyword in ['mozilla', 'chrome', 'safari', 'firefox', 'edge', 'opera', 'msie'])

    # Return help message if no parameters are provided
    if not yt_url and not yt_search:
        if is_browser:
            return render_template('help.html', help_message=HELP_MESSAGE), 200

        else:
            return Response(HELP_MESSAGE, mimetype='text/plain'), 200

    if yt_url:
        try:
            video_path, video_metadata = download_youtube_video_with_metadata(yt_url)
            video_title = video_metadata.get('title', 'Untitled Video')
            video_duration = video_metadata.get('duration', 0)  # Duration in seconds

            # Extract frames
            frames = extract_frames(video_path)
            total_frames = len(frames)

            # Calculate desired frame delay based on video duration and total frames
            if total_frames > 0 and video_duration > 0:
                desired_frame_delay = video_duration / total_frames
            else:
                desired_frame_delay = 0.033333  # Approximately 30 FPS

            # Initialize AsciiVideo
            ascii_video = AsciiVideo(
                frames=frames,
                duration=video_duration,
                video_width=video_width,
                video_title=video_title,
                amount_of_frames=total_frames,
                color=color
            )

            # Generate ASCII frames
            ascii_frames = ascii_video.generate_ascii_frames()

            # Define a generator function to stream the frames with timing control to keep up with video's FPS
            def generate():
                try:
                    start_time = time.monotonic()
                    frame_index = 0

                    for ascii_frame in ascii_frames:
                        frame_index += 1
                        yield ascii_frame

                        # Calculate elapsed time since start
                        elapsed_time = time.monotonic() - start_time
                        expected_time = frame_index * desired_frame_delay
                        sleep_time = expected_time - elapsed_time

                        if sleep_time > 0:
                            time.sleep(sleep_time)

                        else:
                            pass

                finally:
                    # Cleanup temporary files
                    if os.path.exists(video_path):
                        os.remove(video_path)
                        logger.info(f"Deleted temporary file: {video_path}")

                    temp_dir = os.path.dirname(video_path)

                    if os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir)
                        logger.info(f"Deleted temporary directory: {temp_dir}")

            response = Response(generate(), mimetype='text/plain')
            return response

        except Exception as e:
            logger.error(f"Error processing video: {e}")
            return f"Error processing video: {e}", 500

    if yt_search:
        return "\n\nStill implementing this feature.\n\n"

    # For any other cases, return help message
    if is_browser:
        return render_template('help.html', help_message=HELP_MESSAGE), 200

    else:
        return Response(HELP_MESSAGE, mimetype='text/plain'), 200


@app.errorhandler(404)
def page_not_found(e):
    """
    Handler for 404 errors.
    """
    user_agent = request.headers.get('User-Agent', '').lower()
    is_browser = any(browser_keyword in user_agent for browser_keyword in [
                     'mozilla', 'chrome', 'safari', 'firefox', 'edge', 'opera', 'msie'])
    if is_browser:
        return render_template('help.html', help_message=HELP_MESSAGE), 200

    else:
        return Response(HELP_MESSAGE, mimetype='text/plain'), 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)

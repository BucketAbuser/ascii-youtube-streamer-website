# ASCII YouTube Streamer Website

## Overview

**ASCII Streamer Web** is a Flask-based web application that transforms YouTube videos into captivating ASCII art animations. By leveraging powerful libraries like OpenCV and Pillow, the application extracts frames from videos, converts them into ASCII representations, and streams them back to users in their terminals or browsers. Additionally, the platform provides a specialized API that allows users to stream ASCII videos directly using `curl` or `wget` commands with customized queries.

## Features

- **Convert YouTube Videos to ASCII Art**: Transform any YouTube video into a mesmerizing ASCII animation.
- **Color and Grayscale Modes**: Choose between vibrant color ASCII art or classic black-and-white representations.
- **Adjustable Width**: Customize the width of the ASCII output to fit your terminal or display preferences.
- **Real-time Streaming**: Stream the ASCII video with synchronized frame rates for a smooth viewing experience.
- **Progress Bar**: Visualize the playback progress with a dynamic ASCII-based progress bar.
- **API Access via `curl` and `wget`**: Stream ASCII videos directly to your terminal or other command-line tools using specialized HTTP queries.

## Project Structure

- `app.py`: Main Flask application.
- `ascii_video/`: Package containing ASCII conversion logic.
  - `ascii_converter.py`: Contains the `AsciiVideo` class for converting frames to ASCII.
  - `video_processor.py`: Extracts frames from video files.
- `utils/`: Utility functions.
  - `youtube_downloader.py`: Downloads YouTube videos and extracts metadata.
- `templates/`: HTML templates for the Flask app.
  - `help.html`: Help page displayed in browsers.
- `static/css/`: Static CSS files.
  - `style.css`: Stylesheet for the help page.
- `requirements.txt`: Python dependencies.
- `README.md`: Project documentation.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/michal-pielka/ascii-youtube-streamer-website.git
   cd ascii-youtube-streamer-website

2. **Create a Virtual Environment (Optional but Recommended)**:
    ```
    python -m venv venv
    source venv/bin/activate # On Windows, use venv/Scripts/activate
    ```

3. **Install Dependencies**:

    ```pip install -r requirements.txt```

## Usage

1. **Run the Application**:

    ```python app.py```
    
2. **Convert and Stream a YouTube Video to ASCII**:

You can interact with the application using curl / wget from the terminal. Use the **curl** or **wget** command to request an ASCII streaming of a YouTube video.

a) Using **curl**:
    curl 'http://localhost:5000/?yt_url=<YouTube_URL>&color=<true|false>&width=<integer>'

b) Using **wget**:
    wget -qO- 'http://localhost:5000/?yt_url=<YouTube_URL>&color=<true|false>&width=<integer>'

**Parameters**:

    - yt_url (Optional): The URL of the YouTube video you want to convert.

    - yt_search (Optional): Not implemented yet.

    - color (Optional): Enable color in the ASCII output. Accepts 'true', '1', 'yes', 'on'. Default is 'false'.

    - width (Optional): Change the width of the ASCII video in characters. Must be an integer between 20 and 600. Default is 90.


Examples with **curl**:

    curl 'http://localhost:5000/?yt_url=https://www.youtube.com/watch?v=dQw4w9WgXcQ'

    curl 'http://localhost:5000/?yt_url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&color=true&width=100'

3. **View Help Instructions**:

If you access the root URL without any parameters, the application will display a help message detailing how to use the service.

Example with **curl**:

    curl 'http://localhost:5000/'

4. **Stream the ASCII Video**:
    
Once you initiate the streaming using curl or wget, the ASCII video will be displayed in your terminal, synchronized with the original video's frame rate.

## Demonstration

Coming Soon: A demonstration video showcasing the ASCII YouTube Streamer Website in action.

## Configuration

1. **Adjusting Maximum, Minimum and Default Width**:

The maximum, minimum and default width can be adjusted in app.py by modifying the constants.

2. **Adjusting the Color Character**:

In ascii_video/ascii_converter.py, you can change the ASCII_COLOR_CHAR to be whatever you want. That character will then be displayed when the color parameter is true.

## Licence

This project is licenced under the MIT Licence. Feel free to use and modify it as per the licence terms.

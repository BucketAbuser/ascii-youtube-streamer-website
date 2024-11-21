import numpy as np

class AsciiVideo:
    """
    Class to convert video frames to ASCII art.
    """
    ASCII_CHARS = [".", ",", ":", ";", "+", "*", "?", "%", "S", "#", "@"]
    ASCII_COLOR_CHAR = "@"

    def __init__(self, frames, duration, video_width, video_title, amount_of_frames, color=False):
        self.frames = frames
        self.duration = duration
        self.video_width = video_width
        self.video_title = video_title
        self.color = color
        self.total_frames = amount_of_frames

        self.aspect_ratio = 1 / 1.78  # Aspect ratio of the video TODO: remove hard-coded value
        self.viewed_frames = 0

    def resize_image(self, image):
        """
        Resize the image to the specified width while maintaining aspect ratio.
        """
        new_height = int(self.aspect_ratio * self.video_width * 0.55)
        return image.resize((self.video_width, new_height))

    def grayify(self, image):
        """
        Convert image to grayscale.
        """
        return image.convert("L")

    def generate_progress_bar(self, diameter_percentage = 0.04):
        """
        Generate a progress bar to display in the ASCII art.
        """
        diameter = max(2, int(self.video_width * diameter_percentage))
        progress_bars = [[" " for _ in range(self.video_width)] for _ in range(diameter)]
        progress_ratio = self.viewed_frames / self.total_frames
        progress_ratio = max(0, min(progress_ratio, 1))  # Clamp between 0 and 1

        ball_middle_x = 1 + int(progress_ratio * (self.video_width - 3))
        radius = diameter // 2

        # Draw the ball as a circle in the progress bar
        for ball_x in range(max(0, ball_middle_x - radius), min(self.video_width, ball_middle_x + radius + 1)):
            for ball_y in range(diameter):
                if ((ball_y - radius) ** 2) + ((ball_x - ball_middle_x) ** 2) <= radius ** 2:
                    if self.color:
                        progress_bars[ball_y][ball_x] = f"\033[38;2;255;0;0m{self.ASCII_COLOR_CHAR}\033[0m"

                    else:
                        progress_bars[ball_y][ball_x] = "@"

        # Convert progress bars to a string with newlines
        progress_bar_str = "\n".join(["".join(row) for row in progress_bars][::-1])

        return progress_bar_str

    def pixels_to_ascii(self, image):
        """
        Convert image pixels to ASCII characters.
        """
        if self.color:
            pixels = np.array(image)
            height, width, _ = pixels.shape

            # Flatten the pixel array
            pixels_flat = pixels.reshape(-1, 3)

            # Use list comprehension to create ANSI codes for all pixels
            ascii_char = self.ASCII_COLOR_CHAR
            ansi_codes = [f"\033[38;2;{r};{g};{b}m{ascii_char}" for r, g, b in pixels_flat]

            # Reset ANSI codes after each line
            reset_code = "\033[0m"

            # Reconstruct the lines
            lines = [''.join(ansi_codes[i * width:(i + 1) * width]) + reset_code for i in range(height)]

            ascii_str = '\n'.join(lines)

        else:
            gray_image = self.grayify(image)
            pixels = np.array(gray_image)

            # Use list comprehension and join for efficiency
            ascii_str = '\n'.join(
                ''.join(self.ASCII_CHARS[pixel // 25] for pixel in row)
                for row in pixels
            )

        # Generate progress bar and video title
        progress_bar = self.generate_progress_bar()

        if self.color:
            progress_bar = "\033[37m" + progress_bar + "\033[0m"

        # Append progress bar and video title to the ASCII string
        ascii_str += "\n" + progress_bar + "\n\n\n"
        ascii_str += f"\n\033[1m{self.video_title}\033[0m\n"

        return ascii_str

    def generate_ascii_frames(self):
        """
        Generator function to yield ASCII frames.
        """
        for frame in self.frames:
            self.viewed_frames += 1

            # Resize and process frame
            image = self.resize_image(frame)

            if self.color:
                # In color mode, retain RGB
                processed_image = image

            else:
                # In grayscale mode, convert to grayscale
                processed_image = self.grayify(image)

            ascii_frame = self.pixels_to_ascii(processed_image)

            # Clear screen and move cursor to top-left
            ascii_frame_with_escapes = "\033[2J\033[H" + ascii_frame

            yield ascii_frame_with_escapes

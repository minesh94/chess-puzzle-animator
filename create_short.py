from moviepy import VideoFileClip, ImageClip, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
import os

def create_puzzle_short(input_video_path, bg_music_path, output_path="output/puzzle_short.mp4"):
    """
    Generates a YouTube Short with a static chess puzzle position, text overlay, and music.

    Args:
        input_video_path (str): The path to the existing vertical video (e.g., final_puzzle_9x16.mp4).
        bg_music_path (str): The path to the background music file (e.g., music/bg_music.mp3).
        output_path (str): The desired path for the final video file.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 1. Extract the first frame as a static image clip
    initial_video = VideoFileClip(input_video_path)
    static_board = initial_video.to_ImageClip(t=0).with_duration(15)  # Set duration to 15 seconds

    # 2. Create the text overlays
    text_color = "white"
    text1_content = "Solve this puzzle"
    text2_content = "Black to move"
    text3_content = "Solution in comments"

    # Set font size and position
    # The text is positioned in the black bars above and below the chess board
    text1 = TextClip(text1_content, color=text_color).with_position(("center", 150)).with_duration(15)
    text2 = TextClip(text2_content, color=text_color).with_position(("center", 250)).with_duration(15)
    text3 = TextClip(text3_content, color=text_color).with_position(("center", static_board.h - 100)).with_duration(15)

    # 3. Add background music
    if os.path.exists(bg_music_path):
        bg_music = AudioFileClip(bg_music_path).subclipped(0, static_board.duration).volumex(0.2)
        final_audio = CompositeAudioClip([bg_music])
        final_video = static_board.with_audio(final_audio)
    else:
        final_video = static_board

    # 4. Composite the video and text clips
    final_clip = CompositeVideoClip([final_video, text1, text2, text3])

    # 5. Write the final video file
    final_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

    # Close clips to free up resources
    initial_video.close()
    final_video.close()
    final_clip.close()

# Example usage:
# Assuming your video is named final_puzzle_9x16.mp4 and your music is in a music folder.
create_puzzle_short("./output/final_puzzle_9x16.mp4", "./music/bg_music.mp3")
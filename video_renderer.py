import os
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip, ColorClip, CompositeVideoClip
from moviepy.audio.fx.MultiplyVolume import MultiplyVolume
from moviepy.video.fx.Crop import Crop  # Ensure this points to your Crop class file

def merge_video_audio(
    manim_path,
    audio_path,
    out_path="output/final_puzzle.mp4",
    bg_music_path="music/bg_music.mp3",
    out_square="output/final_puzzle_square.mp4",
    out_vertical="output/final_puzzle_9x16.mp4"
):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Load video and audio
    video = VideoFileClip(manim_path)
    narration = AudioFileClip(audio_path)

    # Freeze last frame if audio is longer
    if narration.duration > video.duration:
        freeze_duration = narration.duration - video.duration
        last_frame = video.to_ImageClip(t=video.duration - 0.05).with_duration(freeze_duration)
        video = concatenate_videoclips([video, last_frame])
    else:
        narration = narration.subclipped(0, video.duration)

    # Combine narration + background music (optional)
    audio_clips = [narration]
    if os.path.exists(bg_music_path):
        bg_music_clip = AudioFileClip(bg_music_path).subclipped(0, video.duration)
        bg_music = bg_music_clip.with_effects([MultiplyVolume(0.2)])
        audio_clips.insert(0, bg_music)

    final_audio = CompositeAudioClip(audio_clips)
    video_with_audio = video.with_audio(final_audio)

    # --- 1. Standard horizontal video ---
    video_with_audio.write_videofile(out_path, codec="libx264", audio_codec="aac")

    # --- 2. Square (1:1) video ---
    square_size = 1080
    resized = video_with_audio.resized(height=square_size)
    square_video = resized.with_effects([
        Crop(width=square_size, x_center=resized.w / 2)
    ])
    square_video.write_videofile(out_square, codec="libx264", audio_codec="aac")

    # --- 3. Vertical (9:16) short using square centered ---
    target_width = 1080
    target_height = 1920

    background = ColorClip((target_width, target_height), color=(0, 0, 0)).with_duration(square_video.duration)
    centered = square_video.with_position("center").with_audio(final_audio)
    final_vertical = CompositeVideoClip([background, centered])
    final_vertical.write_videofile(out_vertical, codec="libx264", audio_codec="aac")

    # Cleanup
    video.close()
    narration.close()
    final_audio.close()
    video_with_audio.close()
    square_video.close()
    final_vertical.close()

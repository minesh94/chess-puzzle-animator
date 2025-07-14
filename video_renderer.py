from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip, ColorClip, CompositeVideoClip
from moviepy.audio.fx.MultiplyVolume import MultiplyVolume

import os

def merge_video_audio(manim_path, audio_path, out_path="output/final_puzzle.mp4", bg_music_path="music/bg_music.mp3", out_vertical="output/final_puzzle_9x16.mp4"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    video = VideoFileClip(manim_path)
    narration = AudioFileClip(audio_path)

    if narration.duration > video.duration:
        freeze_duration = narration.duration - video.duration
        last_frame = video.to_ImageClip(t=video.duration - 0.05).with_duration(freeze_duration)
        video = concatenate_videoclips([video, last_frame])
    else:
        narration = narration.subclipped(0, video.duration)

    audio_clips = [narration]

    if os.path.exists(bg_music_path):
        bg_music_clip = AudioFileClip(bg_music_path).subclipped(0, video.duration)
        bg_music = bg_music_clip.with_effects([MultiplyVolume(0.2)])
        audio_clips.insert(0, bg_music)

    final_audio = CompositeAudioClip(audio_clips)
    final_video = video.with_audio(final_audio)

    final_video.write_videofile(out_path, codec="libx264", audio_codec="aac")

    target_width = 1080
    target_height = 1920

    resized_video = video.resized(width=target_width)
    background = ColorClip((target_width, target_height), color=(0, 0, 0)).with_duration(resized_video.duration)
    centered_video = resized_video.with_position("center").with_audio(final_audio)

    final_vertical = CompositeVideoClip([background, centered_video])
    final_vertical.write_videofile(out_vertical, codec="libx264", audio_codec="aac")

    video.close()
    narration.close()
    final_audio.close()
    final_video.close()
    final_vertical.close()

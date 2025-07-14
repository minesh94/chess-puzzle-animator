# composer.py

from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip
import os

def compose_video(
    animation_path="media/videos/board_renderer/480p15/animation.mp4",
    narration_path="audio/narration.mp3",
    music_path="music/bg_music.mp3",
    output_path="final_chess_puzzle_video.mp4"
):
    video = VideoFileClip(animation_path)
    narration = AudioFileClip(narration_path).volumex(1.1)
    music = AudioFileClip(music_path).volumex(0.2).set_duration(video.duration)
    audio = CompositeAudioClip([music, narration])
    video = video.set_audio(audio)
    os.makedirs("video", exist_ok=True)
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")

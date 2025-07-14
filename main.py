# main.py

import subprocess
import os
from fetch_daily_puzzle import fetch_and_save_daily_puzzle
from narration_generator import generate_narration
from puzzle_config import puzzle_data
from video_renderer import merge_video_audio

def render_manim():
    subprocess.run([
        "manim",
        "board_renderer.py",
        "ChessPuzzleScene",
        "-qh",  # Quality: High
        "--output_file", "puzzle_raw.mp4",
        "--media_dir", "output"
    ], check=True)

def find_rendered_video():
    for root, _, files in os.walk("output"):
        for f in files:
            if f.endswith("puzzle_raw.mp4"):
                return os.path.join(root, f)
    raise FileNotFoundError("Rendered video not found.")

def main():
    print("📥 Fetching puzzle...")
    fetch_and_save_daily_puzzle()

    print("🔊 Generating narration...")
    narration = generate_narration(
        puzzle_data["initial_fen"], puzzle_data["solution_moves"]
    )
    for line in narration:
        print("📢", line)

    print("🎬 Rendering board animation...")
    render_manim()

    print("🎞 Merging video + narration...")
    video_path = find_rendered_video()
    merge_video_audio(video_path, "output/narration.mp3", "output/final_puzzle.mp4")

    print("✅ Done! Check: output/final_puzzle.mp4")

if __name__ == "__main__":
    main()

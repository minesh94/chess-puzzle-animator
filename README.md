# Chess Puzzle Animator

A Python project that fetches the daily puzzle from [Lichess.org](https://lichess.org), animates the moves using [Manim](https://www.manim.community/), narrates the solution, and generates final videos in both landscape (16:9) and vertical (9:16) formats.

---

## Features

- Automatically fetches the daily Lichess puzzle
- Renders an animated chessboard using Manim
- Generates voice narration using TTS
- Merges animation with audio narration
- Outputs both 16:9 and 9:16 videos
- Includes metadata like puzzle ID and rating

---

## 🧰 Requirements

- Python 3.10 or later
- `manim`
- `moviepy`
- `python-chess`
- TTS package (e.g. `edge-tts`, `gTTS`, or `elevenlabs`)

You can install all dependencies using:

```bash
pip install -r requirements.txt
```

Folder Structure


chess_puzzle/
├── main.py
├── board_renderer.py
├── fetch_daily_puzzle.py
├── narration_generator.py
├── video_renderer.py
├── puzzle_config.py
├── assets/
│   └── pieces/             # Contains SVG pieces like wK.svg, bQ.svg, etc.
├── output/
│   └── final_puzzle.mp4    # Rendered 16:9 video
│   └── final_puzzle_9x16.mp4  # Rendered 9:16 vertical video
├── requirements.txt
└── README.md

Usage
To run the full pipeline and generate both videos:

python main.py
This will:

Fetch the puzzle

Generate narration

Render the board animation

Merge animation with narration

Output two videos to output/

Customization
Edit puzzle_config.py to hardcode your own puzzle

Replace assets/pieces/ with your preferred chess piece designs

Modify narration_generator.py to use different TTS voices

Add background music by placing a track in the music/ folder

Sample Output
Landscape (16:9)	Vertical (9:16)
output/final_puzzle.mp4	output/final_puzzle_9x16.mp4

Inspiration
Inspired by the daily Lichess puzzles and the goal of making engaging, narrated chess content programmatically.

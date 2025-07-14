import os
import cairosvg

input_dir = "assets/pieces"
output_dir = "assets/pieces/png"
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".svg"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".svg", ".png"))
        cairosvg.svg2png(url=input_path, write_to=output_path, output_width=128, output_height=128)

print("✅ Conversion complete!")

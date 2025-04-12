from cairosvg import svg2png
from PIL import Image
import io

# First convert SVG to PNG using CairoSVG
with open('icon.svg', 'rb') as svg_file:
    svg_data = svg_file.read()

# Create different size PNG images
sizes = [16, 32, 48, 64, 128, 256]
icons = []

for size in sizes:
    png_data = svg2png(bytestring=svg_data, output_width=size, output_height=size)
    icon_image = Image.open(io.BytesIO(png_data))
    icons.append(icon_image)

# Save as ICO file with multiple sizes
icons[0].save('icon.ico', format='ICO', sizes=[(size, size) for size in sizes], append_images=icons[1:])
print('Icon converted successfully!')
from PIL import Image, ImageDraw

# Create images for different sizes
sizes = [16, 32, 48, 64, 128, 256]
icons = []

for size in sizes:
    # Create a new image with a white background
    image = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw a simple 'G' letter in blue
    draw.rectangle([0, 0, size-1, size-1], outline='#0366d6')
    draw.text((size/4, size/4), 'G', fill='#0366d6', size=int(size/2))
    
    icons.append(image)

# Save as ICO file
icons[0].save('icon.ico', format='ICO', sizes=[(size, size) for size in sizes], append_images=icons[1:])
print('Icon generated successfully!')
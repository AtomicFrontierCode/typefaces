import matplotlib.font_manager as fm
from PIL import Image, ImageDraw, ImageFont
import os

beginSaving = 0

# List of fonts to process
# Get a list of all font paths
font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')

# Use a dictionary to store font paths and names to avoid duplicates
font_dict = {}
for font in font_list:
    try:
        font_name = fm.FontProperties(fname=font).get_name()
        font_properties = fm.FontProperties(fname=font)
        if 'italic' not in font_properties.get_style():
            font_dict[font] = font_name
    except RuntimeError:
        continue

# Create a directory to save the images if it doesn't exist
os.makedirs('fontImages', exist_ok=True)

# Print the list of fonts and create an image for each font
i = 1
old_font = ""
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for font_path, font_name in sorted(font_dict.items(), key=lambda item: item[1]):
    if font_name != old_font:
        old_font = font_name
        try:
            if i > beginSaving:
                for letter in letters:
                    print(f"{font_name}\t{letter}")
                    
                    # Set text size based on font name
                    text_size = 2500
                    if font_name == "Amiri Quran":
                        text_size = 1000
                    if font_name == "Meddon":
                        text_size = 1000
                    if font_name == "Miama":
                        text_size = 1000

                    # Create a new image with a white background
                    img = Image.new('RGB', (5000, 5000), color='white')
                    d = ImageDraw.Draw(img)
                    
                    # Load the font and draw the letter
                    font = ImageFont.truetype(font_path, text_size)
                    text = letter
                    
                    # Calculate the position to center the text using textbbox
                    text_bbox = d.textbbox((0, 0), text, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    position = ((5000 - text_width) // 2, (5000 - text_height) // 2)
                    
                    # Draw the text on the image
                    d.text(position, text, font=font, fill=(0, 0, 0))
                    
                    # Crop the image
                    pixels = img.load()

                    # Get image dimensions
                    width, height = img.size

                    # Initialize crop boundaries
                    left = width
                    right = 0
                    top = height
                    bottom = 0

                    # Find the boundaries of the black pixels
                    for y in range(height):
                        for x in range(width):
                            if pixels[x, y] == (0, 0, 0):  # Assuming black pixels are (0, 0, 0)
                                if x < left:
                                    left = x
                                if x > right:
                                    right = x
                                if y < top:
                                    top = y
                                if y > bottom:
                                    bottom = y

                    # Check if valid black pixels were found
                    if left < right and top < bottom:
                        # Determine the side length of the square crop
                        crop_width = right - left + 1
                        crop_height = bottom - top + 1
                        side_length = max(crop_width, crop_height)

                        # Calculate new boundaries for the square crop
                        center_x = (left + right) // 2
                        center_y = (top + bottom) // 2

                        new_left = max(0, center_x - side_length // 2)
                        new_right = min(width, center_x + side_length // 2 + (side_length % 2))
                        new_top = max(0, center_y - side_length // 2)
                        new_bottom = min(height, center_y + side_length // 2 + (side_length % 2))

                        # Crop the image
                        cropped_img = img.crop((new_left, new_top, new_right, new_bottom))
                        bwImage = cropped_img.convert('1')
                        
                        # Resize the cropped image to 1000x1000 pixels
                        resized_img = bwImage.resize((1000, 1000), Image.BICUBIC)
                        
                        # Save the image
                        resized_img.save(f'fontImages/{font_name}_{letter}.png')
                
            i += 1
        except Exception as e:
            print(f"Could not process font: {font_path}, Error: {e}")
            continue

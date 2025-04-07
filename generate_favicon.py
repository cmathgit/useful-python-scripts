# Import the Image module from the Pillow library
from PIL import Image
import os # Import os module for path joining if needed

# --- Configuration ---
# Specify the path to your input JPG image
input_image_filename = 'github-logo.png'
# Specify the desired output path for the favicon
output_favicon_filename = 'favicon.ico'
# Define the standard icon sizes required for a multi-resolution .ico file
# Browsers and systems will pick the best size automatically.
icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
# --- End Configuration ---

# Construct full paths (assuming the script and image are in the same directory)
# If they are in different directories, adjust current_dir or provide absolute paths.
current_dir = os.path.dirname(os.path.abspath(__file__))
input_image_path = os.path.join(current_dir, input_image_filename)
output_favicon_path = os.path.join(current_dir, output_favicon_filename)

try:
    # Step 1: Load the source JPG image
    print(f"Loading image from: {input_image_path}")
    img = Image.open(input_image_path)

    # Step 2: Ensure image is in RGBA format if transparency might be desired
    # (JPG doesn't have transparency, but converting ensures consistency)
    # If the source image has transparency (like a PNG), this preserves it.
    # If it's JPG, it adds an alpha channel where everything is opaque.
    # This step might not be strictly necessary if you know the source is opaque,
    # but it's often safer for icon generation.
    img = img.convert("RGBA")

    # Step 3: Save the image as a multi-resolution ICO file
    # The .save() method for the ICO format handles the resizing internally
    # when provided with the 'sizes' argument. It typically uses a
    # high-quality resampling filter like LANCZOS.
    print(f"Saving favicon to: {output_favicon_path} with sizes: {icon_sizes}")
    img.save(output_favicon_path, format='ICO', sizes=icon_sizes)

    print("-" * 30)
    print(f"Successfully generated '{output_favicon_filename}' from '{input_image_filename}'.")
    print(f"Favicon saved at: {output_favicon_path}")
    print("-" * 30)

except FileNotFoundError:
    print(f"Error: Input image not found at '{input_image_path}'")
    print("Please ensure the image file exists and the path is correct.")
except ImportError:
    print("Error: Pillow library not found.")
    print("Please install it using: pip install Pillow")
except Exception as e:
    # Catch other potential errors during image processing or saving
    print(f"An unexpected error occurred: {e}")

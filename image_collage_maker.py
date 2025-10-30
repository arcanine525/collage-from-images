from PIL import Image
import os
from datetime import datetime
import random
from typing import Tuple, List
import math
from pillow_heif import register_heif_opener
from PIL import ImageDraw, ImageFilter, ImageFont
import requests
from io import BytesIO
import urllib.parse
import imageio

# Import grid layouts and configuration
from grid_layouts import GRID_LAYOUTS, DEFAULT_LAYOUT_CONFIG
from config import STYLE_PRESETS, DIMENSIONS

# Register HEIF opener to support HEIC images
register_heif_opener()

class CollageGenerator:
    def __init__(self, images_dir: str, output_dir: str):
        self.images_dir = images_dir
        self.output_dir = output_dir
        self.used_images = set()
        self.style_presets = STYLE_PRESETS  # Use imported style presets

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def get_dimension_choice(self) -> Tuple[int, int]:
        print("\nChoose output dimension format:")

        # Display dimension options
        for idx, (name, dims) in enumerate(DIMENSIONS.items(), 1):
            print(f"{idx}. {name} ({dims[0]}x{dims[1]})")

        print(f"{len(DIMENSIONS) + 1}. Custom dimensions")

        while True:
            choice = input(f"Enter your choice (1-{len(DIMENSIONS) + 1}): ")

            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(DIMENSIONS):
                    # Return selected preset dimension
                    return list(DIMENSIONS.values())[choice_idx]
                elif choice_idx == len(DIMENSIONS):
                    # Custom dimensions
                    try:
                        width = int(input("Enter width in pixels: "))
                        height = int(input("Enter height in pixels: "))

                        # Basic validation
                        if width <= 0 or height <= 0:
                            print("Dimensions must be positive integers. Please try again.")
                            continue

                        # Optional: Add an upper limit to prevent excessive memory usage
                        if width > 10000 or height > 10000:
                            confirm = input("Large dimensions may require significant memory. Continue? (y/n): ")
                            if confirm.lower() != 'y':
                                continue

                        return (width, height)
                    except ValueError:
                        print("Invalid input. Please enter numeric values for dimensions.")
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def get_available_images(self) -> List[str]:
        """Get list of unused image files from images directory"""
        all_images = [f for f in os.listdir(self.images_dir)
                     if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.heic'))]
        return [img for img in all_images if img not in self.used_images]

    def create_collages(self, image_urls: List[str]):
        dimensions = self.get_dimension_choice()
        available_images = image_urls  # Use the provided image URLs directly

        while available_images:
            # Take up to 6 images for each collage
            collage_images = available_images[:6]
            self.create_single_collage(collage_images, dimensions)

            # Mark these images as used
            for img in collage_images:
                self.used_images.add(img)

            # Update available images
            available_images = [img for img in image_urls if img not in self.used_images]

    def get_style_choice(self) -> dict:
        print("\nChoose style preset:")
        for idx, style in enumerate(self.style_presets.keys(), 1):
            print(f"{idx}. {style.title()}")

        while True:
            choice = input("Enter your choice (1-3): ")
            try:
                style_name = list(self.style_presets.keys())[int(choice)-1]
                return self.style_presets[style_name]
            except (ValueError, IndexError):
                print("Invalid choice. Please try again.")

    def create_single_collage(self, image_files: List[str], dimensions: Tuple[int, int], title=None):
        base_width, base_height = dimensions
        style = self.get_style_choice()

        # Create background with transparency if selected
        if style['background_color'] == 'transparent':
            background = Image.new('RGBA', dimensions, (0, 0, 0, 0))  # Fully transparent
        else:
            background = Image.new('RGBA', dimensions, style['background_color'])

        # Add subtle gradient overlay only if background is not transparent
        if style['background_color'] != 'transparent':
            gradient = self.create_gradient_overlay(dimensions, style['background_color'])
            background = Image.alpha_composite(background, gradient)

        n_images = len(image_files)
        border_size = style['border_size']

        # Use imported grid layouts
        layout_config = random.choice(GRID_LAYOUTS.get(n_images, [DEFAULT_LAYOUT_CONFIG]))
        grid = layout_config["layout"]
        layout_name = layout_config["name"]
        layout_description = layout_config["description"]

        print(f"Using layout: {layout_name} - {layout_description}")

        # Adjust grid if we have fewer images than the layout expects
        grid = grid[:n_images]

        # Process each image with enhanced styling
        for idx, (image_file, (x_ratio, y_ratio, w_ratio, h_ratio)) in enumerate(zip(image_files, grid)):
            # Calculate actual pixel coordinates
            x = int(x_ratio * base_width)
            y = int(y_ratio * base_height)
            w = int(w_ratio * base_width) - (2 * border_size)
            h = int(h_ratio * base_height) - (2 * border_size)

            # Load image from file path
            try:
                img = Image.open(image_file)
            except Exception as e:
                print(f"Error loading image from path {image_file}: {e}")
                continue

            # Calculate aspect ratios
            img_aspect = img.width / img.height
            target_aspect = w / h

            # Determine if we need to scale down (only scale if image is larger than cell)
            scale_needed = img.width > w or img.height > h

            if scale_needed:
                # Only scale down, preserving aspect ratio
                if img.width / w > img.height / h:
                    # Width is the limiting factor
                    scale_factor = w / img.width
                else:
                    # Height is the limiting factor
                    scale_factor = h / img.height

                # Resize using the calculated scale factor
                new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Apply style effects
            if style['shadow']:
                img = self.add_drop_shadow(img, opacity=40)

            # Add border with style color
            if style['border_size'] > 0:
                img = self.add_border(img, style['border_size'], style['border_color'])

            # Apply rotation based on style preset
            rotation = random.uniform(*style['rotation_range'])
            img = img.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)

            # Calculate new position after rotation
            paste_x = x + (w - img.width) // 2
            paste_y = y + (h - img.height) // 2

            # Create mask for smooth edges
            mask = Image.new('L', img.size, 255)

            # Paste with rotation and transparency
            background.paste(img, (paste_x, paste_y), mask)

        # Add text overlay if provided
        if title:
            background = self.add_text_to_collage(background, title)

        # Update the save operation to use PNG for transparency support
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Use PNG for transparent backgrounds, JPEG otherwise
        if style['background_color'] == 'transparent':
            output_path = os.path.join(self.output_dir, f"collage_{timestamp}.png")
            background.save(output_path, format='PNG')
        else:
            output_path = os.path.join(self.output_dir, f"collage_{timestamp}.jpg")
            # Convert to RGB before saving as JPEG
            background_rgb = background.convert('RGB')
            background_rgb.save(output_path)

        print(f"Created collage: {output_path}")

        # Generate a default title if none provided
        if title is None:
            title = f"Photo Collage - {datetime.now().strftime('%B %d, %Y')}"

        # Convert collage to HTML with title
        self.convert_collage_to_html(
            image_files,
            dimensions,
            grid,
            style,
            output_name=f"collage_{timestamp}",
            title=title
        )

    def create_animated_collage(self, image_files: List[str], dimensions: Tuple[int, int], title: str = "Animated Collage", num_frames: int = 10, duration: float = 0.5):
        """Creates an animated collage (GIF or MP4) from a list of images."""
        style = self.get_style_choice()
        output_format = self.get_animation_format_choice()

        frames = []
        for _ in range(num_frames):
            # Create a single frame of the collage
            frame = self.create_single_collage_frame(image_files, dimensions, style)
            frames.append(frame)

        # Save the animated collage
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if output_format == 'gif':
            output_path = os.path.join(self.output_dir, f"animated_collage_{timestamp}.gif")
            imageio.mimsave(output_path, frames, duration=duration)
        else: # mp4
            output_path = os.path.join(self.output_dir, f"animated_collage_{timestamp}.mp4")
            imageio.mimwrite(output_path, frames, fps=1/duration)

        print(f"Created animated collage: {output_path}")

    def get_animation_format_choice(self) -> str:
        """Lets the user choose the animation output format."""
        print("\nChoose animation format:")
        print("1. GIF")
        print("2. MP4")
        while True:
            choice = input("Enter your choice (1-2): ")
            if choice == '1':
                return 'gif'
            elif choice == '2':
                return 'mp4'
            else:
                print("Invalid choice. Please try again.")

    def add_text_to_collage(self, collage_image: Image, text: str, font_size: int = 50, font_color: str = "white", position: Tuple[int, int] = (10, 10)):
        """Adds text overlay to a collage image."""
        draw = ImageDraw.Draw(collage_image)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        draw.text(position, text, font=font, fill=font_color)
        return collage_image

    def create_single_collage_frame(self, image_files: List[str], dimensions: Tuple[int, int], style: dict) -> Image:
        """Creates a single frame for an animated collage."""
        base_width, base_height = dimensions
        if style['background_color'] == 'transparent':
            background = Image.new('RGBA', dimensions, (0, 0, 0, 0))
        else:
            background = Image.new('RGBA', dimensions, style['background_color'])

        if style['background_color'] != 'transparent':
            gradient = self.create_gradient_overlay(dimensions, style['background_color'])
            background = Image.alpha_composite(background, gradient)

        n_images = len(image_files)
        border_size = style['border_size']
        layout_config = random.choice(GRID_LAYOUTS.get(n_images, [DEFAULT_LAYOUT_CONFIG]))
        grid = layout_config["layout"]
        grid = grid[:n_images]

        for idx, (image_file, (x_ratio, y_ratio, w_ratio, h_ratio)) in enumerate(zip(image_files, grid)):
            x = int(x_ratio * base_width)
            y = int(y_ratio * base_height)
            w = int(w_ratio * base_width) - (2 * border_size)
            h = int(h_ratio * base_height) - (2 * border_size)

            if image_file.startswith(('http://', 'https://')):
                try:
                    response = requests.get(image_file, stream=True)
                    response.raise_for_status()
                    img = Image.open(BytesIO(response.content))
                except Exception as e:
                    print(f"Error loading image from URL {image_file}: {e}")
                    continue
            else:
                img_path = os.path.join(self.images_dir, image_file) if self.images_dir else image_file
                try:
                    img = Image.open(img_path)
                except Exception as e:
                    print(f"Error loading image from path {img_path}: {e}")
                    continue

            scale_needed = img.width > w or img.height > h
            if scale_needed:
                if img.width / w > img.height / h:
                    scale_factor = w / img.width
                else:
                    scale_factor = h / img.height
                new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            if style['shadow']:
                img = self.add_drop_shadow(img, opacity=40)
            if style['border_size'] > 0:
                img = self.add_border(img, style['border_size'], style['border_color'])

            rotation = random.uniform(*style['rotation_range'])
            img = img.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)

            paste_x = x + (w - img.width) // 2
            paste_y = y + (h - img.height) // 2
            mask = Image.new('L', img.size, 255)
            background.paste(img, (paste_x, paste_y), mask)

        return background.convert('RGB')

    def convert_collage_to_html(self, image_files: List[str], dimensions: Tuple[int, int],
                               grid: List[Tuple], style: dict, output_name: str = None, title: str = "Image Collage"):
        base_width, base_height = dimensions
        border_size = style.get('border_size', 0)

        # Create HTML content
        html = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '    <meta charset="UTF-8">',
            f'    <title>{title}</title>',
            '    <style>',
            '        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; text-align: center; }',
            f'        h1 {{ margin-bottom: 20px; }}',
        ]

        # Handle transparent background in CSS
        if style["background_color"] == 'transparent':
            html.append(f'        .collage-container {{ position: relative; width: {base_width}px; height: {base_height}px; background-color: transparent; margin: 0 auto; overflow: hidden; }}')
        else:
            html.append(f'        .collage-container {{ position: relative; width: {base_width}px; height: {base_height}px; background-color: {style["background_color"]}; margin: 0 auto; overflow: hidden; }}')

        html.extend([
            '        .collage-image { position: absolute; box-sizing: border-box; }',
            '    </style>',
            '</head>',
            '<body>',
            f'    <h1>{title}</h1>',
            '    <div class="collage-container">'
        ])

        # Add each image
        for idx, (image_file, (x_ratio, y_ratio, w_ratio, h_ratio)) in enumerate(zip(image_files, grid)):
            # Calculate actual pixel coordinates
            x = int(x_ratio * base_width)
            y = int(y_ratio * base_height)
            w = int(w_ratio * base_width) - (2 * border_size)
            h = int(h_ratio * base_height) - (2 * border_size)

            # Calculate rotation
            rotation = random.uniform(*style['rotation_range'])

            # Create inline CSS for the image
            image_style = [
                f"left: {x}px",
                f"top: {y}px",
                f"width: {w}px",
                f"height: {h}px",
                f"transform: rotate({rotation}deg)",
                f"object-fit: contain"
            ]

            # Add border if specified
            if style['border_size'] > 0:
                image_style.append(f"border: {style['border_size']}px solid {style['border_color']}")

            # Add shadow if enabled
            if style.get('shadow', False):
                # image_style.append("box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.3)")
                pass

            # Determine image source path
            if image_file.startswith(('http://', 'https://')):
                # Use the URL directly
                img_src = image_file
            else:
                # For local files, use relative path
                img_src = os.path.join("../images", image_file)

            # Add image element to HTML
            html.append(f'        <img class="collage-image" src="{img_src}" alt="Collage image {idx+1}" style="{"; ".join(image_style)}">')

        # Close HTML
        html.extend([
            '    </div>',
            '</body>',
            '</html>'
        ])

        # Save HTML file
        if output_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"collage_{timestamp}"

        html_path = os.path.join(self.output_dir, f"{output_name}.html")
        with open(html_path, 'w') as f:
            f.write('\n'.join(html))

        print(f"Created HTML collage: {html_path}")
        return html_path

    @staticmethod
    def rectangles_overlap(rect1, rect2):
        """Check if two rectangles overlap"""
        x1, y1, x2, y2 = rect1
        x3, y3, x4, y4 = rect2
        return not (x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1)

    @staticmethod
    def create_gradient_overlay(dimensions: Tuple[int, int], base_color: str) -> Image:
        """Create a subtle gradient overlay"""
        # Skip gradient for transparent backgrounds
        if base_color == 'transparent':
            return Image.new('RGBA', dimensions, (0, 0, 0, 0))

        gradient = Image.new('RGBA', dimensions, (0, 0, 0, 0))
        draw = ImageDraw.Draw(gradient)

        # Create subtle diagonal gradient
        for i in range(dimensions[1]):
            alpha = int(255 * (1 - i/dimensions[1]) * 0.1)  # 10% maximum opacity
            draw.line([(0, i), (dimensions[0], i)],
                     fill=(255, 255, 255, alpha))
        return gradient

    @staticmethod
    def add_drop_shadow(image: Image, opacity: int = 40) -> Image:
        """Add subtle drop shadow to image"""
        shadow = Image.new('RGBA', image.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rectangle([(2, 2), (image.size[0]-2, image.size[1]-2)],
                            fill=(0, 0, 0, opacity))
        shadow = shadow.filter(ImageFilter.GaussianBlur(3))

        result = Image.new('RGBA', image.size, (0, 0, 0, 0))
        result.paste(shadow, (4, 4))
        result.paste(image, (0, 0), image if image.mode == 'RGBA' else None)
        return result

    @staticmethod
    def add_border(image: Image, border_size: int, border_color: str) -> Image:
        """Add border to image with specified size and color"""
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        bordered = Image.new('RGBA',
                           (image.width + 2*border_size,
                            image.height + 2*border_size),
                           border_color)
        bordered.paste(image, (border_size, border_size),
                      image if image.mode == 'RGBA' else None)
        return bordered

def main():
    # Set up directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'collages')

    # Example image URLs
    image_urls = [
        "https://storage.googleapis.com/banner-genius-assets-test/dist/public/Daisy.png",
        "https://storage.googleapis.com/banner-genius-assets-test/dist/public/Gidget.png",
        "https://storage.googleapis.com/banner-genius-assets-test/dist/public/Max.png",
        "https://storage.googleapis.com/banner-genius-assets-test/dist/public/chloe.png",
        "https://storage.googleapis.com/banner-genius-assets-test/dist/public/hamster.png"
    ]

    # Create generator
    generator = CollageGenerator(images_dir=None, output_dir=output_dir)

    # Ask user for collage type
    print("\nChoose collage type:")
    print("1. Static Collage")
    print("2. Animated Collage")
    while True:
        choice = input("Enter your choice (1-2): ")
        if choice == '1':
            generator.create_collages(image_urls)
            break
        elif choice == '2':
            dimensions = generator.get_dimension_choice()
            generator.create_animated_collage(image_urls, dimensions)
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
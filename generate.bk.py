from PIL import Image
import os
from datetime import datetime
import random
from typing import Tuple, List
import math
from pillow_heif import register_heif_opener
from PIL import ImageDraw, ImageFilter

# Register HEIF opener to support HEIC images
register_heif_opener()

class CollageGenerator:
    def __init__(self, images_dir: str, output_dir: str):
        self.images_dir = images_dir
        self.output_dir = output_dir
        self.used_images = set()

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Add new style parameters
        self.style_presets = {
            'modern': {
                'background_color': 'white',
                'rotation_range': (-3, 3),
                'border_size': 4,
                'spacing': 0.02,  # 2% spacing between images
                'shadow': True,
                'border_color': 'white'
            },
            'vintage': {
                'background_color': '#F5E6D3',
                'rotation_range': (-8, 8),
                'border_size': 6,
                'spacing': 0.04,  # 4% spacing for vintage look
                'shadow': True,
                'border_color': '#FFFFFF'
            },
            'minimal': {
                'background_color': 'black',
                'rotation_range': (0, 0),
                'border_size': 2,
                'spacing': 0.01,  # 1% minimal spacing
                'shadow': False,
                'border_color': 'black'
            },
            'polaroid': {
                'background_color': '#EFEFEF',
                'rotation_range': (-5, 5),
                'border_size': 12,
                'spacing': 0.05,
                'shadow': True,
                'border_color': 'white'
            },
            'neon': {
                'background_color': '#121212',
                'rotation_range': (0, 0),
                'border_size': 5,
                'spacing': 0.03,
                'shadow': True,
                'border_color': '#00FFAA'  # Bright neon green
            },
            'retro': {
                'background_color': '#D4B483',  # Warm tan
                'rotation_range': (-4, 4),
                'border_size': 7,
                'spacing': 0.04,
                'shadow': True,
                'border_color': '#C1440E'  # Burnt orange
            },
            'elegant': {
                'background_color': '#2C3639',  # Dark slate
                'rotation_range': (0, 0),
                'border_size': 4,
                'spacing': 0.02,
                'shadow': True,
                'border_color': '#DBA53A'  # Gold accent
            },
            'scrapbook': {
                'background_color': '#F3EFE0',  # Cream paper
                'rotation_range': (-10, 10),
                'border_size': 0,
                'spacing': 0.06,  # More space between images
                'shadow': True,
                'border_color': 'white'
            }
        }

    def get_dimension_choice(self) -> Tuple[int, int]:
        print("\nChoose output dimension format:")
        print("1. 16:9 (1920x1080)")
        print("2. Square (1200x1200)")
        print("3. 9:16 (1080x1920)")
        print("4. Custom dimensions")

        while True:
            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                return (1920, 1080)
            elif choice == '2':
                return (1200, 1200)
            elif choice == '3':
                return (1080, 1920)
            elif choice == '4':
                return (768, 1024)

            elif choice == '5':
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

    def get_available_images(self) -> List[str]:
        """Get list of unused image files from images directory"""
        all_images = [f for f in os.listdir(self.images_dir)
                     if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.heic'))]
        return [img for img in all_images if img not in self.used_images]

    def create_collages(self):
        dimensions = self.get_dimension_choice()
        available_images = self.get_available_images()

        while available_images:
            # Take up to 6 images for each collage
            collage_images = available_images[:6]
            self.create_single_collage(collage_images, dimensions)

            # Mark these images as used
            for img in collage_images:
                self.used_images.add(img)

            # Update available images
            available_images = self.get_available_images()

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

        # Create background with chosen style
        background = Image.new('RGB', dimensions, style['background_color'])

        # Add subtle gradient overlay
        gradient = self.create_gradient_overlay(dimensions, style['background_color'])
        background = Image.alpha_composite(background.convert('RGBA'), gradient)

        n_images = len(image_files)
        border_size = 3
        max_empty_space = 0.06  # 6% maximum empty space allowed
        rotation_range = (-5, 5)  # Rotation range in degrees

        # Define flexible grid layouts with multiple options for each count
        grid_options = {
            1: [
                # Standard centered
                [(0.1, 0.1, 0.8, 0.8)],
                # Full bleed
                [(0.02, 0.02, 0.96, 0.96)],
                # Offset to right
                [(0.3, 0.1, 0.6, 0.8)]
            ],
            2: [
                # Side by side (horizontal)
                [(0.05, 0.1, 0.45, 0.8), (0.5, 0.1, 0.45, 0.8)],
                # Stacked (vertical)
                [(0.1, 0.05, 0.8, 0.45), (0.1, 0.5, 0.8, 0.45)],
                # Diagonal arrangement
                [(0.05, 0.05, 0.5, 0.5), (0.45, 0.45, 0.5, 0.5)],
                # Asymmetric split
                [(0.05, 0.1, 0.6, 0.8), (0.65, 0.2, 0.3, 0.6)]
            ],
            3: [
                # Original layout
                [(0.05, 0.1, 0.6, 0.8), (0.67, 0.1, 0.28, 0.38), (0.67, 0.52, 0.28, 0.38)],
                # Triangle arrangement
                [(0.5 - 0.4, 0.1, 0.8, 0.45), (0.1, 0.55, 0.38, 0.4), (0.52, 0.55, 0.38, 0.4)],
                # Row strip
                [(0.03, 0.25, 0.31, 0.5), (0.35, 0.25, 0.31, 0.5), (0.67, 0.25, 0.31, 0.5)],
                # L-shaped
                [(0.05, 0.05, 0.45, 0.45), (0.05, 0.5, 0.45, 0.45), (0.5, 0.05, 0.45, 0.9)]
            ],
            4: [
                # Grid (2x2)
                [(0.05, 0.05, 0.45, 0.45), (0.5, 0.05, 0.45, 0.45),
                 (0.05, 0.5, 0.45, 0.45), (0.5, 0.5, 0.45, 0.45)],
                # Row of 4
                [(0.02, 0.3, 0.23, 0.4), (0.27, 0.3, 0.23, 0.4),
                 (0.52, 0.3, 0.23, 0.4), (0.77, 0.3, 0.23, 0.4)],
                # 3+1 arrangement
                [(0.05, 0.05, 0.65, 0.9), (0.7, 0.05, 0.25, 0.28),
                 (0.7, 0.35, 0.25, 0.28), (0.7, 0.65, 0.25, 0.28)],
                # Diamond pattern
                [(0.5-0.2, 0.05, 0.4, 0.4), (0.05, 0.5-0.2, 0.4, 0.4),
                 (0.55, 0.5-0.2, 0.4, 0.4), (0.5-0.2, 0.55, 0.4, 0.4)]
            ],
            5: [
                # Original layout
                [(0.05, 0.05, 0.6, 0.6), (0.67, 0.05, 0.28, 0.29), (0.67, 0.36, 0.28, 0.29),
                 (0.05, 0.67, 0.29, 0.28), (0.36, 0.67, 0.29, 0.28)],
                # Cross arrangement
                [(0.5-0.15, 0.05, 0.3, 0.3), (0.05, 0.5-0.15, 0.3, 0.3), (0.5-0.15, 0.5-0.15, 0.3, 0.3),
                 (0.65, 0.5-0.15, 0.3, 0.3), (0.5-0.15, 0.65, 0.3, 0.3)],
                # Scattered arrangement
                [(0.05, 0.05, 0.35, 0.35), (0.6, 0.1, 0.3, 0.3), (0.15, 0.45, 0.25, 0.25),
                 (0.5, 0.5, 0.4, 0.4), (0.1, 0.75, 0.35, 0.2)],
                # Central focus with satellites
                [(0.3, 0.3, 0.4, 0.4), (0.05, 0.05, 0.25, 0.25), (0.7, 0.05, 0.25, 0.25),
                 (0.05, 0.7, 0.25, 0.25), (0.7, 0.7, 0.25, 0.25)]
            ],
            6: [
                # Original layout
                [(0.05, 0.05, 0.45, 0.45), (0.52, 0.05, 0.43, 0.45), (0.05, 0.52, 0.28, 0.43),
                 (0.35, 0.52, 0.28, 0.43), (0.65, 0.52, 0.28, 0.43), (0.52, 0.05, 0.43, 0.45)],
                # 2x3 grid
                [(0.05, 0.05, 0.3, 0.45), (0.35, 0.05, 0.3, 0.45), (0.65, 0.05, 0.3, 0.45),
                 (0.05, 0.5, 0.3, 0.45), (0.35, 0.5, 0.3, 0.45), (0.65, 0.5, 0.3, 0.45)],
                # 3x2 grid
                [(0.05, 0.05, 0.3, 0.3), (0.35, 0.05, 0.3, 0.3), (0.65, 0.05, 0.3, 0.3),
                 (0.05, 0.35, 0.3, 0.3), (0.35, 0.35, 0.3, 0.3), (0.65, 0.35, 0.3, 0.3)],
                # Circular arrangement
                [(0.5-0.2, 0.1, 0.4, 0.4), (0.7, 0.3, 0.25, 0.25), (0.6, 0.65, 0.25, 0.25),
                 (0.3, 0.65, 0.25, 0.25), (0.05, 0.3, 0.25, 0.25), (0.3, 0.05, 0.25, 0.25)]
            ]
        }

        # Random layout selection based on number of images
        layout_options = grid_options.get(n_images, [grid_options[1][0]])  # Default to centered layout
        grid = random.choice(layout_options)

        # Adjust grid if we have fewer images than the layout expects
        grid = grid[:n_images]

        # Process each image with enhanced styling
        for idx, (image_file, (x_ratio, y_ratio, w_ratio, h_ratio)) in enumerate(zip(image_files, grid)):
            # Rest of the existing image processing code...
            # Calculate actual pixel coordinates with slight randomization
            x = int(x_ratio * base_width)
            y = int(y_ratio * base_height)
            w = int(w_ratio * base_width) - (2 * border_size)
            h = int(h_ratio * base_height) - (2 * border_size)

            # Load image
            img_path = os.path.join(self.images_dir, image_file)
            img = Image.open(img_path)

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

        # Save collage
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"collage_{timestamp}.jpg")
        # Convert to RGB before saving as JPEG
        if background.mode == 'RGBA':
            background = background.convert('RGB')
        background.save(output_path)
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

    def convert_collage_to_html(self, image_files: List[str], dimensions: Tuple[int, int],
                               grid: List[Tuple], style: dict, output_name: str = None, title: str = "Image Collage"):
        """
        Generate HTML representation of the collage with each image as a separate element.

        Args:
            image_files: List of image files used in the collage
            dimensions: Width and height of the collage
            grid: List of position tuples (x_ratio, y_ratio, w_ratio, h_ratio)
            style: Style dictionary with formatting parameters
            output_name: Base name for the output file (without extension)
            title: Title for the HTML page and displayed heading
        """
        base_width, base_height = dimensions
        border_size = style.get('border_size', 3)

        # Create HTML content
        html = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '    <meta charset="UTF-8">',
            f'    <title>{title}</title>',
            '    <style>',
            '        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; text-align: center; }',
            f'        h1 {{ color: {style["border_color"]}; margin-bottom: 20px; }}',
            f'        .collage-container {{ position: relative; width: {base_width}px; height: {base_height}px; background-color: {style["background_color"]}; margin: 0 auto; overflow: hidden; }}',
            '        .collage-image { position: absolute; box-sizing: border-box; }',
            '    </style>',
            '</head>',
            '<body>',
            f'    <h1>{title}</h1>',
            '    <div class="collage-container">'
        ]

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
                image_style.append("box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.3)")

            # Create relative path to image
            rel_path = os.path.join("../images", image_file)

            # Add image element to HTML
            html.append(f'        <img class="collage-image" src="{rel_path}" alt="Collage image {idx+1}" style="{"; ".join(image_style)}">')

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
    images_dir = os.path.join(script_dir, 'images')
    output_dir = os.path.join(script_dir, 'collages')

    # Create generator and make collages
    generator = CollageGenerator(images_dir, output_dir)
    generator.create_collages()

if __name__ == "__main__":
    main()

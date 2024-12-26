from PIL import Image
import os
from typing import List, Tuple, Dict
import random
from datetime import datetime

class SmartCollageGenerator:
    def __init__(self, images_dir: str):
        self.images_dir = images_dir
        self.image_orientations = {}  # Store image orientations
        
    def analyze_images(self) -> Dict[str, str]:
        """Analyze all images and classify them as horizontal or vertical"""
        orientations = {}
        for img_file in os.listdir(self.images_dir):
            if img_file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.heic')):
                img_path = os.path.join(self.images_dir, img_file)
                with Image.open(img_path) as img:
                    width, height = img.size
                    aspect_ratio = width / height
                    orientations[img_file] = 'horizontal' if aspect_ratio > 1.1 else (
                        'vertical' if aspect_ratio < 0.9 else 'square')
        return orientations

    def get_layout_for_square(self, n_images: int, orientations: Dict[str, str]) -> List[Tuple[float, float, float, float]]:
        """Generate optimal layout for square canvas based on image count and orientations"""
        # Default spacing and border
        spacing = 0.02
        border = 0.01  # 1% border
        
        if n_images == 6:
            # Main layout for 6 images with optimized layout
            return [
                # Main large image (2/3 width x 2/3 height) at top
                (spacing, spacing, 0.67-spacing, 0.67-spacing),
                
                # Right side column (1/3 width) divided into 2 equal parts
                (0.67+spacing, spacing, 0.33-spacing*2, 0.335-spacing),           # Top right
                (0.67+spacing, 0.335+spacing, 0.33-spacing*2, 0.335-spacing),     # Middle right
                
                # Bottom row (1/3 height)
                (spacing, 0.67+spacing, 0.335-spacing, 0.33-spacing*2),           # Bottom left
                (0.335+spacing, 0.67+spacing, 0.335-spacing, 0.33-spacing*2),     # Bottom middle
                (0.67+spacing, 0.67+spacing, 0.33-spacing*2, 0.33-spacing*2)      # Bottom right
            ]
        
        # Add more layouts for different image counts here
        return []

    def create_collage(self, output_size: Tuple[int, int], n_images: int):
        """Create a collage based on image analysis"""
        # Analyze available images
        orientations = self.analyze_images()
        print("\nImage Analysis:")
        print(f"Total images: {len(orientations)}")
        print(f"Horizontal: {sum(1 for o in orientations.values() if o == 'horizontal')}")
        print(f"Vertical: {sum(1 for o in orientations.values() if o == 'vertical')}")
        print(f"Square: {sum(1 for o in orientations.values() if o == 'square')}")
        
        # Get layout
        layout = self.get_layout_for_square(n_images, orientations)
        if not layout:
            print("No suitable layout found for this configuration")
            return
        
        # Create canvas with black background
        canvas = Image.new('RGB', output_size, 'black')
        
        # Select images based on orientation for optimal placement
        selected_images = list(orientations.keys())[:n_images]
        
        # Place images according to layout with rotation
        for idx, (img_file, (x, y, w, h)) in enumerate(zip(selected_images, layout)):
            img_path = os.path.join(self.images_dir, img_file)
            with Image.open(img_path) as img:
                # Calculate target dimensions
                target_w = int(w * output_size[0])
                target_h = int(h * output_size[1])
                
                # Add white border
                border_size = 5  # 5 pixels border
                img_with_border = Image.new('RGB', (img.width + 2*border_size, img.height + 2*border_size), 'white')
                img_with_border.paste(img, (border_size, border_size))
                img = img_with_border
                
                # Resize maintaining aspect ratio
                img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
                
                # Apply rotation (including main image, but with smaller angle)
                if idx == 0:  # Main image gets slight rotation
                    rotation = random.uniform(-2, 2)  # Random rotation between -2 and 2 degrees
                else:  # Other images get more rotation
                    rotation = random.uniform(-4, 4)  # Random rotation between -4 and 4 degrees
                img = img.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
                
                # Calculate paste position
                paste_x = int(x * output_size[0])
                paste_y = int(y * output_size[1])
                
                # Center the image in its allocated space
                paste_x += (target_w - img.width) // 2
                paste_y += (target_h - img.height) // 2
                
                # Create mask for smooth edges
                mask = Image.new('L', img.size, 255)
                
                # Paste with rotation and transparency
                canvas.paste(img, (paste_x, paste_y), mask)
        
        # Save collage with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        canvas.save(f'smart_collage_{timestamp}.jpg', quality=95)
        print(f"\nCollage created successfully as smart_collage_{timestamp}.jpg!")

def main():
    # Initialize
    images_dir = 'images'
    if not os.path.exists(images_dir):
        print("Please create an 'images' directory and add your images.")
        return
    
    generator = SmartCollageGenerator(images_dir)
    
    # Get user input
    print("\nAnalyzing images...")
    orientations = generator.analyze_images()
    
    if not orientations:
        print("No images found in the images directory!")
        return
    
    print(f"\nFound {len(orientations)} images")
    while True:
        try:
            n_images = int(input("\nHow many images do you want to use (2-6)? "))
            if 2 <= n_images <= 6:
                break
            print("Please enter a number between 2 and 6")
        except ValueError:
            print("Please enter a valid number")
    
    # Create square collage
    output_size = (1200, 1200)
    generator.create_collage(output_size, n_images)

if __name__ == "__main__":
    main()

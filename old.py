from PIL import Image
import os
from datetime import datetime
import random
from typing import Tuple, List
import math
from pillow_heif import register_heif_opener

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
    
    def get_dimension_choice(self) -> Tuple[int, int]:
        print("\nChoose output dimension format:")
        print("1. 16:9 (1920x1080)")
        print("2. Square (1200x1200)")
        print("3. 9:16 (1080x1920)")
        
        while True:
            choice = input("Enter your choice (1-3): ")
            if choice == '1':
                return (1920, 1080)
            elif choice == '2':
                return (1200, 1200)
            elif choice == '3':
                return (1080, 1920)
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
    
    def create_single_collage(self, image_files: List[str], dimensions: Tuple[int, int]):
        base_width, base_height = dimensions
        background = Image.new('RGB', dimensions, 'black')
        
        n_images = len(image_files)
        border_size = 3
        max_empty_space = 0.06  # 6% maximum empty space allowed
        rotation_range = (-5, 5)  # Rotation range in degrees
        
        # Define flexible grid layouts
        if n_images == 1:
            grid = [(0.1, 0.1, 0.8, 0.8)]  # Centered with margin
        elif n_images == 2:
            grid = [
                (0.05, 0.1, 0.45, 0.8),    # Left
                (0.5, 0.1, 0.45, 0.8)      # Right
            ]
        elif n_images == 3:
            grid = [
                (0.05, 0.1, 0.6, 0.8),     # Left large
                (0.67, 0.1, 0.28, 0.38),   # Top right
                (0.67, 0.52, 0.28, 0.38)   # Bottom right
            ]
        elif n_images == 4:
            grid = [
                (0.05, 0.05, 0.45, 0.45),  # Top left
                (0.5, 0.05, 0.45, 0.45),   # Top right
                (0.05, 0.5, 0.45, 0.45),   # Bottom left
                (0.5, 0.5, 0.45, 0.45)     # Bottom right
            ]
        elif n_images == 5:
            grid = [
                (0.05, 0.05, 0.6, 0.6),    # Large top left
                (0.67, 0.05, 0.28, 0.29),  # Top right
                (0.67, 0.36, 0.28, 0.29),  # Middle right
                (0.05, 0.67, 0.29, 0.28),  # Bottom left
                (0.36, 0.67, 0.29, 0.28)   # Bottom right
            ]
        else:  # 6 images
            grid = [
                (0.05, 0.05, 0.45, 0.45),  # Top left
                (0.52, 0.05, 0.43, 0.45),  # Top right
                (0.05, 0.52, 0.28, 0.43),  # Bottom left
                (0.35, 0.52, 0.28, 0.43),  # Bottom middle
                (0.65, 0.52, 0.28, 0.43),  # Bottom right
                (0.52, 0.05, 0.43, 0.45)   # Overlapping top right
            ]

        # Process each image according to grid layout
        for idx, (image_file, (x_ratio, y_ratio, w_ratio, h_ratio)) in enumerate(zip(image_files, grid)):
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
            
            # Resize image maintaining aspect ratio without cropping
            if img_aspect > target_aspect:
                # Image is wider - fit to height
                new_height = h
                new_width = int(h * img_aspect)
                scale_factor = h / img.height
            else:
                # Image is taller - fit to width
                new_width = w
                new_height = int(w / img_aspect)
                scale_factor = w / img.width
            
            # Resize using the calculated scale factor
            new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Add rotation for visual interest
            rotation = random.uniform(rotation_range[0], rotation_range[1])
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
        background.save(output_path, quality=95)
        print(f"Created collage: {output_path}")
    
    @staticmethod
    def rectangles_overlap(rect1, rect2):
        """Check if two rectangles overlap"""
        x1, y1, x2, y2 = rect1
        x3, y3, x4, y4 = rect2
        return not (x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1)

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
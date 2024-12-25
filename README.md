# Image Collage Maker

A Python-based collage generator that creates beautiful, automatically arranged collages from your images. Supports multiple image formats including HEIC/HEIF files.

## Features

- Supports multiple image formats (JPEG, PNG, WebP, HEIC/HEIF)
- Creates collages with up to 9 images
- Instagram-style grid layout for 7-9 images
- Multiple aspect ratio options (16:9, Square, 9:16)
- Intelligent image placement with slight rotations for visual interest
- Face detection to avoid overlapping faces in images
- Random image shuffling for unique collages every time
- Maintains original image aspect ratios (no cropping)
- Automatic multiple collage creation if more images are available
- Clean borders and spacing
- Supports up to 6% empty space for optimal layout
- Automatic timestamp-based naming for output files

## Requirements
```bash
pip install Pillow
pip install pillow-heif
pip install opencv-python
```

## Directory Structure

```bash
project_folder/
├── image_collage_maker.py
├── images/ # Put your source images here
│ ├── image1.jpg
│ ├── image2.heic
│ └── ...
└── collages/ # Output collages will be saved here
├── collage_20240321_123456.jpg
```

## Usage

1. Create an `images` directory in the same folder as the script
2. Place your source images in the `images` directory
3. Run the script:
   ```bash
   python image_collage_maker.py
   ```
4. Choose your desired output dimensions:
   - Option 1: 16:9 (1920x1080)
   - Option 2: Square (1200x1200)
   - Option 3: 9:16 (1080x1920)

The script will automatically:
- Create collages using up to 6 images each
- Save them in the `collages` directory
- Create multiple collages if more images are available
- Never reuse the same image twice

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- HEIC/HEIF (.heic)

## Features in Detail

### Layout Options
- 1 image: Centered with margins
- 2 images: Side-by-side layout
- 3 images: Large left + 2 stacked right
- 4 images: Grid layout
- 5 images: Large main + 4 smaller
- 6 images: Balanced grid with slight overlap
- 7-9 images: Instagram-style 3x3 grid

### Image Processing
- Maintains original aspect ratios
- No cropping of images
- Slight random rotation (-5° to +5°)
- Smooth edges with transparency
- Black background for better aesthetics
- Minimal borders between images

## Notes

- HEIC support requires the `pillow-heif` package
- On Windows, additional dependencies might be needed for HEIC support
- Images are never cropped, only resized to fit
- Each collage is uniquely named with a timestamp
- The script automatically creates the output directory if it doesn't exist

## Version History

### v2.0.0 (Latest)
New Features:
- Added style presets (Modern, Vintage, Minimal)
- Added gradient overlay effects
- Added drop shadow support
- Enhanced border customization
- Added style-specific rotation ranges
- Added customizable spacing between images
- Added style-specific background colors
- Improved image blending with transparency support
- Added smooth edge rendering

Style Presets:
1. Modern
   - Clean white background
   - Subtle rotation (-3° to 3°)
   - Thin white borders
   - Minimal spacing (2%)
   - Drop shadows enabled

2. Vintage
   - Warm beige background
   - More pronounced rotation (-8° to 8°)
   - Thicker white borders
   - Wider spacing (4%)
   - Drop shadows enabled

3. Minimal
   - Black background
   - No rotation
   - Very thin borders
   - Minimal spacing (1%)
   - No drop shadows

Technical Improvements:
- Added RGBA to RGB conversion for JPEG output
- Improved image placement algorithm
- Added gradient overlay for enhanced visual depth
- Enhanced border rendering with transparency support
- Added drop shadow effect with customizable opacity

### v1.0.0 (Base Version)
Initial features as documented in the main section above:
- Basic collage creation
- Multiple format support (JPEG, PNG, WebP, HEIC)
- Simple grid-based layouts
- Basic rotation effects
- Basic border support
- Multiple aspect ratio options

## License

MIT License

## Contributing

Feel free to open issues or submit pull requests for improvements.

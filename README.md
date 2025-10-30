# Image Collage Maker

A Python-based collage generator that creates beautiful, automatically arranged collages from your images. Supports multiple image formats, a command-line interface, and a web UI.

## Features

- **Multiple Image Formats:** Supports JPEG, PNG, WebP, and HEIC/HEIF.
- **Web UI:** Interactive interface for uploading images and generating collages.
- **Command-Line Interface:** For terminal-based collage generation.
- **Animated Collages:** Create GIF or MP4 collages.
- **HTML Export:** Export collages as HTML files.
- **Customizable Styles:** Choose from a variety of style presets.
- **Customizable Dimensions:** Choose from a variety of aspect ratios or specify custom dimensions.
- **Intelligent Layouts:** Automatically arranges images in a variety of layouts.
- **Image Effects:** Add borders, shadows, and rotations to your images.

## Requirements
```bash
pip install Pillow pillow-heif requests imageio imageio-ffmpeg Flask
```

## Directory Structure

```bash
project_folder/
├── app.py
├── image_collage_maker.py
├── config.py
├── grid_layouts.py
├── templates/
│   └── index.html
├── images/ # Put your source images here
│   ├── image1.jpg
│   └── ...
└── collages/ # Output collages will be saved here
    ├── collage_20240321_123456.jpg
```

## Web UI Usage

1. **Run the Flask app:**
   ```bash
   python3 app.py
   ```
2. **Open your browser:**
   Navigate to `http://127.0.0.1:5000`.
3. **Upload images:**
   Click the "Choose Files" button and select the images you want to include in your collage.
4. **Generate collage:**
   Click the "Generate Collage" button. The generated collage will be displayed on the page.

## Command-Line Usage

1. **Run the script:**
   ```bash
   python3 image_collage_maker.py
   ```
2. **Choose collage type:**
   - Option 1: Static Collage
   - Option 2: Animated Collage
3. **Choose output dimensions:**
   - Select a preset aspect ratio or enter custom dimensions.
4. **Choose a style:**
   - Select a style preset from the list.

The script will automatically create a collage and save it in the `collages` directory.

## License

MIT License

## Contributing

Feel free to open issues or submit pull requests for improvements.

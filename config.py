"""Configuration file for the collage generator.

This file contains presets for styles and dimensions.
- DIMENSIONS: A dictionary of predefined aspect ratios and their corresponding pixel dimensions.
- STYLE_PRESETS: A dictionary of style presets, each with its own set of visual options.
"""

# Available dimensions with name and pixel values
DIMENSIONS = {
    "16:9": (1920, 1080),
    "Square": (1200, 1200),
    "9:16": (1080, 1920),
    "iPad": (768, 1024)
}

# Style presets with various visual options
STYLE_PRESETS = {
    'modern': {
        'background_color': 'transparent',  # Original: white
        'rotation_range': (-3, 3),
        'border_size': 0,  # Changed from 4 to 0
        'spacing': 0.02,  # 2% spacing between images
        'shadow': True,
        'border_color': 'white'
    },
    'vintage': {
        'background_color': 'transparent',  # Original: #F5E6D3
        'rotation_range': (-8, 8),
        'border_size': 0,  # Changed from 6 to 0
        'spacing': 0.04,  # 4% spacing for vintage look
        'shadow': True,
        'border_color': 'white'
    },
    'minimal': {
        'background_color': 'transparent',  # Original: black
        'rotation_range': (0, 0),
        'border_size': 0,  # Changed from 2 to 0
        'spacing': 0.01,  # 1% minimal spacing
        'shadow': False,
        'border_color': 'white'
    },
    'polaroid': {
        'background_color': 'transparent',  # Original: #EFEFEF
        'rotation_range': (-5, 5),
        'border_size': 0,  # Changed from 12 to 0
        'spacing': 0.05,
        'shadow': True,
        'border_color': 'white'
    },
    'neon': {
        'background_color': 'transparent',  # Original: #121212
        'rotation_range': (0, 0),
        'border_size': 0,  # Changed from 5 to 0
        'spacing': 0.03,
        'shadow': True,
        'border_color': 'white'
    },
    'retro': {
        'background_color': 'transparent',  # Original: #D4B483 (Warm tan)
        'rotation_range': (-4, 4),
        'border_size': 0,  # Changed from 7 to 0
        'spacing': 0.04,
        'shadow': True,
        'border_color': 'white'
    },
    'elegant': {
        'background_color': 'transparent',  # Original: #2C3639 (Dark slate)
        'rotation_range': (0, 0),
        'border_size': 0,  # Changed from 4 to 0
        'spacing': 0.02,
        'shadow': True,
        'border_color': 'white'
    },
    'scrapbook': {
        'background_color': 'transparent',  # Original: #F3EFE0 (Cream paper)
        'rotation_range': (-10, 10),
        'border_size': 0,  # Already 0, no change needed
        'spacing': 0.06,  # More space between images
        'shadow': True,
        'border_color': 'white'
    }
}

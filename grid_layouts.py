"""Grid layout configurations for image collages.

This file defines the grid layouts for different numbers of images.
- GRID_LAYOUTS: A dictionary where the keys are the number of images and the values are lists of layout configurations.
  - Each layout configuration is a dictionary with a name, a description, and a layout.
  - The layout is a list of tuples, where each tuple represents an image and contains four values: (x_ratio, y_ratio, width_ratio, height_ratio).
- DEFAULT_LAYOUT_CONFIG: A default layout configuration to be used as a fallback.
"""

GRID_LAYOUTS = {
    1: [
        {"name": "Standard centered", "layout": [(0.1, 0.1, 0.8, 0.8)],
         "description": "Single image centered with even margins"},
        {"name": "Full bleed", "layout": [(0.02, 0.02, 0.96, 0.96)],
         "description": "Image fills almost the entire canvas"},
        {"name": "Offset right", "layout": [(0.3, 0.1, 0.6, 0.8)],
         "description": "Image positioned toward the right side"},
        {"name": "Offset left", "layout": [(0.1, 0.1, 0.6, 0.8)],
         "description": "Image positioned toward the left side"},
        {"name": "Giant showcase", "layout": [(0.05, 0.05, 0.9, 0.9)],
         "description": "Large image with minimal margins"}
    ],
    2: [
        {"name": "Side by side", "layout": [(0.05, 0.1, 0.45, 0.8), (0.5, 0.1, 0.45, 0.8)],
         "description": "Two images arranged horizontally"},
        {"name": "Stacked vertical", "layout": [(0.1, 0.05, 0.8, 0.45), (0.1, 0.5, 0.8, 0.45)],
         "description": "Two images stacked vertically"},
        {"name": "Diagonal", "layout": [(0.05, 0.05, 0.5, 0.5), (0.45, 0.45, 0.5, 0.5)],
         "description": "Images arranged in a diagonal pattern"},
        {"name": "Asymmetric split", "layout": [(0.05, 0.1, 0.6, 0.8), (0.65, 0.2, 0.3, 0.6)],
         "description": "One large image with a smaller companion"},
        {"name": "Overlapping", "layout": [(0.1, 0.15, 0.55, 0.7), (0.35, 0.15, 0.55, 0.7)],
         "description": "Two images with partial overlap effect"},
        {"name": "Top and bottom", "layout": [(0.15, 0.05, 0.7, 0.43), (0.15, 0.52, 0.7, 0.43)],
         "description": "Two wide images stacked vertically"}
    ],
    3: [
        {"name": "Feature with sidebar", "layout": [(0.05, 0.1, 0.6, 0.8), (0.67, 0.1, 0.28, 0.38), (0.67, 0.52, 0.28, 0.38)],
         "description": "One large image with two smaller images on the right"},
        {"name": "Triangle", "layout": [(0.5 - 0.4, 0.1, 0.8, 0.45), (0.1, 0.55, 0.38, 0.4), (0.52, 0.55, 0.38, 0.4)],
         "description": "Images arranged in a triangular formation"},
        {"name": "Row strip", "layout": [(0.03, 0.25, 0.31, 0.5), (0.35, 0.25, 0.31, 0.5), (0.67, 0.25, 0.31, 0.5)],
         "description": "Three images in a horizontal row"},
        {"name": "L-shaped", "layout": [(0.05, 0.05, 0.45, 0.45), (0.05, 0.5, 0.45, 0.45), (0.5, 0.05, 0.45, 0.9)],
         "description": "Three images arranged in an L-shape pattern"},
        {"name": "Stepped", "layout": [(0.05, 0.05, 0.4, 0.4), (0.3, 0.3, 0.4, 0.4), (0.55, 0.55, 0.4, 0.4)],
         "description": "Cascading diagonal arrangement"},
        {"name": "Vertical column", "layout": [(0.35, 0.03, 0.3, 0.31), (0.35, 0.35, 0.3, 0.31), (0.35, 0.67, 0.3, 0.31)],
         "description": "Three images stacked vertically in the center"}
    ],
    4: [
        {"name": "Grid 2x2", "layout": [(0.05, 0.05, 0.45, 0.45), (0.5, 0.05, 0.45, 0.45),
                                      (0.05, 0.5, 0.45, 0.45), (0.5, 0.5, 0.45, 0.45)],
         "description": "Classic four-image grid arrangement"},
        {"name": "Row strip", "layout": [(0.02, 0.3, 0.23, 0.4), (0.27, 0.3, 0.23, 0.4),
                                       (0.52, 0.3, 0.23, 0.4), (0.77, 0.3, 0.23, 0.4)],
         "description": "Four images in a horizontal filmstrip"},
        {"name": "Feature with sidebar", "layout": [(0.05, 0.05, 0.65, 0.9), (0.7, 0.05, 0.25, 0.28),
                                                  (0.7, 0.35, 0.25, 0.28), (0.7, 0.65, 0.25, 0.28)],
         "description": "Large feature image with three sidebar thumbnails"},
        {"name": "Diamond", "layout": [(0.5-0.2, 0.05, 0.4, 0.4), (0.05, 0.5-0.2, 0.4, 0.4),
                                     (0.55, 0.5-0.2, 0.4, 0.4), (0.5-0.2, 0.55, 0.4, 0.4)],
         "description": "Images arranged in a diamond pattern"},
        {"name": "T-shape", "layout": [(0.05, 0.05, 0.9, 0.45), (0.05, 0.55, 0.3, 0.4),
                                     (0.35, 0.55, 0.3, 0.4), (0.65, 0.55, 0.3, 0.4)],
         "description": "One wide image on top with three below in T-formation"},
        {"name": "Mosaic", "layout": [(0.05, 0.05, 0.6, 0.6), (0.65, 0.05, 0.3, 0.3),
                                    (0.65, 0.35, 0.3, 0.3), (0.05, 0.65, 0.9, 0.3)],
         "description": "Asymmetrical mosaic with varying image sizes"}
    ],
    5: [
        {"name": "Quad with footer", "layout": [(0.05, 0.05, 0.6, 0.6), (0.67, 0.05, 0.28, 0.29), (0.67, 0.36, 0.28, 0.29),
                                              (0.05, 0.67, 0.29, 0.28), (0.36, 0.67, 0.29, 0.28)],
         "description": "Large feature with four smaller images in corners"},
        {"name": "Cross", "layout": [(0.5-0.15, 0.05, 0.3, 0.3), (0.05, 0.5-0.15, 0.3, 0.3), (0.5-0.15, 0.5-0.15, 0.3, 0.3),
                                   (0.65, 0.5-0.15, 0.3, 0.3), (0.5-0.15, 0.65, 0.3, 0.3)],
         "description": "Images arranged in a cross or plus-sign pattern"},
        {"name": "Scattered", "layout": [(0.05, 0.05, 0.35, 0.35), (0.6, 0.1, 0.3, 0.3), (0.15, 0.45, 0.25, 0.25),
                                       (0.5, 0.5, 0.4, 0.4), (0.1, 0.75, 0.35, 0.2)],
         "description": "Random-looking scattered arrangement"},
        {"name": "Central focus", "layout": [(0.3, 0.3, 0.4, 0.4), (0.05, 0.05, 0.25, 0.25), (0.7, 0.05, 0.25, 0.25),
                                           (0.05, 0.7, 0.25, 0.25), (0.7, 0.7, 0.25, 0.25)],
         "description": "Central image with four smaller corner images"},
        {"name": "Horizontal strips", "layout": [(0.05, 0.05, 0.9, 0.28), (0.05, 0.36, 0.43, 0.28),
                                              (0.52, 0.36, 0.43, 0.28), (0.05, 0.67, 0.43, 0.28), (0.52, 0.67, 0.43, 0.28)],
         "description": "Three rows of horizontal strips"},
        {"name": "Magazine layout", "layout": [(0.05, 0.05, 0.43, 0.55), (0.5, 0.05, 0.45, 0.27),
                                            (0.5, 0.33, 0.45, 0.27), (0.05, 0.62, 0.45, 0.33), (0.5, 0.62, 0.45, 0.33)],
         "description": "Editorial-style layout with mixed sizes"}
    ],
    6: [
        {"name": "Split layout", "layout": [(0.05, 0.05, 0.45, 0.45), (0.52, 0.05, 0.43, 0.45), (0.05, 0.52, 0.28, 0.43),
                                          (0.35, 0.52, 0.28, 0.43), (0.65, 0.52, 0.28, 0.43), (0.95, 0.52, 0.28, 0.43)],
         "description": "Two large images on top, four smaller below"},
        {"name": "Grid 2x3", "layout": [(0.05, 0.05, 0.3, 0.45), (0.35, 0.05, 0.3, 0.45), (0.65, 0.05, 0.3, 0.45),
                                      (0.05, 0.5, 0.3, 0.45), (0.35, 0.5, 0.3, 0.45), (0.65, 0.5, 0.3, 0.45)],
         "description": "Six images in a 2x3 grid pattern"},
        {"name": "Grid 3x2", "layout": [(0.05, 0.05, 0.3, 0.3), (0.35, 0.05, 0.3, 0.3), (0.65, 0.05, 0.3, 0.3),
                                      (0.05, 0.35, 0.3, 0.3), (0.35, 0.35, 0.3, 0.3), (0.65, 0.35, 0.3, 0.3)],
         "description": "Six images in a 3x2 grid pattern"},
        {"name": "Circular", "layout": [(0.5-0.2, 0.1, 0.4, 0.4), (0.7, 0.3, 0.25, 0.25), (0.6, 0.65, 0.25, 0.25),
                                      (0.3, 0.65, 0.25, 0.25), (0.05, 0.3, 0.25, 0.25), (0.3, 0.05, 0.25, 0.25)],
         "description": "Images arranged in a circular pattern"},
        {"name": "Feature with grid", "layout": [(0.05, 0.05, 0.5, 0.9), (0.57, 0.05, 0.38, 0.29), (0.57, 0.35, 0.38, 0.29),
                                              (0.57, 0.65, 0.38, 0.29), (0.57, 0.05, 0.19, 0.59), (0.76, 0.05, 0.19, 0.59)],
         "description": "Tall feature image with five arranged on the right"}
    ],
    7: [
        {"name": "Feature with grid", "layout": [(0.05, 0.05, 0.5, 0.5), (0.57, 0.05, 0.38, 0.24), (0.57, 0.3, 0.38, 0.24),
                                              (0.05, 0.57, 0.3, 0.38), (0.37, 0.57, 0.3, 0.38), (0.69, 0.57, 0.26, 0.19),
                                              (0.69, 0.77, 0.26, 0.19)],
         "description": "One large image with six smaller in grid format"},
        {"name": "Mixed grid", "layout": [(0.05, 0.05, 0.3, 0.3), (0.37, 0.05, 0.3, 0.3), (0.69, 0.05, 0.26, 0.63),
                                        (0.05, 0.37, 0.3, 0.3), (0.37, 0.37, 0.3, 0.3), (0.05, 0.69, 0.47, 0.26),
                                        (0.54, 0.69, 0.41, 0.26)],
         "description": "Varied sizes with one tall vertical image"},
        {"name": "Staggered", "layout": [(0.05, 0.05, 0.29, 0.29), (0.36, 0.05, 0.29, 0.29), (0.67, 0.05, 0.29, 0.29),
                                       (0.2, 0.36, 0.29, 0.29), (0.51, 0.36, 0.29, 0.29), (0.05, 0.67, 0.29, 0.29),
                                       (0.36, 0.67, 0.29, 0.29)],
         "description": "Staggered grid with offset alignment"}
    ],
    8: [
        {"name": "Grid 4x2", "layout": [(0.05, 0.05, 0.23, 0.45), (0.29, 0.05, 0.23, 0.45), (0.53, 0.05, 0.23, 0.45),
                                      (0.77, 0.05, 0.18, 0.45), (0.05, 0.51, 0.23, 0.45), (0.29, 0.51, 0.23, 0.45),
                                      (0.53, 0.51, 0.23, 0.45), (0.77, 0.51, 0.18, 0.45)],
         "description": "Eight images in a 4x2 grid pattern"},
        {"name": "Grid 2x4", "layout": [(0.05, 0.05, 0.45, 0.23), (0.05, 0.29, 0.45, 0.23), (0.05, 0.53, 0.45, 0.23),
                                      (0.05, 0.77, 0.45, 0.18), (0.51, 0.05, 0.45, 0.23), (0.51, 0.29, 0.45, 0.23),
                                      (0.51, 0.53, 0.45, 0.23), (0.51, 0.77, 0.45, 0.18)],
         "description": "Eight images in a 2x4 grid pattern"},
        {"name": "Feature with gallery", "layout": [(0.05, 0.05, 0.6, 0.6), (0.67, 0.05, 0.28, 0.29), (0.67, 0.36, 0.28, 0.29),
                                                 (0.05, 0.67, 0.22, 0.28), (0.28, 0.67, 0.22, 0.28), (0.51, 0.67, 0.22, 0.28),
                                                 (0.74, 0.67, 0.22, 0.28), (0.05, 0.05, 0.22, 0.22)],
         "description": "One large feature with gallery of smaller images"}
    ],
    9: [
        {"name": "Grid 3x3", "layout": [(0.05, 0.05, 0.3, 0.3), (0.35, 0.05, 0.3, 0.3), (0.65, 0.05, 0.3, 0.3),
                                      (0.05, 0.35, 0.3, 0.3), (0.35, 0.35, 0.3, 0.3), (0.65, 0.35, 0.3, 0.3),
                                      (0.05, 0.65, 0.3, 0.3), (0.35, 0.65, 0.3, 0.3), (0.65, 0.65, 0.3, 0.3)],
         "description": "Classic 3x3 grid of equal-sized images"},
        {"name": "Central focus", "layout": [(0.35, 0.35, 0.3, 0.3), (0.05, 0.05, 0.3, 0.3), (0.35, 0.05, 0.3, 0.3),
                                           (0.65, 0.05, 0.3, 0.3), (0.05, 0.35, 0.3, 0.3), (0.65, 0.35, 0.3, 0.3),
                                           (0.05, 0.65, 0.3, 0.3), (0.35, 0.65, 0.3, 0.3), (0.65, 0.65, 0.3, 0.3)],
         "description": "Central image highlighted with surrounding images"},
        {"name": "Mixed sizes", "layout": [(0.05, 0.05, 0.45, 0.45), (0.52, 0.05, 0.43, 0.22), (0.52, 0.28, 0.43, 0.22),
                                         (0.05, 0.52, 0.21, 0.43), (0.27, 0.52, 0.22, 0.43), (0.5, 0.52, 0.22, 0.21),
                                         (0.73, 0.52, 0.22, 0.21), (0.5, 0.74, 0.22, 0.21), (0.73, 0.74, 0.22, 0.21)],
         "description": "Varied image sizes in an asymmetric layout"}
    ],
    10: [
        {"name": "Grid 5x2", "layout": [(0.05, 0.05, 0.18, 0.45), (0.24, 0.05, 0.18, 0.45), (0.43, 0.05, 0.18, 0.45),
                                      (0.62, 0.05, 0.18, 0.45), (0.81, 0.05, 0.14, 0.45), (0.05, 0.51, 0.18, 0.45),
                                      (0.24, 0.51, 0.18, 0.45), (0.43, 0.51, 0.18, 0.45), (0.62, 0.51, 0.18, 0.45),
                                      (0.81, 0.51, 0.14, 0.45)],
         "description": "Ten images in a 5x2 grid layout"},
        {"name": "Grid 2x5", "layout": [(0.05, 0.05, 0.45, 0.18), (0.05, 0.24, 0.45, 0.18), (0.05, 0.43, 0.45, 0.18),
                                      (0.05, 0.62, 0.45, 0.18), (0.05, 0.81, 0.45, 0.14), (0.51, 0.05, 0.45, 0.18),
                                      (0.51, 0.24, 0.45, 0.18), (0.51, 0.43, 0.45, 0.18), (0.51, 0.62, 0.45, 0.18),
                                      (0.51, 0.81, 0.45, 0.14)],
         "description": "Ten images in a 2x5 grid layout"},
        {"name": "Feature with strip", "layout": [(0.05, 0.05, 0.65, 0.65), (0.71, 0.05, 0.24, 0.32), (0.71, 0.38, 0.24, 0.32),
                                               (0.05, 0.71, 0.19, 0.24), (0.25, 0.71, 0.19, 0.24), (0.45, 0.71, 0.19, 0.24),
                                               (0.65, 0.71, 0.19, 0.24), (0.85, 0.71, 0.1, 0.24), (0.05, 0.05, 0.13, 0.13),
                                               (0.57, 0.57, 0.13, 0.13)],
         "description": "Large feature with horizontal strip and accent images"}
    ],
    12: [
        {"name": "Grid 4x3", "layout": [(0.05, 0.05, 0.23, 0.30), (0.29, 0.05, 0.23, 0.30), (0.53, 0.05, 0.23, 0.30),
                                      (0.77, 0.05, 0.18, 0.30), (0.05, 0.36, 0.23, 0.30), (0.29, 0.36, 0.23, 0.30),
                                      (0.53, 0.36, 0.23, 0.30), (0.77, 0.36, 0.18, 0.30), (0.05, 0.67, 0.23, 0.30),
                                      (0.29, 0.67, 0.23, 0.30), (0.53, 0.67, 0.23, 0.30), (0.77, 0.67, 0.18, 0.30)],
         "description": "Twelve images in a 4x3 grid layout"},
        {"name": "Mixed mosaic", "layout": [(0.05, 0.05, 0.30, 0.30), (0.36, 0.05, 0.30, 0.30), (0.67, 0.05, 0.28, 0.30),
                                         (0.05, 0.36, 0.30, 0.30), (0.36, 0.36, 0.30, 0.30), (0.67, 0.36, 0.28, 0.30),
                                         (0.05, 0.67, 0.15, 0.28), (0.21, 0.67, 0.15, 0.28), (0.37, 0.67, 0.15, 0.28),
                                         (0.53, 0.67, 0.15, 0.28), (0.69, 0.67, 0.15, 0.28), (0.85, 0.67, 0.10, 0.28)],
         "description": "Six regular images with six smaller ones below"}
    ],
    15: [
        {"name": "Grid 5x3", "layout": [(0.05, 0.05, 0.18, 0.30), (0.24, 0.05, 0.18, 0.30), (0.43, 0.05, 0.18, 0.30),
                                      (0.62, 0.05, 0.18, 0.30), (0.81, 0.05, 0.14, 0.30), (0.05, 0.36, 0.18, 0.30),
                                      (0.24, 0.36, 0.18, 0.30), (0.43, 0.36, 0.18, 0.30), (0.62, 0.36, 0.18, 0.30),
                                      (0.81, 0.36, 0.14, 0.30), (0.05, 0.67, 0.18, 0.30), (0.24, 0.67, 0.18, 0.30),
                                      (0.43, 0.67, 0.18, 0.30), (0.62, 0.67, 0.18, 0.30), (0.81, 0.67, 0.14, 0.30)],
         "description": "Fifteen images in a 5x3 grid layout"}
    ]
}

# Default layout for fallback
DEFAULT_LAYOUT_CONFIG = {
    "name": "Standard centered",
    "layout": [(0.1, 0.1, 0.8, 0.8)],
    "description": "Single image centered with even margins"
}

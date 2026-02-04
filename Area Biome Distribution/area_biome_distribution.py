from pathlib import Path
from pixel_count.pixel_count import count_colour_pixels as ccp
import os

class Area:
    def __init__(self, name):
        self.name = name
        self.file_format_name = "" # Snake Case
        self.biomes = []
        self.distribution = {}
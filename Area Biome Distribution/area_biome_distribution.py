from pathlib import Path
from pixel_count.pixel_count import count_colour_pixels as ccp
import os

class Area:
    def __init__(self, name):
        self.name = name
        self.snake_case_name = "" # Snake Case
        self.biomes = []
        self.biome_pixels = {}
        self.distribution = {}
        self.pixel_total = 0
        self.target_colour_rgb = (80, 47, 121)

        area_name_split=self.name.lower().split(" ")
        area_name = ""
        for token in area_name_split:
            area_name += token + "_"
        self.snake_case_name = area_name[:len(area_name)-1]

    def count(self, image_path):
        # Expects image path to be something like 3Paldea_Inlet_Grotto_Map_Cave.png
        arr = image_path.split("_")
        biome_arr = arr[len(arr)-1].split(".")
        biome = biome_arr[0]
        if biome not in self.biomes:
            self.biomes.append(biome)
            bp = ccp(image_path, self.target_colour_rgb)
            self.biome_pixels[biome] = bp
            self.pixel_total += bp
        self.biomes.sort()

    def calculate_distribution(self):
        for biome in self.biomes:
            percentage = self.biome_pixels[biome] / self.pixel_total
            self.distribution[biome] = percentage

    def csv(self):
        pass
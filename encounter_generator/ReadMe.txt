This program was made for nuzlocking the base game of Pokémon Scarlet and Violet.
A nuzlocke is a type of fan-made challenge in Pokémon games that has the two core rules:
- you are limited to one Pokémon per unique location
- if a Pokémon you own faints, you cannot use that Pokémon for the rest of the playthrough.

A common optional rule is Dupes Clause, which states:
    - A Pokémon (or its evolutionary-related Pokémon) that you have already captured before are "dupes" or duplicates
    - If encountering a dupe, the dupe can be ignored and you can attempt another encounter
    - This continues until finding a non-dupe

This program will check:
- the chosen location
- time of day
- boosting power that influences certain types to spawn
- the Pokémon that have already been captured (optional)
and it will either choose a Pokémon or display the probability of each Pokémon based on a weighted score.

In the logic code, Pokémon is written as Pokemon (without the acute accent, i.e., é) as it is easier to write.
The two main executable files are main.py, and biome_distribution.py. 
main.py is meant to have most of the interactivity.
biome_distribution is meant to generate CSV files that represents the percentage of area that any given biome takes up in a location.

Data Folder contains raw data files in .txt, .csv, or .png form, meant to separate majority of the data from the logic.
Models Folder contains the two main logic classes, Game and Area. Though they are separate classes, they are tightly coupled. 
    The user interacts with Game objects, and the Game class depends on the Area class.
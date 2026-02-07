import random

def correct_version(game_string, pkmn_to_check):
        """
        Docstring for correct_version
        
        :param self: Area object.
        :param game_string: String object representing game version, either "Scarlet" or "Violet"
        :param pkmn_to_check: String object representing name of Pokemon.
        """
        if game_string.lower() == "scarlet" and pkmn_to_check.lower().find("violet") == -1:
            return True
        elif game_string.lower() == "violet" and pkmn_to_check.lower().find("scarlet") == -1:
            return True 
        else:
            return False

def power(power_int):
        """
        Docstring for power_int
        
        :param self: Area object.
        :param power_int: An Integer intended to 1, 2, or 3. Depending on power_int level, it has a greater chance of forcing a specific Type (Grass, Water, etc.) Pokemon to spawn.
        
        upper_bound represents the percentage chance that a specific Type Pokemon is forced to spawn.
        Generates a random number from 1 to 100 (inclusive), if it is less than or equal to the upper_bound, then the specific Type is forced.
        """
        upper_bound = 0
        if power_int == 1:
            upper_bound = 50
        elif power_int == 2:
            upper_bound = 75
        elif power_int == 3: 
            upper_bound = 100
        else:
            return False
        
        if random.randint(1,100) <= upper_bound:
            return True
        else:
            return False

def valid_area(string_input):
        areas = {
        "Alfornada Cavern",
        "Asado Desert",
        "Cabo Poco",
        "Casseroya Lake",
        "Dalizapa Passage",
        "East Paldean Sea",
        "East Province (Area One)",
        "East Province (Area Two)",
        "East Province (Area Three)",
        "Glaseado Mountain",
        "Great Crater of Paldea",
        "Inlet Grotto",
        "North Paldean Sea",
        "North Province (Area One)",
        "North Province (Area Two)",
        "North Province (Area Three)",
        "Poco Path",
        "Pokemon League",
        "Socarrat Trail",
        "South Paldean Sea",
        "South Province (Area One)",
        "South Province (Area Two)",
        "South Province (Area Three)",
        "South Province (Area Four)",
        "South Province (Area Five)",
        "South Province (Area Six)",
        "Tagtree Thicket",
        "West Paldean Sea",
        "West Province (Area One)",
        "West Province (Area Two)",
        "West Province (Area Three)"
        }

        return any(string_input.lower() == area.lower() for area in areas)

def valid_type(string_input):
    types = ["Normal","Fighting","Flying","Poison","Ground","Rock","Bug","Ghost","Steel","Fire","Water","Grass","Electric","Psychic","Ice","Dragon","Dark","Fairy"]
    string_input = string_input.strip().lower()
    return any(string_input.strip().lower() == pkmn_type.strip().lower() for pkmn_type in types)

def resolve_daypart(time):
        valid = True
        valid_dayparts = {"Dawn", "Day", "Dusk", "Night"}
        daypart = ""

        if isinstance(time, str):
            time = time.title()
            for dp in valid_dayparts:
                if time == dp:
                    daypart = dp
                    break

        if isinstance(time, int):
            if time == 0:
                daypart = "Dawn"
            elif time == 1:
                daypart = "Day"
            elif time == 2:
                daypart = "Dusk"
            elif time == 3:
                daypart = "Night"
            else:
                valid = False

        if valid == False:
            return False
        elif daypart != "":
            return daypart

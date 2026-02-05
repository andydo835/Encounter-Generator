import random
import modules.name_conventions.nc as nc
            
class Area:
    def __init__(self, name):
        self.name = nc.standard(name)
        self.snake_case_name = nc.snake_case(name)
        self.pokemon = []
        self.dawn = {}
        self.day = {}
        self.dusk = {}
        self.night = {}
        self.biome_multipliers = {}
        self.load_biome_multipliers()
        self.load_inserts()

    def load_biome_multipliers(self):
        file_path = f"data/distribution/{self.snake_case_name}.csv"
        lines = ""
        with open(file_path, 'r') as f:
            lines = f.readlines()

        for x in range(len(lines)-1):
            line = lines[x+1].split(",")
            biome = line[0]
            percentage = line[1][:len(line[1])-1] # This extra code is to remove the \n at the end of percentage
            self.biome_multipliers[biome] = float(percentage)

    def power(self, power):
        upper_bound = 0
        if power == 1:
            upper_bound = 50
        elif power == 2:
            upper_bound = 75
        elif power == 3: 
            upper_bound = 100
        else:
            return False
        
        if random.randint(1,100) <= upper_bound:
            return True
        else:
            return False

    def parse_insert(self, insert_string):
        # insert_string should look something like: Dugtrio,Ground,Ground,Cave,20,20,20,20
        line = insert_string.split(",")
        name = line[0]
        type1 = line[1]
        type2 = line[2]
        biome = line[3]
        multiplier = self.biome_multipliers[biome]
        dawn = int(line[4])*multiplier
        day = int(line[5])*multiplier
        dusk = int(line[6])*multiplier
        night = int(line[7])*multiplier
        type_string = type1

        if type1 != type2:
            type_string = f"{type_string}_{type2}"

        # identifier will end up looking something like: Dugtrio_Ground
        identifier = f"{name}_{type_string}"

        
        if self.find_key(identifier) == False:
            self.pokemon.append(identifier)
            self.dawn[identifier] = dawn
            self.day[identifier] = day
            self.dusk[identifier] = dusk
            self.night[identifier] = night
        else:
            self.dawn[identifier] = self.dawn[identifier] + dawn
            self.day[identifier] = self.day[identifier] + day
            self.dusk[identifier] = self.dusk[identifier] + dusk
            self.night[identifier] = self.night[identifier] + night

    def load_inserts(self):
        file_path = f"data/probability_insert/{self.snake_case_name}.csv"
        lines = ""
        with open(file_path, 'r') as f:
            lines = f.readlines()

        for x in range(len(lines)-1):
            line = lines[x+1]
            line = line[:len(line)-1]
            self.parse_insert(line)

    def find_key(self, pkmn_to_check):
        """
        Docstring for find_key
        
        :param self: Area object.
        :param pkmn_to_check: String representing the Pokemon that is being checked if it already exists.

        This function will check if this self.pokemon being inquired has already been recorded in this area.
        This function is used because dictionaries are used in the case of sum + addend.
        Dictionaries will throw an error in the case above if the key does not already exist.
        Hence, the need for this function.
        """
        # Compare the Pokemon to be checked to every Pokemon recorded in the area
        # Return whether or not the Pokemon was found
        # Names are compared in lowercase in case of any strange case input errors. 
        found = any(pkmn_to_check.lower() == recorded_pkmn.lower() for recorded_pkmn in self.pokemon)
        return found
    
    def find_dupe(self, dupes, pkmn_to_check, rule_enabled):
        """
        Docstring for find_dupe
        
        :param self: Area object.
        :param dupes: Set of Strings representing Pokemon in the form "Name_Typestring" such as "Pikachu_Electric" or "Charizard_Fire_Flying". Typically, argument will be "dupes" set recorded by Game object.
        :param pkmn_to_check: String representing the Pokemon that is being checked if it already exists.
        :param rule_enabled: Boolean that signifies if the function will perform any operations. 

        "Dupe" is short for "duplication", and is in reference to a Pokemon (or evolutionary related Pokemon) that you already have CAPTURED before.
        This is related to a common optional rule called "Dupes Clause", which is explained below.which means if you encounter a Pokemon,
        if it is a duplicate then you can ignore it and encounter a different Pokemon, 
        where that Pokemon can also be ignored as per Dupes Clause rules.
        This continues until you encounter a Pokemon (nor any of its evolutionary related Pokemon) that has not been CAPTURED before.

        Dupes Clause is a common optional rule that states:
            - A Pokemon (or its evolutionary-related Pokemon) that you have already captured before are "dupes" or duplicates
            - If encountering a dupe, the dupe can be ignored and you can attempt another encounter
            - This continues until finding a non-dupe
        
        Dupes Clause is used to:
            - Add uniqueness to the roster that you build
            - Add difficulty by making Pokemon irreplaceable
        """
        # Redundancy to check if rule_enabled is a Boolean 
        rule_enabled = (rule_enabled) if (True | False) else (False)

        if rule_enabled == False:
            return False

        # Compare the Pokemon to be checked to every Pokemon in the dupes list
        # Return whether or not the Pokemon is a dupe
        # Names are compared in lowercase in case of any strange case input errors.
        return any(pkmn_to_check == dupe.lower() for dupe in dupes)

    def distribution(self, game, time, type, power, dupes, check_dupes):

        # Choosing all possible wild Pokemon that are present within the day part selected.
        time = time.lower().strip()
        print("{0} ({1})".format(self.name,time.capitalize()))
        selected = {}
        if time == "dawn":
            selected = self.dawn
        elif time == "day":
            selected = self.day
        elif time == "dusk":
            selected = self.dusk
        elif time == "night":
            selected = self.night

        # Ensures that types entered are legitimate types, and will ignore typos.
        types = ["Normal","Fighting","Flying","Poison","Ground","Rock","Bug","Ghost","Steel","Fire","Water","Grass","Electric","Psychic","Ice","Dragon","Dark","Fairy"]
        valid_type = False
        for t in types:
            if type.strip().lower() == t.strip().lower():
                valid_type = True
                break
        
        """
        I am under the assumption that the way Encounter Powers works is: 
        whatever % of encounters will be the enforced type, while the other % will always be a different type.
        I have yet to find extensive evidence that proves or disproves this, but it is a simpler assumption
        compared to the possibility that the other % still having a chance to spawn the enforced type.
        """
        upper_bound = 0
        if power >= 1 and power <= 3 and valid_type == True:
            if power == 1:
                upper_bound = 0.50
            elif power == 2:
                upper_bound = 0.75
            elif power == 3: 
                upper_bound = 1
        multiplier = (1-upper_bound)

        sum = 0
        keys = selected.keys() # Keys are possible wild Pokemon present in the day part selected.
        for k in keys: # For every while Pokemon
            if self.find_dupe(dupes, k.split("_")[0], check_dupes) == False: # Proceed if neither the Pokemon (or related Pokemon) have already been captured
                if game == "Scarlet" and k.find("Violet") == -1: # Proceed if the Pokemon is not an opposite version exclusive 
                    if valid_type == True and upper_bound != 0 and k.find(type) == -1: # If there is an Encounter Power in use and the Pokemon is not of the correct type,
                        sum = sum + selected[k]*multiplier # Apply the multiplier (actually makes chances worse for incorrect type pokemon)
                    else:
                        sum = sum + selected[k]
                elif game == "Violet" and k.find("Scarlet") == -1:
                    if valid_type == True and upper_bound != 0 and k.find(type) == -1:
                        sum = sum + selected[k]*multiplier
                    else:
                        sum = sum + selected[k]
        
        names = []
        percents = []
        for k in keys:
            if self.find_dupe(dupes, k.split("_")[0], check_dupes) == False:
                if game == "Scarlet" and k.find("Violet") == -1:
                    n = k.split("_")[0]
                    percent = 0
                    if valid_type == True and upper_bound != 0 and k.find(type) == -1:
                        percent = selected[k]*multiplier/sum
                    else:
                        percent = selected[k]/sum
                    index = -1
                    percent = percent * 10000
                    percent = percent // 1
                    percent = percent / 100
                    if len(percents) == 0:
                        index = 0
                    else:
                        for x in range(len(percents)):
                            if percent >= percents[x]:
                                index = x
                                break
                        if index == -1:
                            index = len(percents)
                    names.insert(index, n)
                    percents.insert(index, percent)
                elif game == "Violet" and k.find("Scarlet") == -1:
                    n = k.split("_")[0]
                    percent = 0
                    if valid_type == True and upper_bound != 0 and k.find(type) == -1:
                        percent = selected[k]*multiplier/sum
                    else:
                        percent = selected[k]/sum
                    index = 0
                    percent = percent * 10000
                    percent = percent // 1
                    percent = percent / 100
                    if len(percents) == 0:
                        continue
                    else:
                        for x in range(len(percents)):
                            if percent >= percents[x]:
                                index = x
                                break
                            index = len(percents)-1
                    names.insert(index, n)
                    percents.insert(index, percent)
        for x in range(len(names)):
            print("{0}: {1}%".format(names[x],percents[x]))        

    def generate(self, game, time, type, power, dupes, check_dupes):
        class Range:
            def __init__(self, name, lower, upper):
                self.name = name
                self.lower = lower
                self.upper = upper

            def enclosed(self, number):
                return (self.lower <= number and number <= self.upper)             

        # Ensures that types entered are legitimate types, and will ignore typos.
        types = ["Normal","Fighting","Flying","Poison","Ground","Rock","Bug","Ghost","Steel","Fire","Water","Grass","Electric","Psychic","Ice","Dragon","Dark","Fairy"]
        valid_type = False
        for t in types:
            if type.strip().lower() == t.strip().lower():
                valid_type = True
                break
        
        # If the type entered is real, then check if the specific type is activated.
        power_activated = False
        if valid_type == True:
            power_activated = self.power(power)

        # Select a day part
        time = time.lower().strip()
        selected = {}
        if time == "dawn":
            selected = self.dawn
        elif time == "day":
            selected = self.day
        elif time == "dusk":
            selected = self.dusk
        elif time == "night":
            selected = self.night

        sum = 0
        keys = selected.keys() # Keys are possible wild Pokemon present in the day part selected.
        ranges = []

        for k in keys: # For every wild Pokemon
            if self.find_dupe(dupes, k.split("_")[0], check_dupes) == False: # Proceed if neither the Pokemon (or related Pokemon) have already been captured
                if game == "Scarlet" and k.find("Violet") == -1: # Proceed if the Pokemon is not an opposite version exclusive 
                    if power_activated == True and k.find(type) == -1: # Skip if a specific type is enforced, and the Pokemon does not match the type.
                        continue
                    ranges.append(Range(k, sum, sum + selected[k])) # Otherwise, create ranges with bounds like: [(0, 15.7563), (15.7563, 26.0), etc.]
                    sum = sum + selected[k]
                elif game == "Violet" and k.find("Scarlet") == -1:
                    if power_activated == True and k.find(type) == -1:
                        continue
                    ranges.append(Range(k, sum, sum + selected[k]))
                    sum = sum + selected[k]
    
        rng = random.uniform(0, sum) # Generate a value
        for r in ranges: # For every range created...
            if r.enclosed(rng): # Proceed if the value falls within the range
                pkmn_name = r.name.split("_")[0]
                print(f"{self.name} ({time.title()}): {pkmn_name}")
                return r.name

    def load_areas():
        alfornada_cavern = Area("Alfornada Cavern")
        asado_desert = Area("Asado Desert")
        cabo_poco = Area("Cabo Poco")
        casseroya_lake = Area("Casseroya Lake")
        dalizapa_passage = Area("Dalizapa Passage")
        east_paldean_sea = Area("East Paldean Sea")
        east_province_area_one = Area("East Province (Area One)")
        east_province_area_two = Area("East Province (Area Two)")
        east_province_area_three = Area("East Province (Area Three)")
        glaseado_mountain = Area("Glaseado Mountain")
        great_crater_of_paldea = Area("Great Crater of Paldea")
        inlet_grotto = Area("Inlet Grotto")
        north_paldean_sea = Area("North Paldean Sea")
        north_province_area_one = Area("North Province (Area One)")
        north_province_area_two = Area("North Province (Area Two)")
        north_province_area_three = Area("North Province (Area Three)")
        poco_path = Area("Poco Path")
        pokemon_league = Area("Pokemon League")
        socarrat_trail = Area("Socarrat Trail")
        south_paldean_sea = Area("South Paldean Sea")
        south_province_area_one = Area("South Province (Area One)")
        south_province_area_two = Area("South Province (Area Two)")
        south_province_area_three = Area("South Province (Area Three)")
        south_province_area_four = Area("South Province (Area Four)")
        south_province_area_five = Area("South Province (Area Five)")
        south_province_area_six = Area("South Province (Area Six)")
        tagtree_thicket = Area("Tagtree Thicket")
        west_paldean_sea = Area("West Paldean Sea")
        west_province_area_one = Area("West Province (Area One)")
        west_province_area_two = Area("West Province (Area Two)")
        west_province_area_three = Area("West Province (Area Three)")

        alphabetical = {}
        alphabetical[1] = alfornada_cavern
        alphabetical[2] = asado_desert
        alphabetical[3] = cabo_poco
        alphabetical[4] = casseroya_lake
        alphabetical[5] = dalizapa_passage
        alphabetical[6] = east_paldean_sea
        alphabetical[7] = east_province_area_one
        alphabetical[8] = east_province_area_two
        alphabetical[9] = east_province_area_three
        alphabetical[10] = glaseado_mountain
        alphabetical[11] = great_crater_of_paldea
        alphabetical[12] = inlet_grotto
        alphabetical[13] = north_paldean_sea
        alphabetical[14] = north_province_area_one
        alphabetical[15] = north_province_area_two
        alphabetical[16] = north_province_area_three
        alphabetical[17] = poco_path
        alphabetical[18] = pokemon_league
        alphabetical[19] = socarrat_trail
        alphabetical[20] = south_paldean_sea
        alphabetical[21] = south_province_area_one
        alphabetical[22] = south_province_area_two
        alphabetical[23] = south_province_area_three
        alphabetical[24] = south_province_area_four
        alphabetical[25] = south_province_area_five
        alphabetical[26] = south_province_area_six
        alphabetical[27] = tagtree_thicket
        alphabetical[28] = west_paldean_sea
        alphabetical[29] = west_province_area_one
        alphabetical[30] = west_province_area_two
        alphabetical[31] = west_province_area_three


        chronological = {}
        chronological[1] = cabo_poco
        chronological[2] = poco_path
        chronological[3] = inlet_grotto
        chronological[4] = south_province_area_one
        chronological[5] = south_province_area_two
        chronological[6] = pokemon_league
        chronological[7] = south_province_area_three
        chronological[8] = west_province_area_one
        chronological[9] = south_paldean_sea
        chronological[10] = south_province_area_four
        chronological[11] = south_province_area_five
        chronological[12] = east_province_area_one
        chronological[13] = east_province_area_two
        chronological[14] = east_province_area_three
        chronological[15] = tagtree_thicket
        chronological[16] = west_province_area_two
        chronological[17] = west_province_area_three
        chronological[18] = east_paldean_sea
        chronological[19] = west_paldean_sea
        chronological[20] = dalizapa_passage
        chronological[21] = glaseado_mountain
        chronological[22] = alfornada_cavern
        chronological[23] = south_province_area_six
        chronological[24] = asado_desert
        chronological[25] = north_province_area_three
        chronological[26] = north_province_area_two
        chronological[27] = north_province_area_one
        chronological[28] = north_paldean_sea
        chronological[29] = casseroya_lake
        chronological[30] = socarrat_trail
        chronological[31] = great_crater_of_paldea
        
        pair = [chronological, alphabetical]
        return pair

class Game:
    def __init__(self, game):
        self.game = game.strip().lower().capitalize()
        self.areas = []
        self.box = []
        self.links = {}
        self.dupes = set()
        self.pokedex = []
        self.alphabetical = {}
        self.chronological = {}

        with open("data/pokedex/paldea_dex.txt","r") as f1:
            self.pokedex = f1.readlines()
        
        for x in range(len(self.pokedex)):
            self.pokedex[x] = self.pokedex[x][0:len(self.pokedex[x])-1].strip()
        
        self.define_links()
        self.load_areas()
        
    def define_links(self):
        links = ""
        with open("data/pokedex/links.txt", "r") as f1:
            links = f1.readlines()
        for line in links:
            pkmn_list = line.strip().split(",")
            header_pkmn = pkmn_list[0]
            linked_pkmn = pkmn_list[1].split("_")
            self.links[header_pkmn] = linked_pkmn

    def populate_dupes(self):
        for boxed_pkmn in self.box:
            link = self.links[boxed_pkmn]
            for pkmn in link:
                self.dupes.add(pkmn)

    def generate(self, pkmn_set_int, area, time, type, power, check_dupes):
        pkmn_set = {}
        area_chosen = -1
        daypart = ""
        if pkmn_set_int == 0:
            pkmn_set = self.chronological
        elif pkmn_set_int == 1:
            pkmn_set = self.alphabetical
        else:
            print("0 = chronological")
            print("1 = alphabetical")
            return None

        if 1 <= area and area <= 31:
            area_chosen = area
        else:
            print("Areas 1-31")
            return None

        if time == 0:
            daypart = "Dawn"
        elif time == 1:
            daypart = "Day"
        elif time == 2:
            daypart = "Dusk"
        elif time == 3:
            daypart = "Night"
        else:
            print("0 = Dawn")
            print("1 = Day")
            print("2 = Dusk")
            print("3 = Night")
            return None
        
        pkmn_set[area_chosen].generate(self.game, daypart, type, power, self.dupes, check_dupes)

    def distribution(self, pkmn_set_int, area, time, type, power, check_dupes):
        pkmn_set = {}
        area_chosen = -1
        daypart = ""
        if pkmn_set_int == 0:
            pkmn_set = self.chronological
        elif pkmn_set_int == 1:
            pkmn_set = self.alphabetical
        else:
            print("0 = chronological")
            print("1 = alphabetical")
            return None

        if 1 <= area and area <= 31:
            area_chosen = area
        else:
            print("Areas 1-31")
            return None

        if time == 0:
            daypart = "Dawn"
        elif time == 1:
            daypart = "Day"
        elif time == 2:
            daypart = "Dusk"
        elif time == 3:
            daypart = "Night"
        else:
            print("0 = Dawn")
            print("1 = Day")
            print("2 = Dusk")
            print("3 = Night")
            return None
        
        pkmn_set[area_chosen].distribution(self.game, daypart, type, power, self.dupes, check_dupes)

    def locate(self, pkmn_set_int, pkmn):
        if pkmn_set_int == 0:
            pkmn_set = self.chronological
        elif pkmn_set_int == 1:
            pkmn_set = self.alphabetical
        else:
            print("0 = chronological")
            print("1 = alphabetical")
            return None
        
        habitats = []
        for x in range(len(pkmn_set)):
            pkmn_found = False
            dawn_found = False
            day_found = False
            dusk_found = False
            night_found = False
            for k in pkmn_set[x+1].dawn.keys():
                if k.lower().find(pkmn.lower().strip()) != -1:
                    pkmn_found = True
                    break
            if pkmn_found == False:
                continue
            elif pkmn_found == True:
                for k in pkmn_set[x+1].dawn.keys():
                    if k.lower().find(pkmn.lower().strip()) == -1:
                        continue
                    if pkmn_set[x+1].dawn[k] > 0:
                        dawn_found = True
                        break
                for k in pkmn_set[x+1].day.keys():
                    if k.lower().find(pkmn.lower().strip()) == -1:
                        continue
                    if pkmn_set[x+1].day[k] > 0:
                        day_found = True
                        break
                for k in pkmn_set[x+1].dusk.keys():
                    if k.lower().find(pkmn.lower().strip()) == -1:
                        continue
                    if pkmn_set[x+1].dusk[k] > 0:
                        dusk_found = True
                        break
                for k in pkmn_set[x+1].night.keys():
                    if k.lower().find(pkmn.lower().strip()) == -1:
                        continue
                    if pkmn_set[x+1].night[k] > 0:
                        night_found = True
                        break
            if (dawn_found == True) and (day_found == True) and (dusk_found == True) and (night_found == True):
                habitats.append(pkmn_set[x+1].name)
            else:
                string = pkmn_set[x+1].name + " ("
                if dawn_found == True:
                    string = string + "Dawn, "
                if day_found == True:
                    string = string + "Day, "
                if dusk_found == True:
                    string = string + "Dusk, "
                if night_found == True:
                    string = string + "Night, "
                string = string[0:len(string)-2] + ")"
                habitats.append(string)
        if len(habitats) >= 1:
            print("{0} is located in:".format(pkmn))
            for x in habitats:
                print(x)

    def load_areas(self):
        duo = Area.load_areas()
        self.alphabetical = duo[1]
        self.chronological = duo[0]


g = Game("Scarlet")
g.box = ["Crocalor","Clodsire","Gumshoos","Arrokuda","Klawf","Bombirdier", "Magikarp", "Gimmighoul","Azumarill","Oinkologne (Male)","Tauros (Combat Breed)", "Goomy","Basculin (Red-Striped)"]
g.populate_dupes()
g.distribution(0,15,1,"Flying",0,True)
g.generate(0,15,1,"Flying",0,True)
#g.generate(0,8,1,"Flying",0)
#g.distribution(0,9,1,"Normal",0)
#g.generate(0,15,1,"Fairy",1)
#g.locate(0, "Dratini")
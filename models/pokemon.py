class Pokemon:
    def __init__(self, name, type1, type2, dawn, day, dusk, night):
        self.dawn = float(dawn)
        self.day = float(day)
        self.dusk = float(dusk)
        self.night = float(night)
        self.dupes = []

        attributes_to_format = [name, type1, type2]
        for attribute in attributes_to_format:
            attribute = attribute.strip().title()
        
        self.name = name
        self.type1 = type1
        self.type2 = type2
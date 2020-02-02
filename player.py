
class Player:

    armies = []
    name = ""
    coins = 20
    cavalry = 0
    infantry = 0
    archer = 0


    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def buy_units(self, type, amount, army_name):

        amount = int(amount)
        if type is "I":

            new_army = Army(self.name, army_name)
            new_army.add_infantry(amount)
            self.armies.append(new_army)
            self.infantry = self.infantry + amount

        elif type is "A":
            new_army = Army(self.name, army_name)
            new_army.add_archer(amount)
            self.armies.append(new_army)
            self.archer = self.archer+ amount

        elif type is "C":
            new_army = Army(self.name, army_name)
            new_army.add_cavalry(amount)
            self.armies.append(new_army)
            self.cavalry = self.cavalry + amount


    def info(self):

        information = []
        information.append("ARMY: ")

        for army in self.armies:
            information[0] = information[0] + army.get_name() + " "
            information.append(f"Cavalry: {army.cavalry}")
            information.append(f"Infantry: {army.infantry}")
            information.append(f"Archers: {army.archer}")



        return information





class Army:
    cavalry = 0
    infantry = 0
    archer = 0
    owner=""
    army=""

    def __init__(self, name, army_name):
        self.owner = name
        self.army = army_name

    def add_infantry(self, addition):
        self.infantry = self.infantry + addition

    def add_archer(self, addition):
        self.archer = self.archer+ addition

    def add_cavalry(self, addition):
        self.cavalry = self.cavalry + addition

    def get_name(self):
        return self.army



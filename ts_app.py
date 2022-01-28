# App to play twilight struggle

defcon = 5
phasing_player = 'USA'
countries = {}


def adjust_defcon(adjustment_value):
    global defcon
    defcon = defcon + adjustment_value

    # Adjust defcon to 5 if above 5
    if defcon > 5:
        defcon = 5

    # Check to see if the defcon has ended the game
    # TODO - Add game ending conditions if defcon = 1


class CardGame:
    """Base class for a collection of Card Pile objects"""
    # TODO Finish the CardGame class with piles

    def __init__(self, n, d):
        self.name = n
        self.date = d
        self.piles = []


class Country:
    """Base class for a country in a game"""
    def __init__(self, n):
        self.name = n

    def __repr__(self):
        return "<Country: %s>" % self.name

    def __str__(self):
        return self.name


class Player:
    """Base class for a player in a game"""
    def __init__(self, n):
        self.name = n

    def __repr__(self):
        return "<Player: %s>" % self.name

    def __str__(self):
        return self.name


class TwilightStruggleCountry(Country):
    """Class of countries specific to Twilight Struggle"""

    def __init__(self, n, r, sr, st, bg, usa_i, ussr_i, c):
        Country.__init__(self, n)

        if r not in ['Africa', 'Asia', 'Central America', 'Europe', 'Middle East', 'South America']:
            raise ValueError("Error creating Twilight Struggle country. Region must be one of: Africa, Asia, Central America, Europe, Middle East, or South America")
        self.region = r

        if sr not in ['Both Europe', 'Eastern Europe', 'Western Europe', 'Southeast Asia', '']:
            raise ValueError("Error creating Twilight Struggle country. Subregion must be one of: 'Both Europe', 'Eastern Europe', 'Western Europe', or 'Southeast Asia'")
        if sr == '':
            pass
        else:
            self.subregion = sr

        if not st.isdigit() and (int(st) > 4 or int(st) < 1):
            raise ValueError("Error creating Twilight Struggle country. Stability must be a number between 1 and 4")
        self.stability = int(st)

        if bg not in ['TRUE', 'FALSE']:
            raise ValueError("Error creating Twilight Struggle country. Battleground must be True or False.")
        self.battleground = True if bg == 'True' else False

        if not usa_i.isdigit():
            raise ValueError("Error creating Twilight Struggle country. USA influence must be a number.")
        self.usa_influence = int(usa_i)

        if not ussr_i.isdigit():
            raise ValueError("Error creating Twilight Struggle country. USSR influence must be a number.")
        self.ussr_influence = int(ussr_i)

        if c not in ['usa', 'ussr', '']:
            raise ValueError("Error creating Twilight Struggle country. Controlled must be 'usa', 'ussr', or ''")
        self.controlled = c


class TwilightStruggleGame(CardGame):
    """Class of an individual game of Twilight Struggle"""

    turns = 10
    action_rounds = {1: 6, 2: 6, 3: 6, 4: 7, 5: 7, 6: 7, 7: 7, 8: 7, 9: 7, 10: 7}

    def __init__(self, n, d, opt):
        CardGame.__init__(self, n, d)

        if not opt.isdigit() and int(opt) != 1 and int(opt) != 0:
            raise ValueError("Error creating Twilight Struggle game. Optional cards parameter must be a 1 or a 0.")
        self.optional_cards = True if opt == 1 else False

        self.__create_countries()

    def __create_countries(self):
        with open('countries/country_list.csv', 'r') as handle:
            header = handle.readline()
            lines = handle.read().splitlines()

        for line in lines:
            country = TwilightStruggleCountry(*line.split(','))
            countries.update({country.name: country})

    # Functions to modify influence
    def check_for_control(self, c):
        if (countries[c].usa_influence - countries[c].ussr_influence) >= countries[c].stability:
            countries[c].controlled = 'usa'
        elif (countries[c].ussr_influence - countries[c].usa_influence) >= countries[c].stability:
            countries[c].controlled = 'ussr'
        else:
            countries[c].controlled = ''

    def add_influence(self, c, s, i):
        if s == 'usa':
            countries[c].usa_influence += i
        elif s == 'ussr':
            countries[c].ussr_influence += i

        self.check_for_control(c)

    def add_influence_to_control(self, c, s):
        if s == 'usa':
            countries[c].usa_influence = countries[c].ussr_influence + countries[c].stability
        elif s == 'ussr':
            countries[c].ussr_influence = countries[c].usa_influence + countries[c].stability

        self.check_for_control(c)

    def remove_influence(self, c, s, i):
        if s == 'usa':
            countries[c].usa_influence -= i
            if countries[c].usa_influence < 0:
                countries[c].usa_influence = 0
        elif s == 'ussr':
            countries[c].ussr_influence -= i
            if countries[c].ussr_influence < 0:
                countries[c].ussr_influence = 0

        self.check_for_control(c)

    def remove_all_influence(self, c, s):
        if s == 'usa':
            countries[c].usa_influence = 0
        elif s == 'ussr':
            countries[c].ussr_influence = 0

        self.check_for_control(c)


game = TwilightStruggleGame("default_name", "2022-01-27", "0")


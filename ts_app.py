# App to play twilight struggle
import random

defcon = 5
score = 0

game_active = True

cards = {}
countries = {}
players = {}
sides = {}
opponent = {'usa': 'ussr', 'ussr': 'usa'}


def adjust_defcon(adjustment_value):
    global defcon
    defcon = defcon + adjustment_value

    # Adjust defcon to 5 if above 5
    if defcon > 5:
        defcon = 5

    if defcon < 2:
        if sides['usa'].phasing:
            sides['ussr'].winner = True
        elif sides['ussr'].phasing:
            sides['usa'].winner = True

        global game_active
        game_active = False


class Card:
    """Base class for a generic card in a game"""

    def __init__(self, n):
        self.name = n

    def __repr__(self):
        return "<Card: %s>" % self.name

    def __str__(self):
        return self.name


class CardGame:
    """Base class for a collection of Card Pile objects"""

    def __init__(self, n, d):
        self.name = n
        self.date = d
        self.piles = {}

    def add_pile(self, p):
        if isinstance(p, CardPile):
            self.piles.update({p.name: p})
        else:
            raise ValueError("Could not add pile " + str(p) + " to card game " + str(self.name) + ".")

    def remove_pile(self, p):
        try:
            self.piles.pop(p.name)
        except ValueError:
            raise ValueError("Could not remove pile " + str(p) + " from card game " + str(self.name) + ".")

    def get_pile(self, n):
        pile = self.piles[n]
        return pile

    def __repr__(self):
        string = "<CardGame: %s on %s>" % (self.name, self.date)
        for pile in self.piles:
            string += "\t" + repr(pile) + "\n"
        return string

    def __str__(self):
        return "%s on %s" % (self.name, self.date)


class CardPile:
    """Base class for a collection of Card objects"""
    def __init__(self, n, card_dict={}):
        self.name = n
        self.cards = {}
        for card in card_dict:
            self.add_card(card)

    def add_card(self, c):
        if isinstance(c, Card):
            self.cards.update({c.name: c})
        else:
            raise ValueError("Could not add card " + str(c) + " to card pile " + str(self) + ".")

    def remove_card(self, c):
        try:
            self.cards.pop(c.name)
        except ValueError:
            raise ValueError("Could not remove card" + str(c) + " from card pile " + str(self) + ".")

    def random_card(self):
        card_list = self.cards
        card = random.choice(list(card_list.values()))
        return card

    def get_card(self, n):
        card = self.cards[n]
        return card

    def get_pile_size(self):
        return len(self.cards)

    def get_cards_in_pile(self):
        cards_in_pile = self.cards
        return cards_in_pile

    def __repr__(self):
        string = "<CardPile: %s>" % self.name
        for card in self.cards:
            string += "\t" + repr(card) + "\n"
        return string

    def __str__(self):
        return self.name


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


class TwilightStruggleCard(Card):
    """Class of cards specific to the game Twilight Struggle"""

    def __init__(self, n, no, p, e, o, r, opt):
        Card.__init__(self, n)

        if not no.isdigit():
            raise ValueError("Error creating Twilight Struggle Card. Number parameter must be a number")
        self.number = int(no)

        if p not in ['early war', 'mid war', 'late war']:
            raise ValueError("Error creating Twilight Struggle Card. Period parameter must be one of early war, mid war, or late war")
        self.period = p

        if e not in ['scoring', 'usa', 'ussr', 'neutral']:
            raise ValueError("Error creating Twilight Struggle Card. Event type must be scoring, usa, ussr, or neutral")
        self.event_type = e

        if not o.isdigit() and (int(o) > 4 or int(o) < 0):
            raise ValueError("Error creating Twilight Struggle Card. Ops must be a number between 0 and 4")
        self.ops = int(o)

        if not r.isdigit() and int(r) != 1 and int(r) != 0:
            raise ValueError("Error creating Twilight Struggle Card. Removed parameter must be a 1 or a 0")
        self.removed = True if int(r) == 1 else False

        if not opt.isdigit() and int(opt) != 1 and int(opt) != 0:
            raise ValueError("Error creating Twilight Struggle Card. Optional parameter must be a 1 or 0")
        self.optional = True if int(opt) == 1 else False

        self.played = False


class TwilightStrugglePlayer(Player):
    """Class of players specific to Twilight Struggle"""

    def __init__(self, n, s):
        Player.__init__(self, n)

        if s not in ['usa', 'ussr']:
            raise ValueError("Error creating Twilight Struggle country. Controlled must be 'usa' or 'ussr'")
        self.side = s

        # Set phasing player to false
        self.phasing = False

        # Set space level to 0
        self.space_level = 0

        # Set winner to false
        self.winner = False


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

        self.borders = []


class TwilightStruggleGame(CardGame):
    """Class of an individual game of Twilight Struggle"""

    turns = 10
    action_rounds = {1: 6, 2: 6, 3: 6, 4: 7, 5: 7, 6: 7, 7: 7, 8: 7, 9: 7, 10: 7}

    def __init__(self, n, d, opt):
        CardGame.__init__(self, n, d)

        if not opt.isdigit() and int(opt) != 1 and int(opt) != 0:
            raise ValueError("Error creating Twilight Struggle game. Optional cards parameter must be a 1 or a 0.")
        self.optional_cards = True if opt == 1 else False

        self.__create_piles()
        self.__create_cards()
        self.__create_countries()
        self.__create_players()

    def __create_cards(self):
        with open('cards/card_list.csv', 'r') as handle:
            header = handle.readline()
            lines = handle.read().splitlines()

        for line in lines:
            card = TwilightStruggleCard(*line.split(','))
            if not self.optional_cards and card.optional:
                continue
            start_pile = self.get_pile(card.period)
            if not start_pile:
                raise ValueError("Error adding card " + str(card) + " to pile " + str(start_pile) + ".")
            start_pile.add_card(card)
            cards.update({card.name: card})

    def __create_countries(self):
        with open('countries/country_list.csv', 'r') as c_handle:
            country_header = c_handle.readline()
            c_lines = c_handle.read().splitlines()

        for c_line in c_lines:
            country = TwilightStruggleCountry(*c_line.split(','))
            countries.update({country.name: country})

        with open('countries/borders_list.csv', 'r') as b_handle:
            b_header = b_handle.readline()
            b_lines = b_handle.read().splitlines()

        for b_line in b_lines:
            borders_list = b_line.split(',')
            borders_list[:] = [x for x in borders_list if x]
            countries[borders_list[0]].borders = borders_list[1:]

    def __create_piles(self):
        pile_list = ['early war', 'mid war', 'late war', 'deck', 'discard', 'removed', 'usa hand', 'ussr hand']

        for pile in pile_list:
            self.add_pile(CardPile(pile))

    def __create_players(self):
        # TODO - Change the "create players" function to allow for user input

        player_list = [['Player 1', 'ussr'], ['Player 2', 'usa']]

        for p_list in player_list:
            player = TwilightStrugglePlayer(p_list[0], p_list[1])
            players.update({player.name: player})
            sides.update({player.side: player})

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

    # Functions to modify the score
    def check_game_end(self):
        global game_active
        if score >= 20:
            sides['usa'].winner = True
            game_active = False
        elif score <= -20:
            sides['ussr'].winner = True
            game_active = False

    def change_score(self, s, p):
        global score
        if s == 'usa':
            score = score + p
        elif s == 'ussr':
            score = score - p

        self.check_game_end()

    # Functions for space race
    def space_race_awards(self, s):
        space_race_points = {1: [2, 1], 3: [2, 0], 5: [3, 1], 7: [4, 2], 8: [2, 0]}
        level = sides[s].space_level

        if level in space_race_points:
            if sides[opponent[s]].space_level < level:
                self.change_score(s, space_race_points[level][0])
            if sides[opponent[s]].space_level >= level:
                self.change_score(s, space_race_points[level][1])

    def increase_space_level(self, s):
        if s == 'usa':
            sides['usa'].space_level += 1
            self.space_race_awards('usa')
        elif s == 'ussr':
            sides['ussr'].space_level += 1
            self.space_race_awards('ussr')
        else:
            raise ValueError("Side must be 'usa' or 'ussr'")

    # Functions for checking access
    def countries_with_influence(self, s):
        country_list = []
        for country in countries.values():
            if s == 'usa' and country.usa_influence > 0:
                country_list.append(country.name)
            elif s == 'ussr' and country.ussr_influence > 0:
                country_list.append(country.name)

        return country_list

    def accessible_countries(self, s):
        influenced_countries = self.countries_with_influence(s)
        accessible_countries = influenced_countries.copy()

        for country in influenced_countries:
            border_list = countries[country].borders
            for border in border_list:
                if border not in accessible_countries and border != 'USA' and border != 'USSR':
                    accessible_countries.append(border)

        return accessible_countries

    # Functions for moving cards around
    def which_pile(self, c):
        for pile in self.piles:
            cards_in_pile = self.piles[pile].get_cards_in_pile()

            if c.name in cards_in_pile:
                return pile

    def move_card(self, c, pile_name):
        current_pile = self.which_pile(c)
        self.piles[current_pile].remove_card(c)
        self.piles[pile_name].add_card(c)


game = TwilightStruggleGame("default_name", "2022-01-27", "0")

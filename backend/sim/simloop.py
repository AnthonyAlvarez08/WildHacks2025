"""
Will contain the actual simulation here

"""
from sim.country import Country
from sim.request import Request
import sim.constants as constants
from sim.adjmat import AdjacencyMatrix
import random


# instantiate initial countries and such

usa = Country("USA", 347, 1.0068, 30338, 1)
saudi_arabia = Country("Saudi Arabia", 35, 1.0165, 1138, 1)
japan = Country("Japan", 123, -1.0041, 4390, 7)
brazil = Country("Brazil", 212, 1.0061, 2308, 4)
ukraine = Country("Ukraine", 39, -1.0052, 189, 7)
malaysia = Country("Malaysia", 36, 1.0101, 488, 3)
haiti = Country("Haiti", 12, 1.0118, 24, 9)
india = Country("India", 1463, 1.0070, 4270, 4)
ethiopia = Country("Ethiopia", 135, 1.0242, 238, 7)

class SimStates:
    CompRequests = 1
    PlayerPhase = 2
    CompRequests = 3

class SimLoop:
    def __init__(self):
        self.tariffs = AdjacencyMatrix()
        self.alliances = AdjacencyMatrix(symmetrical=True)

        # accces as [importer][exporter] = {}
        self.food_trading = AdjacencyMatrix()

        # initialize all the matrices
        sizes = self.tariffs.size
        for i in range(sizes):
            for j in range(sizes):
                if i != j:
                    self.tariffs.update(i, j, 0)
                    self.alliances.update(i, j, False)
                    self.food_trading.update(i, j, {constants.VEG: 0, constants.MEAT: 0, constants.GRAIN: 0})


        self.year = 0
        
        self.state = SimStates.CompRequests

        self.countries: list[Country] = [usa, saudi_arabia, japan, brazil, ukraine, malaysia, haiti, india, ethiopia]

        self.request_list: list[Request] = []

        self.log = []


    """
    Player actions section
    """

    def request_aid(self, player: Country, target: Country, amount: float) -> bool:
        if self.state != SimStates.PlayerPhase or not player.player_controlled:
            return False
        
    
        

    def give_aid(self, player: Country, target: Country, amount: float) -> bool:
        if self.state != SimStates.PlayerPhase or not player.player_controlled:
            return False
        
        if player.money < amount:
            return False
        player.money -= amount
        target.money += amount

    def change_tariffs(self, player: Country, target: Country, amount: float):
        if self.state != SimStates.PlayerPhase or not player.player_controlled:
            return
        
        self.tariffs.update(player.id, target.id, amount)

    def invest_in_agriculture(self, player: Country) -> bool:
        if self.state != SimStates.PlayerPhase or not player.player_controlled:
            return False
        return player.invest_in_agriculture()
    
    def invest_money_prod(self, player: Country) -> bool:
        if self.state != SimStates.PlayerPhase or not player.player_controlled:
            return False
        return player.invest_in_money_prod()

    def end_player_turn(self):
        self.state = SimStates.CompReact

        self._comp_react()

        self.state = SimStates.CompRequests
        # I think advance one year should be called from controller otherwise it will run out of stack space eventually from all the nested function calls



    """
    Other Sim Functions
    """

    def advance_one_year(self):
        """
        
        Returns:
        (insecure, disaster) tuple with lists of countries that are insecure or in disaster
        """

        insecure = []
        disaster = []
        for i in self.countries:

            # do all imports and exports with tariffs and shit
            for b in self.countries:
                if i.id != b.id:
                    # i is importer, b is exporter
                    tariff = self.tariffs.get(i.id, b.id)

                    # get transaction money
                    export = self.food_trading.get(i.id, b.id) # is dict
                    costs = 0
                    for idx in [constants.VEG, constants.MEAT, constants.GRAIN]:
                        costs += constants.PRICES[idx] *  export[idx]

                    costs *= (1 + tariff)

                    # check failure cases for transactions
                    if i.money < costs:
                        self.log.append(f"Couldnt complete transaction: {i.name} importing {export} from {b.name} with tariff {tariff}")
                        continue

                    can_export = True
                    for idx in [constants.VEG, constants.MEAT, constants.GRAIN]:
                        if b.food[idx] < export[idx]:
                            can_export = False
                    if not can_export:
                        self.log.append(f"Couldnt complete transaction: {i.name} importing {export} from {b.name} with tariff {tariff}")
                        continue





            i.advance_one_year()

            if not i.is_food_secure():
                insecure.append(i)

            if i.in_disaster:
                disaster.append(i)

            
        self.log.append((f"Food inscure countries",  [j.name for j in insecure]))
        self.log.append((f"Countries in disaster", [j.name for j in disaster]))

        self.year += 1

        self.state = SimStates.CompRequests

        self._comp_requests(insecure, disaster)

        self.state = SimStates.PlayerPhase

        return insecure, disaster
    
    def _comp_requests(self, insecure: list[Country], indisaster: list[Country]):
        for country in indisaster:
            # for now always try to fix the disaster if have the money for it
            if country.money >= constants.DISASTER_MONEY:# and random.randint(0, 100) % 2 == 0:
                res = country.try_end_disaster()

                if res:
                    self.log.append(f"{country.name} successfully ended disaster")
                else:
                    self.log.append(f"{country.name} tried and failed to end the disaster")
            else:
                # request aid
                pass

        
        insecureids = [i.id for i in insecure]
        secure = [i for i in self.countries if not i.id in insecureids]
        for country in insecure:

            # try to request trade?
            
            
            for resource in [constants.VEG, constants.MEAT, constants.GRAIN]:
                if country.food[resource] / country.population < constants.FOOD_SECURE[resource]:
                    # find a country with enough food to give you


                    # food needed
                    food_needed = (constants.FOOD_SECURE[resource] - country.food[resource] / country.population) * country.population

                    target = random.choice([i for i in self.countries if i.food[resource] > food_needed])

                    self.request_list.append(Request(country, target, food_needed, resource))



    def _comp_react(self):
        
        for rq in self.request_list:
            # processs each request

            requester = rq.requester
            recepient = rq.recepient

            # check if requester has surplus
            surplus = (recepient.food[rq.resource] / recepient.population - constants.FOOD_SECURE[rq.resource]) * recepient.population
            if surplus > 0:
                # random slice of their surplus I guess?

                trade_amount = round(random.random() * surplus)


                # accepts the request
                self.food_trading.update(requester, recepient, trade_amount)
            else:
                # deny request, which means do nothing
                pass
    

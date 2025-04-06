import sim.constants as constants
import random, math, time

random.seed(20)


class Country:

    country_id = 1

    def __init__(self, 
                 name:str, 
                 population:float, 
                 population_growth_rate:float,
                 starting_money, 
                 risk,
                 arable_land,
                 player_controlled=False,
                 food_level=1,
                 years_in_disaster=0,
                 other_attributes=[]):
        
        self.name = name
        self.population = population * 100
        self.initial_population = population * 100
        self.population_growth_rate = population_growth_rate
        self.money = starting_money
        self.income_rate = starting_money / 10

        self.production_rate = dict() # proportional to arable land?
        self.production_rate[constants.VEG] = starting_money/population * arable_land
        self.production_rate[constants.MEAT] = starting_money/population * arable_land
        self.production_rate[constants.GRAIN] = starting_money/population * arable_land
        print(self.production_rate)

        self.food = dict()
        self.food[constants.GRAIN] = 0
        self.food[constants.VEG] = 0
        self.food[constants.MEAT] = 0

        self.risk = risk
        self.in_disaster = False
        self.years_in_disaster = years_in_disaster

        self.agriculture_tech_level = food_level # affects food
        self.other_attributes = other_attributes

        self.player_controlled = player_controlled

        self.id = Country.country_id
        Country.country_id += 1



        """
        TODO: raise tech level
        spend money for recovery
        try to end war
        """

    def give_resource(self, other_country: "Country", amount: int, _type):
        if not _type in [constants.GRAIN, constants.VEG, constants.MEAT]:
            raise ValueError
        if amount > self.food[_type]:
            raise Exception("not enough food to give")
        
        self.food[_type] -= amount
        other_country.food[_type] += amount


    def is_food_secure(self):
        for i in [constants.GRAIN, constants.VEG, constants.MEAT]:
            if self.food[i] / self.population < constants.FOOD_SECURE[i]:
                return False
        return True
    


    def advance_one_year(self):
        random.seed(time.time())
        pop_mult = 1
        food_mult = self.agriculture_tech_level
        money_mult = 1

        if self.in_disaster:
            money_mult *= constants.DISASTER_MONEY_DEBUF
            food_mult *= constants.DISASTER_PRODUCTION_DEBUF
            pop_mult *= constants.DISASTER_POPULATION_DECREASE

        # consume current food reservers
        for resource in [constants.GRAIN, constants.VEG, constants.MEAT]:
            self.food[resource] -= self.population * constants.FOOD_SECURE[resource]

        # causes citizens to die of starvation if food is insecure
        if any([i < 0 for i in self.food.values()]):
            died = min(self.food.values()) / self.population
            self.population -= died

        # reset back to 0 if needed
        for resource in [constants.GRAIN, constants.VEG, constants.MEAT]:
            self.food[resource] = max(0, self.food[resource])

        # rots leftover food
        for resource in [constants.GRAIN, constants.VEG, constants.MEAT]:
            self.food[resource] *= constants.FOOD_REMAINING_AFTER_ROT
            
            

        # grow population, get money and produce
        if self.population * pop_mult > self.initial_population * 0.5:
            self.population *= self.population_growth_rate * pop_mult
        self.money += self.income_rate * money_mult
        self.money = math.ceil(self.money)
        self.population = math.ceil(self.population)
        for i in [constants.GRAIN, constants.VEG, constants.MEAT]:
            self.food[i] += self.production_rate[i] * food_mult
            self.food[resource] = math.ceil(self.food[resource])



        # make them invest aggresively
        if random.random() < (math.atan(self.money / 500) / math.pi * 2):
            self.invest_in_money_prod()
            self.invest_in_agriculture()
        

        if self.risk / 30 > random.random():
            self.in_disaster = True


    def invest_in_agriculture(self) -> bool:
        if self.money < constants.INVESTING_COST:
            return False
        if random.random() <= constants.INVESTING_SUCCESS_RATE:
            for i in [constants.GRAIN, constants.VEG, constants.MEAT]:
                self.production_rate[i] *= constants.REASEARCH_MULT
            return True
        return False
    
    def invest_in_money_prod(self) -> bool:
        if self.money < constants.INVESTING_COST:
            return False
        if random.random() <= constants.INVESTING_SUCCESS_RATE:
            self.income_rate *= constants.REASEARCH_MULT
            return True
        return False

    def try_end_disaster(self) -> bool:
        if not self.in_disaster:
            return True
        
        if self.money > constants.DISASTER_MONEY:
            self.money -= constants.DISASTER_MONEY

            self.in_disaster = random.random() <= constants.DISASTER_FIXING_CHANCE
            return not self.in_disaster
        return False
        
        
    


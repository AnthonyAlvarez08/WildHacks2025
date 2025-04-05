from sim.country import Country

class Request:

    def __init__(self, requester: Country, recepient: Country, amount: float, resource):
        self.amount = amount
        self.requester = requester
        self.recepient = recepient
        self.resource = resource

        
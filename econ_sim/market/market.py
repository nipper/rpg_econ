from econ_sim.actor import Actor

class MarketPlace():

    def __init__(self):

        self.actors = []

    def register_actor(self,agent: Actor):
        self.actors.append(agent)


    def production(self):

        [x.production() for x in self.actors]

    def generate_offers(self):

        [x.generate_offer(self) for x in self.actors]





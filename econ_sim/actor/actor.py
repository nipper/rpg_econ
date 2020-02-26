import random
from loguru import logger
from econ_sim.commodities import Commodities as cd
from collections import defaultdict


class Actor:
    def __init__(self, inventory: defaultdict = None):

        if inventory:
            self.inventory = defaultdict(lambda: 0, inventory)
        else:
            self.inventory = defaultdict(lambda: 0)
        self.money = 0

    def production(self):
        self._production()
        logger.info(
            f"{id(self)} - {self._class_name} : {dict(self.inventory)} - Money: {self.money}"
        )

    def _proudction(self):
        raise NotImplementedError

    def generate_offer(self, market_place):
        print(market_place)

    def break_tools(self, prob):

        tools_break = random.random() <= prob
        if tools_break:
            self.inventory["tools"] = self.inventory["tools"] - 1
            logger.info(f"{id(self)} - Tools break!")

        return tools_break

    def produce(self, commodity: cd, value: int) -> None:

        self.inventory[commodity] = self.inventory[commodity] + value

    def consume(self, commodity: cd, value: int) -> None:

        self.inventory[commodity] = self.inventory[commodity] - value

    def has(self, commodity: cd):

        return self.inventory[commodity] > 0

    def get(self, commodity: cd):

        return self.inventory[commodity]

    def transform(self, source: cd, dest: cd, max_val: int = None):

        if max_val:
            transform_amount = min(max_val, self.get(source))
        else:
            transform_amount = self.get(source)

        self.produce(cd.Tool, transform_amount)
        self.consume(cd.Metal, transform_amount)


class Farmer(Actor):
    def __init__(self, inventory):
        self._class_name = "Farmer"
        super().__init__(inventory)

    def _production(self):

        if self.has(cd.Wood) and self.has(cd.Tool):
            self.produce(cd.Food, 4)
            self.consume(cd.Wood, 1)
            self.break_tools(0.1)

        elif self.has(cd.Wood) and not self.has(cd.Tool):
            self.produce(cd.Food, 2)
            self.consume(cd.Wood, 1)

        else:
            self.money = self.money - 2


class Miner(Actor):
    def __init__(self, inventory):
        self._class_name = "Miner"
        super().__init__(inventory)

    def _production(self):

        if self.has(cd.Food) and self.has(cd.Tool):
            self.produce(cd.Ore, 4)
            self.consume(cd.Food, 1)
            self.break_tools(0.1)

        elif self.has(cd.Food) and not self.has(cd.Tool):
            self.produce(cd.Ore, 2)
            self.consume(cd.Food, 1)

        else:
            self.money = self.money - 2


class Refiner(Actor):
    def __init__(self, inventory):
        self._class_name = "Refiner"
        super().__init__(inventory)

    def _production(self):

        if self.has(cd.Food) and self.has(cd.Tool):
            self.transform(cd.Ore, cd.Metal)
            self.consume(cd.Food, 1)
            self.break_tools(0.1)

        elif self.has(cd.Food) and not self.has(cd.Tool):
            self.transform(cd.Ore, cd.Metal, 2)
            self.consume(cd.Food, 1)

        else:
            self.money = self.money - 2


class Woodcutter(Actor):
    def __init__(self):
        self._class_name = "Woodcutter"
        super().__init__()

    def _production(self):

        if self.has(cd.Food) and self.has(cd.Tool):
            self.produce(cd.Wood, 2)
            self.consume(cd.Food, 1)
            self.break_tools(0.1)

        elif self.has(cd.Food) and not self.has(cd.Tool):
            self.produce(cd.Wood, 1)
            self.consume(cd.Food, 1)

        else:
            self.money = self.money - 2


class Blacksmith(Actor):
    def __init__(self, inventory):
        self._class_name = "Blacksmith"
        super().__init__(inventory)

    def _production(self):

        if self.has(cd.Food):
            self.transform(cd.Metal, cd.Tool)
            self.consume(cd.Food, 1)
        else:
            self.money = self.money - 2

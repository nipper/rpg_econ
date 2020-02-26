import econ_sim.actor as actors
import econ_sim.market as market
from econ_sim.commodities import Commodities as cd

test_market = market.MarketPlace()

farmer = actors.Farmer(inventory={cd.Wood: 2, cd.Tool: 1})

test_market.register_actor(farmer)

test_market.production()
test_market.production()
test_market.production()
test_market.production()
test_market.generate_offers()

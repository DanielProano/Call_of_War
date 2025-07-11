from units import Unit

class Game:
	def __init__(self, game_name, country, faction, resources, production, upkeep):
		self.game_name = game_name
		self.country = country
		self.faction = faction
		self.resources = Resources(resources, production, upkeep)
		self.units = []
	def update(self, game_name, country, faction):
		self.game_name = game_name
		self.country = country
		self.faction = faction

class Resources:
	def __init__(self, resources=None, production=None, upkeep=None):
		keys = ["corn", "gas", "steel", "cash", "manpower", "war_bonds"]
		self.resources = {key: 0 for key in keys}
		self.production = {key: 0 for key in keys}
		self.upkeep = {key: 0 for key in keys}

		if resources:
			self.resources.update(resources)
		if production:
			self.production.update(production)
		if upkeep:
			self.upkeep.update(upkeep)
	def update(self, resources=None, production=None, upkeep=None):
		if resources:
			self.resources.update(resources)
		if production:	
			self.production.update(production)
		if upkeep:
			self.upkeep.update(upkeep)
	def day_change(self):
		for resource, value in self.resources:
			self.resources[resource] += self.production[resource] - self.upkeep[resource]

setup = Unit("Game 1", 1)

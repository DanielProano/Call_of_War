import units

class Game:
	def __init__(self, game_name, country, faction, resources=None, production=None, upkeep=None):
		self.game_name = game_name
		self.country = country
		self.faction = faction
		self.resources = Resources(resources, production, upkeep)
		self.units = []
		self.enemy_units = []
		self.buildings = []
	def update(self, game_name, country, faction):
		self.game_name = game_name
		self.country = country
		self.faction = faction
	def add_unit(self, unit_cls, level, territory=None, buildings=None, health=None):
		unit = unit_cls.create(level, self, territory, buildings, health)
		if unit:
			self.units.append(unit)
			return unit
		print("Failed to create Unit")
		return None
	def add_building(self, building_cls, level, *args, affect_resources=True):
		building = building_cls.create(level, self, *args, affect_resources=affect_resources)
		if building:
			self.buildings.append(building)
			return building
		print("Failed to create Building")
		return None
	def faction_info(self):
		print(f"Faction Information\n{'-' * 35}\nAxis\n\t+Increased Unit Damage\n\t+Increased Unit Hitpoints\n\t-Increased Unit Costs\n{"-" * 35}\nAllies\n\t+Decreased Production Times\n\t+Decreased Research Costs & Times\n\t+Decreased Upgrade Costs & Times\n\t-Decreased Unit Speed\n{"-" * 35}\nComintern\n\t+Decreased Unit Costs\n\t+Decreased unit upkeep\n\t-Decreased Unit Damage\n{"-" * 35}\nPan-asian\n\t+Increased Unit Speed\n\t+Increased Unit View Range\n\t+Increased Unit Terrain Bonus\n\t-Decreased Unit Hitpoints\n{'-' * 35}\n")
	def __str__(self):
		return f"Game Information\n{'-' * 50}\nGame: {self.game_name}\nCountry: {self.country}\nFaction: {self.faction}\n{'-' * 50}\n"

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
	def add(self, resources=None, production=None, upkeep=None):
		if resources:
			for key, value in resources.items():
				self.resources[key] += value
		if production:
			for key, value in production.items():
				self.production[key] += value
		if upkeep:
			for key, value in upkeep.items():
				self.upkeep[key] += value
	def subtract(self, resources=None, production=None, upkeep=None):
		unable_to_pay = False
		depleted_resource = {}
		if resources:
			for key, value in resources.items():
				self.resources[key] -= value
				if self.resources[key] < 0:
					unable_to_pay = True
					depleted_resource[key] = value
		if production:
			for key, value in production.items():
				self.production[key] -= value
				if self.production[key] < 0:
					unable_to_pay = True
					depileted_resource[key] = value
		if upkeep:
			for key, value in upkeep.items():
				self.upkeep[key] -= value
				if self.upkeep[key] < 0:
					unable_to_pay = True
					depleted_resource[key] = value
		if unable_to_pay:
			print(f"{'*' * 50}\n\nCannot afford Unit, need at least:")
			for key, value in depleted_resource.items():
				print(f"\t~ {value} {key}\n")
			print(f"{'*' * 50}\n")
			if resources:
				self.add(resources=resources)
			if production:
				self.add(production=production)
			if upkeep:
				self.add(upkeep=upkeep)
			return False
		return True
	def day_change(self):
		for key, value in self.resources.items():
			self.resources[key] += self.production[key] - self.upkeep[key]
	def __str__(self):
		return f"Resource Information\n{'-' * 50}\nResources:\n\tCorn: {self.resources['corn']}\n\tGas: {self.resources['gas']}\n\tSteel: {self.resources['steel']}\n\tCash: {self.resources['cash']}\n\tManpower: {self.resources['manpower']}\n\tWar Bonds: {self.resources['war_bonds']}\nProduction:\n\tCorn: {self.production['corn']}\n\tGas: {self.production['gas']}\n\tSteel: {self.production['steel']}\n\tCash: {self.production['cash']}\n\tManpower: {self.production['manpower']}\n\tWar Bonds: {self.production['war_bonds']}\n Upkeep:\n\tCorn: {self.upkeep['corn']}\n\tGas: {self.upkeep['gas']}\n\tSteel: {self.upkeep['steel']}\n\tCash: {self.upkeep['cash']}\n\tManpower: {self.upkeep['manpower']}\n\tWar Bonds: {self.upkeep['war_bonds']}\n{'-' * 50}\n"

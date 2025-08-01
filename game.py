import units, stack

class Game:

	'''
	Initialize the game to have custom name, your starting country
	& faction, along with your starting resources and upkeep.
	'''

	def __init__(self, game_name, country, faction, day=1, resources=None, production=None, upkeep=None):
		self.game_name = game_name
		self.country = country
		self.faction = faction
		self.day = day
		self.resources = Resources(resources, production, upkeep)
		self.units = []
		self.enemy_units = []
		self.buildings = []
		self.stacks = []

	def update(self, game_name=None, country=None, faction=None, day=None):
		if game_name:
			self.game_name = game_name
		if country:
			self.country = country
		if faction:
			self.faction = faction
		if day:
			self.day = day

	'''
	Official way to add and delete units from game
	'''

	def add_unit(self, unit_cls, level, territory=None, buildings=None, health=None, owner=True):
		unit = unit_cls.create(level, self, territory=territory, buildings=buildings, health=health)
		if unit and owner:
			self.units.append(unit)
			return unit
		elif unit and not owner:
			self.enemy_units.append(unit)
			return unit
		return None

	def delete_unit(self, unit_obj):
		if not self.units.remove(unit_obj):
				return True
		return False
	
	'''
	Add buildings that affect your resource production & units
	'''

	def add_building(self, building_cls, level, *args, affect_resources=True, untracked_resources=False):
		building = building_cls.create(level, self, *args, affect_resources=affect_resources, untracked_resources=untracked_resources)
		if building:
			self.buildings.append(building)
			return building
		return None
	def delete_building(self, building_obj):
		if not self.buildings.remove(building_obj):
			return True
		return False

	'''
	Adds stacks of units to the game
	'''

	def create_stack(self, territory=None, buildings=None, owner=True):
		stack1 = stack.Stack(self, territory=territory, buildings=buildings)
		if stack1:
			self.stacks.append(stack1)
			return stack1
		else:
			return None
	'''
	Get the general info about the faction pros and cons
	'''

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

	'''
	Returns the resources that
	are depleted as a dictionary.
	This is successful if it
	return None
	'''

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
			if resources:
				self.add(resources=resources)
			if production:
				self.add(production=production)
			if upkeep:
				self.add(upkeep=upkeep)
			return depleted_resource
		return None

	'''
	Day change happens every 24 hrs and should update amount of resources
	based on production and upkeep
	'''

	def day_change(self):
		for key, value in self.resources.items():
			self.resources[key] += self.production[key] - self.upkeep[key]
	def __str__(self):
		return f"Resource Information\n{'-' * 50}\nResources:\n\tCorn: {self.resources['corn']}\n\tGas: {self.resources['gas']}\n\tSteel: {self.resources['steel']}\n\tCash: {self.resources['cash']}\n\tManpower: {self.resources['manpower']}\n\tWar Bonds: {self.resources['war_bonds']}\nProduction:\n\tCorn: {self.production['corn']}\n\tGas: {self.production['gas']}\n\tSteel: {self.production['steel']}\n\tCash: {self.production['cash']}\n\tManpower: {self.production['manpower']}\n\tWar Bonds: {self.production['war_bonds']}\nUpkeep:\n\tCorn: {self.upkeep['corn']}\n\tGas: {self.upkeep['gas']}\n\tSteel: {self.upkeep['steel']}\n\tCash: {self.upkeep['cash']}\n\tManpower: {self.upkeep['manpower']}\n\tWar Bonds: {self.upkeep['war_bonds']}\n{'-' * 50}\n"

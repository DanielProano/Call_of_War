

class Unit:
	def __init__(self, level, game):
		self.level = level
		self.game = game		### Python game object for access to important information like faction ### 

	def pay_costs(self):
		if self.daily_costs and self.production_costs:
			payment = self.game.resources.subtract(resources=self.production_costs)
			if payment:
				self.game.resources.add(upkeep=self.daily_costs)
				self.can_afford_unit = True
			else:
				self.can_afford_unit = False
		else:
			self.can_afford_unit = False
	def research_unit(self):
		if self.research_costs:
			payment = self.game.resources.subtract(resources=self.research_costs)
			if payment:
				self.can_afford_unit = True
			else:
				self.can_afford_unit = False
		else:
			print("No research costs available")
			self.can_afford_unit = False
	def upgrade(self, level=None):
		if level:
			self.level = level
		else:
			self.level += 1
		self.update_stats()
	def attack(self, enemy_unit, territory, buildings):
		hp = self.terrain_effects[territory]['HP']
		if self.terrain_effects[territory]['strength']:
			hp = hp * self.terrain_effects[territory]['strength']
		if buildings:
			pass
	def __str__(self):
		basic = f"{'-' * 50}\n"
		if self.name:
			basic += (f"Unit Name: {self.name}\n")
		basic += (f"Unit level: {self.level}\nUnit Faction: {self.game.faction}\nUnit Health: {self.health}\nUnit Speed: {self.speed}\nUnit View Range: {self.view_range}\nUnit Attack Range: {self.attack_range}\nDay available: {self.day_available}\n")
		if self.combat:
			combat_info = (f"{'=' * 35}\nAttack Unarmored: {self.combat['unarmored']['attack']}\nDefense against Unarmored: {self.combat['unarmored']['defense']}\n{"=" * 35}\nAttack Light Armor: {self.combat['light_armor']['attack']}\nDefense Against Light Armor: {self.combat['light_armor']['defense']}\n{'=' * 35}\nAttack Heavy Armor: {self.combat['heavy_armor']['attack']}\nDefense Against Heavy Armor: {self.combat['heavy_armor']['defense']}\n{'=' * 35}\nAttack Airplane: {self.combat['airplane']['attack']}\nDefense Against Airplane: {self.combat['airplane']['defense']}\n{'=' * 35}\nAttack ship: {self.combat['ship']['attack']}\nDefense Against ships: {self.combat['ship']['defense']}\n{'=' * 35}\nAttack submarine: {self.combat['submarine']['attack']}\nDefense Against submarine: {self.combat['submarine']['defense']}\n{'=' * 35}\nAttack Buildings: {self.combat['buildings']['attack']}\nDefense Against Buildings: {self.combat['buildings']['defense']}\n{'=' * 35}\nAttack morale: {self.combat['morale']}\n{'=' * 35}\n\n\n{'=' * 35}\nResearch Costs: {self.research_costs}\nProduction Costs: {self.production_costs}\nDaily Costs: {self.daily_costs}\nTerrain Effects: {self.terrain_effects}\n{'=' * 35}\n")
			basic += combat_info
		basic += f"{"-" * 50}"
		return basic

class Militia(Unit):
	@classmethod
	def create(cls, level, game):
		unit = cls(level, game, build=False)
		unit.update_stats()
		unit.pay_costs()
		if not unit.can_afford_unit:
			return None
		return unit

	def __init__(self, level, game, build=True):
		super().__init__(level, game)
		self.name = "Militia"
		self.description = "The militia is a cheap defensive unit. Due to its slow speed and fast production time its main purpose is to defend own provinces and, due to its stealth characteristics, to ambush enemy attackers."
		self.special = "Is hidden (in hills, forests, or urban) as long as it is not fighting or uncovered by a scout unit of equal or higher level."

		if build:
			self.update_stats()
			self.pay_costs()
			if self.can_afford_unit:
				raise ValueError("Cannot afford Militia. Please do not try to bypass create() method! Instead, use game.add_unit()")
	def update_stats(self):
		match self.game.faction:
			case "Axis":
				match self.level:
					case 1:
						self.combat = {"unarmored": {"attack": 2.0, "defense": 3.0}, "light_armor": {"attack": 1.2, "defense": 1.8}, "heavy_armor": {"attack": 0.6, "defense": 0.9}, "airplane": {"attack": 1.2, "defense": 1.8}, "ship": {"attack": 0.6, "defense": 0.9}, "submarine": {"attack": 0.6, "defense": 0.9}, "buildings": {"attack": 0.5, "defense": 0.8}, "morale": 0.1}
						self.health = 17
						self.speed = 24
						self.view_range = 42
						self.attack_range = 0
						self.research_costs = {'steel': 350, 'corn': 850, 'cash': 1950}
						self.production_costs = {'corn': 550, 'manpower': 880, 'steel': 220, 'cash': 660}
						self.daily_costs = {'corn': 25, 'manpower': 40, 'steel': 10, 'cash': 30}
						self.minimum_production_time = 0.75
						self.research_time = 0.083
						self.day_available = 1
						self.terrain_effects = {'plains': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': 1.25}, 'mountains': {'HP': 17, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.25}, 'forest': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': 1.50}, 'urban': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'soldier', 'speed': None, 'strength': None}, 'Enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}
					case 2:
						self.combat = {"unarmored": {"attack": 3.7, "defense": 5.5}, "light_armor": {"attack": 2.0, "defense": 3.0}, "heavy_armor": {"attack": 1.2, "defense": 1.8}, "airplane": {"attack": 1.9, "defense": 2.8}, "ship": {"attack": 1.5, "defense": 2.2}, "submarine": {"attack": 1.5, "defense": 2.2}, "buildings": {"attack": 0.7, "defense": 1.0}, "morale": 0.1}
						self.health = 23
						self.speed = 28
						self.view_range = 42
						self.attack_range = 0
						self.research_costs = {'steel': 450, 'corn': 1000, 'cash': 2400}
						self.daily_costs = {'steel': 13, 'corn': 28, 'manpower': 43, 'cash': 33}
						self.production_costs = {'steel': 280, 'corn': 610, 'manpower': 940, 'cash': 720}
						self.minimum_production_time = 1
						self.research_time = 8
						self.day_available = 4
						self.terrain_effects = {'plains': {'HP': 23, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 23, 'armor': 'soldier', 'speed': None, 'strength': 1.25}, 'mountains': {'HP': 23, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.25}, 'forest': {'HP': 23, 'armor': 'soldier', 'speed': None, 'strength': 1.50}, 'urban': {'HP': 23, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'soldier', 'speed': None, 'strength': None}, 'Enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}
					case 3:
						self.combat = {"unarmored": {"attack": 6.7, "defense": 10.0}, "light_armor": {"attack": 3.5, "defense": 5.2}, "heavy_armor": {"attack": 2.3, "defense": 3.4}, "airplane": {"attack": 3.5, "defense": 5.2}, "ship": {"attack": 2.3, "defense": 3.4}, "submarine": {"attack": 2.3, "defense": 3.4}, "buildings": {"attack": 0.9, "defense": 1.3}, "morale": 0.2}
						self.health = 35
						self.speed = 32
						self.view_range = 42
						self.attack_range = 0
						self.research_costs = {'steel': 650, 'corn': 1400, 'cash': 3500}
						self.daily_costs = {'steel': 15, 'corn': 33, 'manpower': 43, 'cash': 38}
						self.production_costs = {'steel': 330, 'corn': 720, 'manpower': 940, 'cash': 830}
						self.minimum_production_time = 1.5
						self.research_time = 15
						self.day_available = 10
						self.terrain_effects = {'plains': {'HP': 35, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 35, 'armor': 'soldier', 'speed': None, 'strength': 1.25}, 'mountains': {'HP': 35, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.25}, 'forest': {'HP': 35, 'armor': 'soldier', 'speed': None, 'strength': 1.50}, 'urban': {'HP': 35, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'soldier', 'speed': None, 'strength': None}, 'Enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}
					case 4:
						self.combat = {"unarmored": {"attack": 11.5, "defense": 17.3}, "light_armor": {"attack": 6.7, "defense": 10.1}, "heavy_armor": {"attack": 4.0, "defense": 6.0}, "airplane": {"attack": 5.8, "defense": 8.7}, "ship": {"attack": 3.8, "defense": 5.7}, "submarine": {"attack": 3.8, "defense": 5.7}, "buildings": {"attack": 1.4, "defense": 2.1}, "morale": 0.2}
						self.health = 52
						self.speed = 36
						self.view_range = 42
						self.attack_range = 0
						self.research_costs = {'steel': 850, 'corn': 1900, 'cash': 4850}
						self.daily_costs = {'steel': 18, 'corn': 38, 'manpower': 45, 'cash': 45}
						self.production_costs = {'steel': 390, 'corn': 830, 'manpower': 990, 'cash': 990}
						self.minimum_production_time = 1.75
						self.research_time = 26
						self.day_available = 16
						self.terrain_effects = {'plains': {'HP': 52, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 52, 'armor': 'soldier', 'speed': None, 'strength': 1.25}, 'mountains': {'HP': 52, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.25}, 'forest': {'HP': 52, 'armor': 'soldier', 'speed': None, 'strength': 1.50}, 'urban': {'HP': 52, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'soldier', 'speed': None, 'strength': None}, 'Enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}

			case "Allies":
				pass
			case "Comintern":
				pass
			case "Pan-asian":
				pass
			case _:
				pass


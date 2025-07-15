

class Unit:
	def __init__(self, level, game, territory=None, buildings=None, health=None):
		self.level = level
		self.game = game		### Python game object for access to important information like faction ### 
		self.territory = territory
		self.buildings = buildings
		self.health = health
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
	def update(self, level=None, game=None, territory=None, buildings=None, health=None):
		if level:
			self.level = level
		if game:
			self.game = game
		if territory:
			self.territory = territory
		if buildings:
			self.buildings = buildings
		if health:
			self.health = health
	def fight(self, enemy_unit, attacking=True):
		
		# Determine the unit and enemy unit damage output

		if self.territory and self.terrain_effects[self.territory]['strength']:
			unit_damage = self.terrain_effects[self.territory]['strength'] * self.combat[enemy_unit.armor_class]['attack' if attacking else 'defense']
		else:
			unit_damage = self.combat[enemy_unit.armor_class]['attack' if attacking else 'defense']

		if enemy_unit.territory and enemy_unit.terrain_effects[enemy_unit.territory]['strength']:
			enemy_damage = enemy_unit.terrain_effects[enemy_unit.territory]['strength'] * enemy_unit.combat[self.armor_class]['defense' if attacking else 'attack']
		else:
			enemy_damage = enemy_unit.combat[self.armor_class]['defense' if attacking else 'attack']
		
		# Determine the unit and enemy health
		
		unit_health = self.health
		enemy_health = enemy_unit.health
	
		print(f"{'=' * 50}\n\t\t\tBATTLE\n{'=' * 50}\n")
		print(f"Pre-Battle Unit Health: {unit_health}\nDamage: {unit_damage}\nPre-Battle Enemy Health: {enemy_health}\nDamage: {enemy_damage}\n")	
		index = 1
		while unit_health > 0 and enemy_health > 0:
			unit_health -= enemy_damage
			enemy_health -= unit_damage
			print(f"{'-' * 15}\n")
			print(f"Round {index}\n")
			print(f"My Unit: {self.name}\n-Current Health: {unit_health}\nEnemy Unit: {enemy_unit.name}\n-Enemy Health: {enemy_health}\n")
			print(f"{'-' * 15}\n")
			index += 1
		self.health = unit_health
		enemy_unit.health = enemy_health
		if unit_health > 0:
			print(f"The Winner is: {self.name}\n")
			print(f"Health: {unit_health}\n")
			enemy_unit.kill()
		if enemy_health > 0:
			print(f"The Winner is: {enemy_unit.name}\n")
			print(f"Health: {enemy_health}\n")
			self.kill()
		print(f"{'=' * 50}\n")
		print(f"{'=' * 50}\n")
	def kill(self):
		self.health = 0
		self.game.units.remove(self)
	def __str__(self):
		basic = f"{'-' * 50}\n"
		if self.name:
			basic += (f"Unit Name: {self.name}\n")
		basic += (f"Unit level: {self.level}\nUnit Faction: {self.game.faction}\nUnit Health: {self.health}\nUnit Speed: {self.speed}\nUnit View Range: {self.view_range}\nUnit Attack Range: {self.attack_range}\nDay available: {self.day_available}\n")
		if self.combat:
			combat_info = (f"\n{'=' * 35}\nAttack Unarmored: {self.combat['unarmored']['attack']}\nDefense against Unarmored: {self.combat['unarmored']['defense']}\n{"=" * 35}\nAttack Light Armor: {self.combat['light_armor']['attack']}\nDefense Against Light Armor: {self.combat['light_armor']['defense']}\n{'=' * 35}\nAttack Heavy Armor: {self.combat['heavy_armor']['attack']}\nDefense Against Heavy Armor: {self.combat['heavy_armor']['defense']}\n{'=' * 35}\nAttack Airplane: {self.combat['airplane']['attack']}\nDefense Against Airplane: {self.combat['airplane']['defense']}\n{'=' * 35}\nAttack ship: {self.combat['ship']['attack']}\nDefense Against ships: {self.combat['ship']['defense']}\n{'=' * 35}\nAttack submarine: {self.combat['submarine']['attack']}\nDefense Against submarine: {self.combat['submarine']['defense']}\n{'=' * 35}\nAttack Buildings: {self.combat['buildings']['attack']}\nDefense Against Buildings: {self.combat['buildings']['defense']}\n{'=' * 35}\nAttack morale: {self.combat['morale']}\n{'=' * 35}\n\n\n{'=' * 35}\n")
			combat_info += (f"Research Costs:\n")
			for key, value in self.research_costs.items():
				combat_info += (f"\t{key}: {value}\n")
			combat_info += (f"\nProduction Costs:\n")
			for key, value in self.production_costs.items():
				combat_info += (f"\t{key}: {value}\n")
			combat_info += (f"\nDaily Costs:\n")
			for key, value in self.daily_costs.items():
				combat_info += (f"\t{key}: {value}\n")
			combat_info += (f"\nTerrain Effects: \n")
			for key, value in self.terrain_effects.items():
				combat_info += (f"\t{key}:\n") 
				for k, v in value.items():
					combat_info += (f"\t\t{k}: {v}\n")
			combat_info += (f"{'=' * 35}\n")
			basic += combat_info
		basic += f"{"-" * 50}\n"
		return basic

class Militia(Unit):
	@classmethod
	def create(cls, level, game, territory=None, buildings=None, health=None):
		unit = cls(level, game, territory, buildings, health, build=False)
		unit.update_stats()
		unit.pay_costs()
		if health:
			unit.health = health
		if not unit.can_afford_unit:
			return None
		return unit

	def __init__(self, level, game, territory=None, buildings=None, health=None, build=True):
		super().__init__(level, game, territory, buildings, health)
		self.name = "Militia"
		self.description = "The militia is a cheap defensive unit. Due to its slow speed and fast production time its main purpose is to defend own provinces and, due to its stealth characteristics, to ambush enemy attackers."
		self.special = "Is hidden (in hills, forests, or urban) as long as it is not fighting or uncovered by a scout unit of equal or higher level."
		self.armor_class = "unarmored"

		if build:
			self.update_stats()
			self.pay_costs()
			if health:
				self.health = health
			if not self.can_afford_unit:
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
						self.terrain_effects = {'plains': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': 1.25}, 'mountains': {'HP': 17, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.25}, 'forest': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': 1.50}, 'urban': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}
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
						self.terrain_effects = {'plains': {'HP': 23, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 23, 'armor': 'soldier', 'speed': None, 'strength': 1.25}, 'mountains': {'HP': 23, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.25}, 'forest': {'HP': 23, 'armor': 'soldier', 'speed': None, 'strength': 1.50}, 'urban': {'HP': 23, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}
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
						self.terrain_effects = {'plains': {'HP': 35, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 35, 'armor': 'soldier', 'speed': None, 'strength': 1.25}, 'mountains': {'HP': 35, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.25}, 'forest': {'HP': 35, 'armor': 'soldier', 'speed': None, 'strength': 1.50}, 'urban': {'HP': 35, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}
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
						self.terrain_effects = {'plains': {'HP': 52, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 52, 'armor': 'soldier', 'speed': None, 'strength': 1.25}, 'mountains': {'HP': 52, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.25}, 'forest': {'HP': 52, 'armor': 'soldier', 'speed': None, 'strength': 1.50}, 'urban': {'HP': 52, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}

			case "Allies":
				pass
			case "Comintern":
				pass
			case "Pan-asian":
				pass
			case _:
				pass

class Infantry(Unit):
	@classmethod
	def create(cls, level, game, territory=None, buildings=None, health=None):
		unit = cls(level, game, territory, buildings, health, build=False)
		unit.update_stats()
		unit.pay_costs()
		if unit.can_afford_unit:
			return unit
		return None
	def __init__(self, level, game, territory=None, buildings=None, health=None, build=True):
		super().__init__(level, game, territory, buildings, health)
		self.name = "Infantry"
		self.description = "Infantry is a defensive unit and the base unit of every army. It is cheap and easy to produce and important to defend cities. Infantry is best used to defend against unarmored units."
		self.special = None
		self.armor_class = "unarmored"
		if build:
			self.update_stats()
			self.pay_costs()
			if not self.can_afford_unit:
				raise ValueError("Cannot afford this Unit. Please do not try to bypass my code, use game.add_unit()!")
	def update_stats(self):
		match self.game.faction:
			case "Axis":
				match self.level:
					case 1:
						self.combat = {"unarmored": {"attack": 3.5, "defense": 5.3}, "light_armor": {"attack": 1.7, "defense": 2.6}, "heavy_armor": {"attack": 1.2, "defense": 1.8}, "airplane": {"attack": 1.2, "defense": 1.8}, "ship": {"attack": 0.6, "defense": 0.9}, "submarine": {"attack": 0.6, "defense": 0.9}, "buildings": {"attack": 0.2, "defense": 0.3}, "morale": 0.1}
						self.health = 17
						self.speed = 36
						self.view_range = 42
						self.attack_range = 0
						self.research_costs = {'steel': 400, 'corn': 1900, 'cash': 2550}
						self.production_costs = {'corn': 1200, 'manpower': 1100, 'steel': 280, 'cash': 880}
						self.daily_costs = {'corn': 55, 'manpower': 48, 'steel': 13, 'cash': 40}
						self.minimum_production_time = 2.5
						self.research_time = 0.083
						self.day_available = 1
						self.terrain_effects = {'plains': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 17, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.20}, 'forest': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': 1.20}, 'urban': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': 1.5}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}
					case 2:
						self.combat = {"unarmored": {"attack": 4.6, "defense": 6.9}, "light_armor": {"attack": 2.3, "defense": 3.4}, "heavy_armor": {"attack": 1.7, "defense": 2.6}, "airplane": {"attack": 1.7, "defense": 2.6}, "ship": {"attack": 1.2, "defense": 1.8}, "submarine": {"attack": 1.2, "defense": 1.8}, "buildings": {"attack": 0.3, "defense": 0.5}, "morale": 0.1}
						self.health = 23
						self.speed = 39
						self.view_range = 42
						self.attack_range = 0
						self.research_costs = {'steel': 450, 'corn': 2050, 'cash': 2850}
						self.production_costs = {'corn': 1300, 'manpower': 1100, 'steel': 280, 'cash': 880}
						self.daily_costs = {'corn': 58, 'manpower': 48, 'steel': 13, 'cash': 40}
						self.minimum_production_time = 3
						self.research_time = 5
						self.day_available = 2
						self.terrain_effects = {'plains': {'HP': 23, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 23, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 23, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.20}, 'forest': {'HP': 23, 'armor': 'soldier', 'speed': None, 'strength': 1.20}, 'urban': {'HP': 23, 'armor': 'soldier', 'speed': None, 'strength': 1.5}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}
					case 3:
						self.combat = {"unarmored": {"attack": 6.3, "defense": 9.4}, "light_armor": {"attack": 3.1, "defense": 4.6}, "heavy_armor": {"attack": 2.3, "defense": 3.4}, "airplane": {"attack": 2.3, "defense": 3.4}, "ship": {"attack": 1.7, "defense": 2.6}, "submarine": {"attack": 1.7, "defense": 2.6}, "buildings": {"attack": 0.5, "defense": 0.7}, "morale": 0.1}
						self.health = 29
						self.speed = 42
						self.view_range = 42
						self.attack_range = 0
						self.research_costs = {'steel': 500, 'corn': 2250, 'cash': 3150}
						self.production_costs = {'corn': 1300, 'manpower': 1100, 'steel': 280, 'cash': 940}
						self.daily_costs = {'corn': 60, 'manpower': 48, 'steel': 13, 'cash': 43}
						self.minimum_production_time = 3.5
						self.research_time = 8
						self.day_available = 3
						self.terrain_effects = {'plains': {'HP': 29, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 29, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 23, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.20}, 'forest': {'HP': 29, 'armor': 'soldier', 'speed': None, 'strength': 1.20}, 'urban': {'HP': 29, 'armor': 'soldier', 'speed': None, 'strength': 1.5}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'Enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}
					case 4:
						self.combat = {"unarmored": {"attack": 8.1, "defense": 12.2}, "light_armor": {"attack": 4.6, "defense": 6.9}, "heavy_armor": {"attack": 3.5, "defense": 5.3}, "airplane": {"attack": 3.5, "defense": 5.3}, "ship": {"attack": 3.5, "defense": 3.5}, "submarine": {"attack": 2.3, "defense": 3.5}, "buildings": {"attack": 0.7, "defense": 1.1}, "morale": 0.2}
						self.health = 35
						self.speed = 45
						self.view_range = 42
						self.attack_range = 0
						self.research_costs = {'steel': 500, 'corn': 2450, 'cash': 3450}
						self.production_costs = {'corn': 1400, 'manpower': 1100, 'steel': 280, 'cash': 990}
						self.daily_costs = {'corn': 63, 'manpower': 50, 'steel': 13, 'cash': 45}
						self.minimum_production_time = 4
						self.research_time = 10
						self.day_available = 4
						self.terrain_effects = {'plains': {'HP': 35, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 35, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 35, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.20}, 'forest': {'HP': 35, 'armor': 'soldier', 'speed': None, 'strength': 1.20}, 'urban': {'HP': 35, 'armor': 'soldier', 'speed': None, 'strength': 1.5}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}
					case 5:
						self.combat = {"unarmored": {"attack": 10.4, "defense": 15.6}, "light_armor": {"attack": 5.8, "defense": 8.7}, "heavy_armor": {"attack": 4.6, "defense": 6.9}, "airplane": {"attack": 4.6, "defense": 6.9}, "ship": {"attack": 3.5, "defense": 5.2}, "submarine": {"attack": 3.5, "defense": 5.2}, "buildings": {"attack": 0.9, "defense": 1.3}, "morale": 0.2}
						self.health = 46
						self.speed = 48
						self.view_range = 42
						self.attack_range = 0
						self.research_costs = {'steel': 700, 'corn': 3150, 'cash': 4600}
						self.production_costs = {'corn': 1500, 'manpower': 1100, 'steel': 330, 'cash': 1100}
						self.daily_costs = {'corn': 70, 'manpower': 50, 'steel': 15, 'cash': 50}
						self.minimum_production_time = 5
						self.research_time = 15
						self.day_available = 8
						self.terrain_effects = {'plains': {'HP': 46, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 46, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 46, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.20}, 'forest': {'HP': 46, 'armor': 'soldier', 'speed': None, 'strength': 1.20}, 'urban': {'HP': 46, 'armor': 'soldier', 'speed': None, 'strength': 1.5}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}
					case 6:
						self.combat = {"unarmored": {"attack": 13.8, "defense": 20.7}, "light_armor": {"attack": 8.1, "defense": 12.2}, "heavy_armor": {"attack": 6.1, "defense": 9.1}, "airplane": {"attack": 6.1, "defense": 9.1}, "ship": {"attack": 4.6, "defense": 6.9}, "submarine": {"attack": 4.6, "defense": 6.9}, "buildings": {"attack": 1.4, "defense": 2.1}, "morale": 0.3}
						self.health = 58
						self.speed = 51
						self.view_range = 42
						self.attack_range = 0
						self.research_costs = {'steel': 850, 'corn': 3900, 'cash': 5800}
						self.production_costs = {'corn': 1800, 'manpower': 1200, 'steel': 390, 'cash': 1300}
						self.daily_costs = {'corn': 80, 'manpower': 53, 'steel': 18, 'cash': 58}
						self.minimum_production_time = 5.5
						self.research_time = 22
						self.day_available = 12
						self.terrain_effects = {'plains': {'HP': 58, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 58, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 58, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.20}, 'forest': {'HP': 58, 'armor': 'soldier', 'speed': None, 'strength': 1.20}, 'urban': {'HP': 58, 'armor': 'soldier', 'speed': None, 'strength': 1.5}, 'sea': {'HP': 12, 'armor': 'shi[', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}
					case 7:
						self.combat = {"unarmored": {"attack": 17.6, "defense": 26.4}, "light_armor": {"attack": 10.7, "defense": 16.0}, "heavy_armor": {"attack": 8.1, "defense": 12.2}, "airplane": {"attack": 8.1, "defense": 12.2}, "ship": {"attack": 6.6, "defense": 9.9}, "submarine": {"attack": 6.6, "defense": 9.9}, "buildings": {"attack": 2.1, "defense": 3.1}, "morale": 0.4}
						self.health = 75
						self.speed = 54
						self.view_range = 42
						self.attack_range = 0
						self.research_costs = {'steel': 850, 'corn': 3900, 'cash': 5800}
						self.production_costs = {'corn': 1900, 'manpower': 1200, 'steel': 440, 'cash': 1400}
						self.daily_costs = {'corn': 88, 'manpower': 53, 'steel': 20, 'cash': 63}
						self.minimum_production_time = 6.25
						self.research_time = 30
						self.day_available = 16
						self.terrain_effects = {'plains': {'HP': 75, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 75, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 75, 'armor': 'soldier', 'speed': -1.5, 'strength': 1.20}, 'forest': {'HP': 75, 'armor': 'soldier', 'speed': None, 'strength': 1.20}, 'urban': {'HP': 75, 'armor': 'soldier', 'speed': None, 'strength': 1.5}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}

			case "Allies":
				pass
			case "Comintern":
				pass
			case "Pan-Asian":
				pass

class Motorized_Infantry(Unit):
	@classmethod
	def create(cls, level, game, territory=None, buildings=None, health=None):
		unit = cls(level, game, territory, buildings, health, build=False)
		unit.update_stats()
		unit.pay_costs()
		if health:
			unit.health = health
		if not unit.can_afford_unit:
			return None
		return unit

	def __init__(self, level, game, territory=None, buildings=None, health=None, build=True):
		super().__init__(level, game, territory, buildings, health)
		self.name = "Motorized Infantry"
		self.description = "Motorized Infantry has the strength of nromal infantry and adds additional speed a high view range to it, in which it also reveals stealth units. As offensive unit it is best used for conquering cities."
		self.special = "Can uncover stealth units of the same of lower stealth level."
		self.armor_class = "unarmored"
		if build:
			self.update_stats()
			self.pay_costs()
			if health:
				self.health = health
			if not self.can_afford_unit:
				raise ValueError("Cannot afford Mot. Infantry. Please do not try to bypass create() method! Instead, use game.add_unit()")
	def update_stats(self):
		match self.game.faction:
			case "Axis":
				match self.level:
					case 1:
						self.combat = {"unarmored": {"attack": 7.8, "defense": 5.2}, "light_armor": {"attack": 3.5, "defense": 2.3}, "heavy_armor": {"attack": 2.6, "defense": 1.7}, "airplane": {"attack": 2.6, "defense": 1.7}, "ship": {"attack": 1.7, "defense": 1.1}, "submarine": {"attack": 1.7, "defense": 1.1}, "buildings": {"attack": 0.5, "defense": 0.3}, "morale": 0.1}
						self.health = 23
						self.speed = 69
						self.view_range = 72
						self.attack_range = 0
						self.production_costs = {'gas': 1700, 'corn': 1100, 'cash': 1400, 'manpower': 1300}
						self.research_costs = {'corn': 1800, 'gas': 2750, 'cash': 4400}
						self.daily_costs = {'corn': 50, 'manpower': 58, 'gas': 75, 'cash': 63}
						self.minimum_production_time = 3.75
						self.research_time = 8
						self.day_available = 1
						self.terrain_effects = {'plains': {'HP': 23, 'armor': 'soldier', 'speed': 0.25, 'strength': 0.25}, 'hills': {'HP': 23, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'mountains': {'HP': 23, 'armor': 'soldier', 'speed': -0.5, 'strength': None}, 'forest': {'HP': 23, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'urban': {'HP': 23, 'armor': 'soldier', 'speed': None, 'strength': 0.25}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}
					case 2:
						self.combat = {"unarmored": {"attack": 10.8, "defense": 7.2}, "light_armor": {"attack": 4.8, "defense": 3.2}, "heavy_armor": {"attack": 3.5, "defense": 2.3}, "airplane": {"attack": 3.5, "defense": 2.3}, "ship": {"attack": 2.6, "defense": 1.7}, "submarine": {"attack": 2.6, "defense": 1.7}, "buildings": {"attack": 0.7, "defense": 0.5}, "morale": 0.1}
						self.health = 29
						self.speed = 77
						self.view_range = 72
						self.attack_range = 0
						self.production_costs = {'gas': 1700, 'corn': 1200, 'cash': 1400, 'manpower': 1700}
						self.research_costs = {'corn': 2000, 'gas': 2950, 'cash': 4850}
						self.daily_costs = {'corn': 53, 'manpower': 58, 'gas': 78, 'cash': 65}
						self.minimum_production_time = 3.75
						self.research_time = 12
						self.day_available = 2
						self.terrain_effects = {'plains': {'HP': 29, 'armor': 'soldier', 'speed': 0.25, 'strength': 0.25}, 'hills': {'HP': 29, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'mountains': {'HP': 29, 'armor': 'soldier', 'speed': -0.5, 'strength': None}, 'forest': {'HP': 29, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'urban': {'HP': 29, 'armor': 'soldier', 'speed': None, 'strength': 0.25}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}
					case 3:
						self.combat = {"unarmored": {"attack": 14.3, "defense": 9.5}, "light_armor": {"attack": 6.9, "defense": 4.6}, "heavy_armor": {"attack": 5.2, "defense": 3.5}, "airplane": {"attack": 5.2, "defense": 3.5}, "ship": {"attack": 3.5, "defense": 2.3}, "submarine": {"attack": 3.5, "defense": 2.3}, "buildings": {"attack": 1.2, "defense": 0.8}, "morale": 0.2}
						self.health = 35
						self.speed = 85
						self.view_range = 72
						self.attack_range = 0
						self.production_costs = {'gas': 1900, 'corn': 1300, 'cash': 1600, 'manpower': 1300}
						self.research_costs = {'corn': 2450, 'gas': 3700, 'cash': 6200}
						self.daily_costs = {'corn': 58, 'manpower': 58, 'gas': 88, 'cash': 73}
						self.minimum_production_time = 5.75
						self.research_time = 16
						self.day_available = 4
						self.terrain_effects = {'plains': {'HP': 35, 'armor': 'soldier', 'speed': 0.25, 'strength': 0.25}, 'hills': {'HP': 35, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'mountains': {'HP': 35, 'armor': 'soldier', 'speed': -0.5, 'strength': None}, 'forest': {'HP': 35, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'urban': {'HP': 35, 'armor': 'soldier', 'speed': None, 'strength': 0.25}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}
					case 4:
						self.combat = {"unarmored": {"attack": 18.2, "defense": 12.1}, "light_armor": {"attack": 8.6, "defense": 5.7}, "heavy_armor": {"attack": 6.9, "defense": 4.6}, "airplane": {"attack": 6.9, "defense": 4.6}, "ship": {"attack": 5.2, "defense": 3.5}, "submarine": {"attack": 5.2, "defense": 3.5}, "buildings": {"attack": 1.4, "defense": 0.9}, "morale": 0.2}
						self.health = 46
						self.speed = 93
						self.view_range = 72
						self.attack_range = 0
						self.production_costs = {'gas': 2200, 'corn': 1400, 'cash': 1800, 'manpower': 1300}
						self.research_costs = {'corn': 3100, 'gas': 4650, 'cash': 8000}
						self.daily_costs = {'corn': 65, 'manpower': 60, 'gas': 100, 'cash': 83}
						self.minimum_production_time = 6.75
						self.research_time = 22
						self.day_available = 8
						self.terrain_effects = {'plains': {'HP': 46, 'armor': 'soldier', 'speed': 0.25, 'strength': 0.25}, 'hills': {'HP': 46, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'mountains': {'HP': 46, 'armor': 'soldier', 'speed': -0.5, 'strength': None}, 'forest': {'HP': 46, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'urban': {'HP': 46, 'armor': 'soldier', 'speed': None, 'strength': 0.25}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}
					case 5:
						self.combat = {"unarmored": {"attack": 24.1, "defense": 16.1}, "light_armor": {"attack": 12.1, "defense": 8.1}, "heavy_armor": {"attack": 9.2, "defense": 6.1}, "airplane": {"attack": 9.2, "defense": 6.1}, "ship": {"attack": 6.9, "defense": 4.6}, "submarine": {"attack": 6.9, "defense": 4.6}, "buildings": {"attack": 2.1, "defense": 1.4}, "morale": 0.3}
						self.health = 58
						self.speed = 101
						self.view_range = 72
						self.attack_range = 0
						self.production_costs = {'gas': 2400, 'corn': 1700, 'cash': 2000, 'manpower': 1400}
						self.research_costs = {'corn': 3750, 'gas': 5600, 'cash': 9800}
						self.daily_costs = {'corn': 75, 'manpower': 63, 'gas': 110, 'cash': 93}
						self.minimum_production_time = 7.75
						self.research_time = 30
						self.day_available = 12
						self.terrain_effects = {'plains': {'HP': 58, 'armor': 'soldier', 'speed': 0.25, 'strength': 0.25}, 'hills': {'HP': 58, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'mountains': {'HP': 58, 'armor': 'soldier', 'speed': -0.5, 'strength': None}, 'forest': {'HP': 58, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'urban': {'HP': 58, 'armor': 'soldier', 'speed': None, 'strength': 0.25}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}
					case 6:
						self.combat = {"unarmored": {"attack": 29.9, "defense": 19.9}, "light_armor": {"attack": 16.1, "defense": 10.7}, "heavy_armor": {"attack": 12.1, "defense": 8.1}, "airplane": {"attack": 12.1, "defense": 8.1}, "ship": {"attack": 9.8, "defense": 6.5}, "submarine": {"attack": 9.8, "defense": 6.5}, "buildings": {"attack": 3.2, "defense": 2.1}, "morale": 0.4}
						self.health = 75
						self.speed = 109
						self.view_range = 72
						self.attack_range = 0
						self.production_costs = {'gas': 2700, 'corn': 1800, 'cash': 2400, 'manpower': 2000}
						self.research_costs = {'corn': 4400, 'gas': 6550, 'cash': 1160}
						self.daily_costs = {'corn': 83, 'manpower': 63, 'gas': 123, 'cash': 103}
						self.minimum_production_time = 8.5
						self.research_time = 38
						self.day_available = 16
						self.terrain_effects = {'plains': {'HP': 75, 'armor': 'soldier', 'speed': 0.25, 'strength': 0.25}, 'hills': {'HP': 75, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'mountains': {'HP': 75, 'armor': 'soldier', 'speed': -0.5, 'strength': None}, 'forest': {'HP': 75, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'urban': {'HP': 75, 'armor': 'soldier', 'speed': None, 'strength': 0.25}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}

class Mechanized_Infantry(Unit):
	@classmethod
	def create(cls, level, game, territory=None, buildings=None, health=None):
		unit = cls(level, game, territory, buildings, health, build=False)
		unit.update_stats()
		unit.pay_costs()
		if health:
			unit.health = health
		if not unit.can_afford_unit:
			return None
		return unit

	def __init__(self, level, game, territory=None, buildings=None, health=None, build=True):
		super().__init__(level, game, territory, buildings, health)
		self.name = "Mechanized Infantry"
		self.description = "Mechanized Infantry combines the strengths of infantry with the endurance of armored vehicles. As an allrounder it can be used for both offensive and defenseive maneuvers. It is most effective against unarmored targets."
		self.special = None
		self.armor_class = "light armor"
		if build:
			self.update_stats()
			self.pay_costs()
			if health:
				self.health = health
			if not self.can_afford_unit:
				raise ValueError("Cannot afford Mech. Infantry. Please do not try to bypass create() method! Instead, use game.add_unit()")
	def update_stats(self):
		match self.game.faction:
			case "Axis":
				match self.level:
					case 1:
						self.combat = {"unarmored": {"attack": 9.8, "defense": 9.8}, "light_armor": {"attack": 5.2, "defense": 5.2}, "heavy_armor": {"attack": 4.0, "defense": 4.0}, "airplane": {"attack": 4.0, "defense": 4.0}, "ship": {"attack": 2.3, "defense": 2.3}, "submarine": {"attack": 2.6, "defense": 2.6}, "buildings": {"attack": 0.7, "defense": 0.7}, "morale": 0.1}
						self.health = 40
						self.speed = 55
						self.view_range = 42
						self.attack_range = 0
						self.production_costs = {'gas': 1400, 'steel': 1600, 'cash': 1800, 'manpower': 1400}
						self.research_costs = {'steel': 2900, 'gas': 2600, 'cash': 6350}
						self.daily_costs = {'steel': 73, 'manpower': 63, 'gas': 65, 'cash': 80}
						self.minimum_production_time = 5.75
						self.research_time = 14
						self.day_available = 3
						self.terrain_effects = {'plains': {'HP': 40, 'armor': 'soldier', 'speed': 0.25, 'strength': 0.25}, 'hills': {'HP': 40, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'mountains': {'HP': 40, 'armor': 'soldier', 'speed': -0.5, 'strength': None}, 'forest': {'HP': 40, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'urban': {'HP': 40, 'armor': 'soldier', 'speed': None, 'strength': 0.25}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}
					case 2:
						self.combat = {"unarmored": {"attack": 13.2, "defense": 13.2}, "light_armor": {"attack": 7.5, "defense": 7.5}, "heavy_armor": {"attack": 5.5, "defense": 5.5}, "airplane": {"attack": 5.5, "defense": 5.5}, "ship": {"attack": 3.5, "defense": 3.5}, "submarine": {"attack": 3.5, "defense": 3.5}, "buildings": {"attack": 0.9, "defense": 0.9}, "morale": 0.2}
						self.health = 52
						self.speed = 62
						self.view_range = 42
						self.attack_range = 0
						self.production_costs = {'gas': 1700, 'steel': 1900, 'cash': 2000, 'manpower': 1400}
						self.research_costs = {'steel': 3400, 'gas': 3800, 'cash': 8500}
						self.daily_costs = {'steel': 85, 'manpower': 65, 'gas': 75, 'cash': 93}
						self.minimum_production_time = 7
						self.research_time = 19
						self.day_available = 6
						self.terrain_effects = {'plains': {'HP': 52, 'armor': 'soldier', 'speed': 0.25, 'strength': 0.25}, 'hills': {'HP': 52, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'mountains': {'HP': 52, 'armor': 'soldier', 'speed': -0.5, 'strength': None}, 'forest': {'HP': 52, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'urban': {'HP': 52, 'armor': 'soldier', 'speed': None, 'strength': 0.25}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}
					case 3:
						self.combat = {"unarmored": {"attack": 16.7, "defense": 16.7}, "light_armor": {"attack": 10.1, "defense": 10.1}, "heavy_armor": {"attack": 7.5, "defense": 7.5}, "airplane": {"attack": 7.5, "defense": 7.5}, "ship": {"attack": 5.2, "defense": 5.2}, "submarine": {"attack": 5.2, "defense": 5.2}, "buildings": {"attack": 1.4, "defense": 1.4}, "morale": 0.2}
						self.health = 63
						self.speed = 69
						self.view_range = 42
						self.attack_range = 0
						self.production_costs = {'gas': 1900, 'steel': 2100, 'cash': 2300, 'manpower': 1400}
						self.research_costs = {'steel': 3400, 'gas': 3800, 'cash': 8500}
						self.daily_costs = {'steel': 95, 'manpower': 65, 'gas': 85, 'cash': 105}
						self.minimum_production_time = 8
						self.research_time = 26
						self.day_available = 10
						self.terrain_effects = {'plains': {'HP': 63, 'armor': 'soldier', 'speed': 0.25, 'strength': 0.25}, 'hills': {'HP': 63, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'mountains': {'HP': 63, 'armor': 'soldier', 'speed': -0.5, 'strength': None}, 'forest': {'HP': 63, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'urban': {'HP': 63, 'armor': 'soldier', 'speed': None, 'strength': 0.25}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}
					case 4:
						self.combat = {"unarmored": {"attack": 21.9, "defense": 21.9}, "light_armor": {"attack": 13.2, "defense": 13.2}, "heavy_armor": {"attack": 10.1, "defense": 10.1}, "airplane": {"attack": 10.1, "defense": 10.1}, "ship": {"attack": 7.8, "defense": 7.8}, "submarine": {"attack": 6.9, "defense": 6.9}, "buildings": {"attack": 2.1, "defense": 2.1}, "morale": 0.3}
						self.health = 81
						self.speed = 76
						self.view_range = 42
						self.attack_range = 0
						self.production_costs = {'gas': 2100, 'steel': 2400, 'cash': 2600, 'manpower': 1500}
						self.research_costs = {'steel': 5550, 'gas': 5000, 'cash': 12850}
						self.daily_costs = {'steel': 108, 'manpower': 68, 'gas': 95, 'cash': 118}
						self.minimum_production_time = 9
						self.research_time = 34
						self.day_available = 14
						self.terrain_effects = {'plains': {'HP': 81, 'armor': 'soldier', 'speed': 0.25, 'strength': 0.25}, 'hills': {'HP': 81, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'mountains': {'HP': 81, 'armor': 'soldier', 'speed': -0.5, 'strength': None}, 'forest': {'HP': 81, 'armor': 'soldier', 'speed': -0.25, 'strength': None}, 'urban': {'HP': 81, 'armor': 'soldier', 'speed': None, 'strength': 0.25}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}

class Commandos(Unit):
	@classmethod
	def create(cls, level, game, territory=None, buildings=None, health=None):
		unit = cls(level, game, territory, buildings, health, build=False)
		unit.update_stats()
		unit.pay_costs()
		if health:
			unit.health = health
		if not unit.can_afford_unit:
			return None
		return unit

	def __init__(self, level, game, territory=None, buildings=None, health=None, build=True):
		super().__init__(level, game, territory, buildings, health)
		self.name = "Commandos"
		self.description = "Commandos are offensive units that use sabotage and explosives, making them most effective against unarmored and light armored targets. They also ignore enemy defense bonuses and are best used for surprise attacks on lightly defended positions due to their stealth characteristics."
		self.special = "Is hidden as long as it is not fighting or uncovered by a scout unit of equal or higher level. Also storms fortifications and ignores the enemy defence bonus."
		self.armor_class = "unarmored"
		if build:
			self.update_stats()
			self.pay_costs()
			if health:
				self.health = health
			if not self.can_afford_unit:
				raise ValueError("Cannot afford Commando. Please do not try to bypass create() method! Instead, use game.add_unit()")
	def update_stats(self):
		match self.game.faction:
			case "Axis":
				match self.level:
					case 1:
						self.combat = {"unarmored": {"attack": 9.2, "defense": 4.6}, "light_armor": {"attack": 10.4, "defense": 5.2}, "heavy_armor": {"attack": 6.9, "defense": 3.5}, "airplane": {"attack": 2.3, "defense": 1.2}, "ship": {"attack": 2.3, "defense": 1.2}, "submarine": {"attack": 1.2, "defense": 0.6}, "buildings": {"attack": 4.6, "defense": 2.3}, "morale": 0.5}
						self.health = 35
						self.speed = 40
						self.view_range = 30
						self.attack_range = 0
						self.production_costs = {'gas': 1100, 'corn': 2400, 'cash': 2400, 'manpower': 1200}
						self.research_costs = {'gas': 2100, 'corn': 4600, 'cash': 9250}
						self.daily_costs = {'gas': 50, 'manpower': 53, 'corn': 108, 'cash': 108}
						self.minimum_production_time = 6.5
						self.research_time = 20
						self.day_available = 8
						self.terrain_effects = {'plains': {'HP': 40, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 40, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 40, 'armor': 'soldier', 'speed': -0.5, 'strength': 0.5}, 'forest': {'HP': 40, 'armor': 'soldier', 'speed': None, 'strength': 0.5}, 'urban': {'HP': 40, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}
					case 2:
						self.combat = {"unarmored": {"attack": 12.7, "defense": 6.3}, "light_armor": {"attack": 13.8, "defense": 6.9}, "heavy_armor": {"attack": 9.2, "defense": 4.6}, "airplane": {"attack": 2.9, "defense": 1.5}, "ship": {"attack": 2.9, "defense": 1.5}, "submarine": {"attack": 1.7, "defense": 0.9}, "buildings": {"attack": 6.9, "defense": 3.5}, "morale": 0.7}
						self.health = 46
						self.speed = 46
						self.view_range = 30
						self.attack_range = 0
						self.production_costs = {'gas': 1300, 'corn': 2700, 'cash': 2700, 'manpower': 1200}
						self.research_costs = {'gas': 2100, 'corn': 4600, 'cash': 9250}
						self.daily_costs = {'gas': 58, 'manpower': 55, 'corn': 123, 'cash': 123}
						self.minimum_production_time = 7.5
						self.research_time = 26
						self.day_available = 12
						self.terrain_effects = {'plains': {'HP': 46, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 46, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 46, 'armor': 'soldier', 'speed': -0.5, 'strength': 0.5}, 'forest': {'HP': 46, 'armor': 'soldier', 'speed': None, 'strength': 0.5}, 'urban': {'HP': 46, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}
					case 3:
						self.combat = {"unarmored": {"attack": 16.7, "defense": 8.4}, "light_armor": {"attack": 19.0, "defense": 9.5}, "heavy_armor": {"attack": 12.7, "defense": 6.3}, "airplane": {"attack": 4.0, "defense": 4.0}, "ship": {"attack": 4.0, "defense": 2.0}, "submarine": {"attack": 2.9, "defense": 1.5}, "buildings": {"attack": 9.8, "defense": 4.9}, "morale": 1.0}
						self.health = 58
						self.speed = 53
						self.view_range = 30
						self.attack_range = 0
						self.production_costs = {'gas': 1400, 'corn': 3000, 'cash': 3000, 'manpower': 1200}
						self.research_costs = {'gas': 2100, 'corn': 4600, 'cash': 9250}
						self.daily_costs = {'gas': 65, 'manpower': 55, 'corn': 138, 'cash': 138}
						self.minimum_production_time = 8.5
						self.research_time = 34
						self.day_available = 16
						self.terrain_effects = {'plains': {'HP': 58, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 58, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 58, 'armor': 'soldier', 'speed': -0.5, 'strength': 0.5}, 'forest': {'HP': 58, 'armor': 'soldier', 'speed': None, 'strength': 0.5}, 'urban': {'HP': 58, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}
					case 4:
						self.combat = {"unarmored": {"attack": 16.7, "defense": 8.4}, "light_armor": {"attack": 23.0, "defense": 11.5}, "heavy_armor": {"attack": 26.5, "defense": 13.3}, "airplane": {"attack": 5.8, "defense": 2.9}, "ship": {"attack": 5.8, "defense": 2.9}, "submarine": {"attack": 4.0, "defense": 2.0}, "buildings": {"attack": 13.8, "defense": 6.9}, "morale": 1.4}
						self.health = 75
						self.speed = 60
						self.view_range = 30
						self.attack_range = 0
						self.production_costs = {'gas': 1700, 'corn': 3500, 'cash': 3500, 'manpower': 1300}
						self.research_costs = {'gas': 2100, 'corn': 4600, 'cash': 9250}
						self.daily_costs = {'gas': 75, 'manpower': 58, 'corn': 160, 'cash': 160}
						self.minimum_production_time = 9.75
						self.research_time = 46
						self.day_available = 22
						self.terrain_effects = {'plains': {'HP': 75, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 75, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 75, 'armor': 'soldier', 'speed': -0.5, 'strength': 0.5}, 'forest': {'HP': 75, 'armor': 'soldier', 'speed': None, 'strength': 0.5}, 'urban': {'HP': 75, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}

class Paratrooper(Unit):
	@classmethod
	def create(cls, level, game, territory=None, buildings=None, health=None):
		unit = cls(level, game, territory, buildings, health, build=False)
		unit.update_stats()
		unit.pay_costs()
		if health:
			unit.health = health
		if not unit.can_afford_unit:
			return None
		return unit

	def __init__(self, level, game, territory=None, buildings=None, health=None, build=True):
		super().__init__(level, game, territory, buildings, health)
		self.name = "Paratrooper"
		self.description = "Paratroopers are versatile units used for surprise attacks behind enemy lines. They are fighting best against unarmored units. While on the ground they can also be converted back into an aircraft and dropped in another location."
		self.special = "This unit can be transported via air carg to the next airfield. Also, is hidden as long as it is not fighting or uncovered by a scout unit of equal or higher level."
		self.armor_class = "unarmored"
		if build:
			self.update_stats()
			self.pay_costs()
			if health:
				self.health = health
			if not self.can_afford_unit:
				raise ValueError("Cannot afford Paratrooper. Please do not try to bypass create() method! Instead, use game.add_unit()")
	def update_stats(self):
		match self.game.faction:
			case "Axis":
				match self.level:
					case 1:
						self.combat = {"unarmored": {"attack": 10.4, "defense": 10.4}, "light_armor": {"attack": 5.2, "defense": 5.2}, "heavy_armor": {"attack": 3.5, "defense": 3.5}, "airplane": {"attack": 1.2, "defense": 1.2}, "ship": {"attack": 1.2, "defense": 1.2}, "submarine": {"attack": 1.2, "defense": 1.2}, "buildings": {"attack": 0.9, "defense": 0.9}, "morale": 0.2}
						self.health = 40
						self.speed = 42
						self.view_range = 42
						self.attack_range = 0
						self.production_costs = {'gas': 1300, 'corn': 1500, 'cash': 2800, 'manpower': 1500}
						self.research_costs = {'gas': 2100, 'corn': 4600, 'cash': 9250}
						self.daily_costs = {'gas': 60, 'manpower': 68, 'corn': 68, 'cash': 128}
						self.minimum_production_time = 6.5
						self.research_time = 20
						self.day_available = 6
						self.terrain_effects = {'plains': {'HP': 40, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 40, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 40, 'armor': 'soldier', 'speed': -0.5, 'strength': 0.5}, 'forest': {'HP': 40, 'armor': 'soldier', 'speed': None, 'strength': 0.5}, 'urban': {'HP': 40, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}
					case 2:
						self.combat = {"unarmored": {"attack": 12.7, "defense": 12.7}, "light_armor": {"attack": 6.3, "defense": 6.3}, "heavy_armor": {"attack": 4.6, "defense": 4.6}, "airplane": {"attack": 1.7, "defense": 1.7}, "ship": {"attack": 1.7, "defense": 1.7}, "submarine": {"attack": 1.7, "defense": 1.7}, "buildings": {"attack": 1.4, "defense": 1.4}, "morale": 0.2}
						self.health = 52
						self.speed = 46
						self.view_range = 42
						self.attack_range = 0
						self.production_costs = {'gas': 1500, 'corn': 1700, 'cash': 3200, 'manpower': 1500}
						self.research_costs = {'gas': 2100, 'corn': 4600, 'cash': 9250}
						self.daily_costs = {'gas': 68, 'manpower': 70, 'corn': 78, 'cash': 145}
						self.minimum_production_time = 7.5
						self.research_time = 26
						self.day_available = 10
						self.terrain_effects = {'plains': {'HP': 52, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 52, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 52, 'armor': 'soldier', 'speed': -0.5, 'strength': 0.5}, 'forest': {'HP': 52, 'armor': 'soldier', 'speed': None, 'strength': 0.5}, 'urban': {'HP': 52, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}
					case 3:
						self.combat = {"unarmored": {"attack": 16.7, "defense": 16.7}, "light_armor": {"attack": 8.6, "defense": 8.6}, "heavy_armor": {"attack": 6.3, "defense": 6.3}, "airplane": {"attack": 2.9, "defense": 2.9}, "ship": {"attack": 2.9, "defense": 2.9}, "submarine": {"attack": 2.9, "defense": 2.9}, "buildings": {"attack": 2.1, "defense": 2.1}, "morale": 0.3}
						self.health = 63
						self.speed = 50
						self.view_range = 42
						self.attack_range = 0
						self.production_costs = {'gas': 1700, 'corn': 1900, 'cash': 3600, 'manpower': 1600}
						self.research_costs = {'gas': 2100, 'corn': 4600, 'cash': 9250}
						self.daily_costs = {'gas': 75, 'manpower': 73, 'corn': 88, 'cash': 163}
						self.minimum_production_time = 8.5
						self.research_time = 34
						self.day_available = 14
						self.terrain_effects = {'plains': {'HP': 63, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 63, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 63, 'armor': 'soldier', 'speed': -0.5, 'strength': 0.5}, 'forest': {'HP': 63, 'armor': 'soldier', 'speed': None, 'strength': 0.5}, 'urban': {'HP': 63, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}
					case 4:
						self.combat = {"unarmored": {"attack": 23, "defense": 23}, "light_armor": {"attack": 11.5, "defense": 11.5}, "heavy_armor": {"attack": 8.1, "defense": 8.1}, "airplane": {"attack": 4.6, "defense": 4.6}, "ship": {"attack": 4.6, "defense": 4.6}, "submarine": {"attack": 4.6, "defense": 4.6}, "buildings": {"attack": 3.2, "defense": 3.2}, "morale": 0.4}
						self.health = 81
						self.speed = 54
						self.view_range = 42
						self.attack_range = 0
						self.production_costs = {'gas': 1900, 'corn': 2200, 'cash': 4200, 'manpower': 1700}
						self.research_costs = {'gas': 2100, 'corn': 4600, 'cash': 9250}
						self.daily_costs = {'gas': 88, 'manpower': 75, 'corn': 100, 'cash': 190}
						self.minimum_production_time = 9.75
						self.research_time = 34
						self.day_available = 20
						self.terrain_effects = {'plains': {'HP': 81, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 81, 'armor': 'soldier', 'speed': None, 'strength': None}, 'mountains': {'HP': 81, 'armor': 'soldier', 'speed': -0.5, 'strength': 0.5}, 'forest': {'HP': 81, 'armor': 'soldier', 'speed': None, 'strength': 0.5}, 'urban': {'HP': 81, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'ship', 'speed': None, 'strength': None}, 'enemy_territory': {'HP': None, 'armor': None, 'speed': -0.50, 'strength': None}}


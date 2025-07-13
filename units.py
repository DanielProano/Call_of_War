

class Unit:
	def __init__(self, name, level, game):
		self.name = name
		self.level = level
		self.game = game		### Python game object for access to important information like faction ### 
		self.health = 0
		self.combat = 0			### Python dictionary ###
		self.speed = 0
		self.view_range = 0
		self.attack_range = 0
		self.day_available = 0
		self.description = None		### Text description ###
		self.special = None		### Description of special abilities ###
		self.production_costs = None	### Python dictionary ###
		self.production_time = None	### Time in minutes ###
		self.daily_costs = None		### Pytho dictionary ###
		self.terrain_effects = None	### Python dictionary ###
	def pay_costs(self):
		if self.daily_costs and self.production_costs:
			self.game.resources.add(upkeep=self.daily_costs)
			self.game.resources.subtract(resources=self.production_costs)
		else:
			print("Either daily costs or production costs does not exist")
	def upgrade(self, level=None):
		if level:
			self.level = level
		else:
			self.level += 1
		self.update_stats()
	def attack(self, enemy_unit, territory, bunker_level):
		hp = self.terrain_effects[territory]['HP']
		if self.terrain_effects[territory]['strength']:
			hp = hp * self.terrain_effects[territory]['strength']
		if bunker_level:
			bunker_stats = {1: 15, 2: 30, 3: 45, 4: 60, 5: 75}
			
		while hp and enemy_unit.health:
			
	def __str__(self):
		basic = (f"{"-" * 50}\nUnit name: {self.name}\nUnit level: {self.level}\nUnit Faction: {self.game.faction}\nUnit Health: {self.health}\nUnit Speed: {self.speed}\nUnit View Range: {self.view_range}\nUnit Attack Range: {self.attack_range}\nDay available: {self.day_available}\n")
		if self.combat:
			combat_info = (f"{'=' * 35}\nAttack Unarmored: {self.combat['unarmored']['attack']}\nDefense against Unarmored: {self.combat['unarmored']['defense']}\n{"=" * 35}\nAttack Light Armor: {self.combat['light_armor']['attack']}\nDefense Against Light Armor: {self.combat['light_armor']['defense']}\n{"=" * 35}\nAttack Heavy Armor: {self.combat['heavy_armor']['attack']}\nDefense Against Heavy Armor: {self.combat['heavy_armor']['defense']}\n{"=" * 35}\nAttack Airplane: {self.combat['airplane']['attack']}\nDefense Against Airplane: {self.combat['airplane']['defense']}\n{"=" * 35}\nAttack ship: {self.combat['ship']['attack']}\nDefense Against ships: {self.combat['ship']['defense']}\n{"=" * 35}\nAttack submarine: {self.combat['submarine']['attack']}\nDefense Against submarine: {self.combat['submarine']['defense']}\n{"=" * 35}\nAttack Buildings: {self.combat['buildings']['attack']}\nDefense Against Buildings: {self.combat['buildings']['defense']}\n{"=" * 35}\nAttack morale: {self.combat['morale']}\n")
			basic += combat_info
		basic += f"{"-" * 50}"
		return basic

class Militia(Unit):
	def __init__(self, name, level, game):
		super().__init__(name, level, game)
		self.update_stats()
		self.pay_costs()
		self.description = "The militia is a cheap defensive unit. Due to its slow speed and fast production time its main purpose is to defend own provinces and, due to its stealth characteristics, to ambush enemy attackers."
		self.special = "Is hidden (in hills, forests, or urban) as long as it is not fighting or uncovered by a scout unit of equal or higher level."
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
						self.production_costs = {'corn': 550, 'manpower': 880, 'steel': 220, 'cash': 660}
						self.daily_costs = {'corn': 25, 'manpower': 40, 'steel': 10, 'cash': 30}
						self.production_time = 45
						self.day_available = 1
						self.terrain_effects = {'plains': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': None}, 'hills': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': 1.25}, 'mountains': {'HP': 17, 'armor': 'soldier', 'speed': -1.50, 'strength': 1.25}, 'forest': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': 1.50}, 'urban': {'HP': 17, 'armor': 'soldier', 'speed': None, 'strength': None}, 'sea': {'HP': 12, 'armor': 'soldier', 'speed': None, 'strength': None}, 'Enemy_territory': {'HP': None, 'armor': None, 'speed': -1.50, 'strength': None}}
					case 2:
						self.combat = {"unarmored": {"attack": 3.7, "defense": 5.5}, "light_armor": {"attack": 2.0, "defense": 3.0}, "heavy_armor": {"attack": 1.2, "defense": 1.8}, "airplane": {"attack": 1.9, "defense": 2.8}, "ship": {"attack": 1.5, "defense": 2.2}, "submarine": {"attack": 1.5, "defense": 2.2}, "buildings": {"attack": 0.7, "defense": 1.0}, "morale": 0.1}
			case "Allies":
				pass
			case "Comintern":
				pass
			case "Pan-asian":
				pass
			case _:
				pass


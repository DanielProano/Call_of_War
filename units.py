

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
		self.description = None		### Text description ###
		self.special = None
		self.production_costs = None	### Python dictionary ###
		self.production_time = None	### Time in minutes ###
		self.daily_costs = None		### Pytho dictionary ###
	def upkeep(self, unit_upkeep):
		self.game.resources.update(upkeep=unit_upkeep)
	def upgrade(self, level=None):
		if level:
			self.level = level
		else:
			self.level += 1
		self.update_stats()
	def attack(self, enemy_unit):
		pass
	def __str__(self):
		basic = (f"{"-" * 50}\nUnit name: {self.name}\nUnit level: {self.level}\nUnit Faction: {self.game.faction}\nUnit Health: {self.health}\nUnit Speed: {self.speed}\nUnit View Range: {self.view_range}\nUnit Attack Range: {self.attack_range}\n")
		if self.combat:
			combat_info = (f"{'=' * 35}\nAttack Unarmored: {self.combat['unarmored']['attack']}\nDefense against Unarmored: {self.combat['unarmored']['defense']}\n{"=" * 35}\nAttack Light Armor: {self.combat['light_armor']['attack']}\nDefense Against Light Armor: {self.combat['light_armor']['defense']}\n{"=" * 35}\nAttack Heavy Armor: {self.combat['heavy_armor']['attack']}\nDefense Against Heavy Armor: {self.combat['heavy_armor']['defense']}\n{"=" * 35}\nAttack Airplane: {self.combat['airplane']['attack']}\nDefense Against Airplane: {self.combat['airplane']['defense']}\n{"=" * 35}\nAttack ship: {self.combat['ship']['attack']}\nDefense Against ships: {self.combat['ship']['defense']}\n{"=" * 35}\nAttack submarine: {self.combat['submarine']['attack']}\nDefense Against submarine: {self.combat['submarine']['defense']}\n{"=" * 35}\nAttack Buildings: {self.combat['buildings']['attack']}\nDefense Against Buildings: {self.combat['buildings']['defense']}\n{"=" * 35}\nAttack morale: {self.combat['morale']}\n")
			basic += combat_info
		basic += f"{"-" * 50}"
		return basic

class Militia(Unit):
	def __init__(self, name, level, game):
		super().__init__(name, level, game)
		self.update_stats()
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
						self.productions_costs = {'corn': 550, 'manpower': 880, 'steel': 220, 'cash': 660}
						self.production_time = 45
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


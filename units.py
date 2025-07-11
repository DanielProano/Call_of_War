

class Unit:
	def __init__(self, name, level, game):
		self.name = name
		self.level = level
		self.game = game
		self.health = None
		self.combat = None
	def upkeep(self, unit_upkeep):
		self.game.resources.update(upkeep=unit_upkeep)
	def upgrade(self, level=None):
		if level:
			self.level = level
		else:
			self.level += 1
	def attack(self, enemy_unit):
		pass
	def __str__(self):
		return f"{"-" * 40}\nUnit name: {self.name}\nUnit level: {self.level}\nUnit Faction: {self.game.faction}\nVersus Unarmored: {self.combat['unarmored']}\nVersus Light Armor: {self.combat['light_armor']}\nVersus Heavy Armor: {self.combat['heavy_armor']}\nVersus Airplane: {self.combat['airplane']}\nVersus ship: {self.combat['ship']}\nVersus submarine: {self.combat['submarine']}\nVersus Buildings: {self.combat['buildings']}\nVersus morale: {self.combat['morale']}\n{"-" * 40}"

class Militia(Unit):
	def __init__(self, name, level, game):
		super().__init__(name, level, game)
		match self.game.faction:
			case "Axis":
				match self.level:
					case 1:
						self.combat = {"unarmored": {"attack": 2.0, "defense": 3.0}, "light_armor": {"attack": 1.2, "defense": 1.8}, "heavy_armor": {"attack": 0.6, "defense": 0.9}, "airplane": {"attack": 1.2, "defense": 1.8}, "ship": {"attack": 0.6, "defense": 0.9}, "submarine": {"attack": 0.6, "defense": 0.9}, "buildings": {"attack": 0.5, "defense": 0.8}, "morale": 0.1}
						#self.health = 
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


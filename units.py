

class Unit:
	def __init__(self, name, level, game):
		self.name = name
		self.level = level
	def upkeep(self, resources):
		self.resources.update(self.upkeep)
	def upgrade(self, level=None):
		if level:
			self.level = level
		else:
			self.level += 1

class Militia(Unit):
	def __init__(self, name, level):
		super().__init__(name, level)
		match self.faction:
			case "Axis":
				match self.level:
					case 1:
						self.combat = {"unarmored": {"attack": 2.0, "defense": 3.0}, "light_armor": {"attack": 1.2, "defense": 1.8}, "heavy_armor": {"attack": 0.6, "defense": 0.9}, "airplane": {"attack": 1.2, "defense": 1.8}, "ship": {"attack": 0.6, "defense": 0.9}, "submarine": {"attack": 0.6, "defense": 0.9}, "buildings": {"attack": 0.5, "defense": 0.8}, "morale": 0.1}
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


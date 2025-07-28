import units

class Stack:
	def create(self, game, territory=None, buildings=None):
		pass
	def __init__(self, game, territory=None, buildings=None):
		self.units = []	
		self.game = game
		self.territory = territory
		self.buildings = buildings

	def add_to_stack(self, unit):
		if isinstance(unit, units.Unit):
			unit.territory = self.territory
			unit.buildings = self.buildings
			self.units.append(unit)
		else:
			print("Cannot add because paramater is not a Unit")

	def create_units(self, unit_cls, level=1, num=1, health=None):
		for i in range(num):
			unit = self.game.add_unit(unit_cls, level, health=health)
			if unit:
				self.add_to_stack(unit)
			else:
				print("Couldn't make unit")

	def combine_with(self, stack2):
		if isinstance(stack2, Stack):
			for i in stack2.units:
				i.territory = self.territory
				i.buildings = self.buildings
				self.units.append(i)
			stack2.units.clear()
			if hasattr(self.game, "stacks"):
				self.game.stacks.remove(stack2)
		else:
			print("Cannot combine because input is not a stack")


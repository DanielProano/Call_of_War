import units

class Stack:
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

	def create_units(self, unit_cls, level=1, num=1, health=None, owner=True):
		for i in range(num):
			unit = self.game.add_unit(unit_cls, level, health=health, owner=owner)
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

	def __str__(self):
		info = f"Stack info\n{'-' * 50}\n"
		units_list = {}
		for unit in self.units:
			name = unit.name
			hp = unit.health
			
			if name not in units_list:
				units_list[name] = {}
			if hp not in units_list[name]:
				units_list[name][hp] = 0

			units_list[name][hp] += 1
		
		total = 0
		for unit_name, unit_health in units_list.items():
			for unit_hp, unit_count in unit_health.items():
				total += unit_count * unit_hp
				if unit_count > 1:
					info += f"{unit_count} {unit_name} with {unit_hp * unit_count} total health, {unit_hp} each\n"
				else:
					info += f"{unit_count} {unit_name} with {unit_hp} health individually\n"
		info += f"Total hp: {total}\n{'-' * 50}\n"
		return info

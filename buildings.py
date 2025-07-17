class Buildings:
	@classmethod
	def create(cls, level, game, *args, affect_resources=True):
		building = cls(level, game, *args)
		if affect_resources:
			if building.pay_costs():
				return building
			else:
				print("Could not afford building")
				return None
		else:
			return building
	def __init__(self, level, game):
		self.level = level
		self.game = game	### Python game object ###
	def pay_costs(self):
		if hasattr(self, "construction_costs"):
			successfully_paid = self.game.resources.subtract(resources=self.construction_costs)
			if successfully_paid:
				if isinstance(self, Industry):
					if self.level == 1:
						self.game.resources.production[self.resource] += round(self.daily_resource_production * 1.13)
						self.game.resources.production['cash'] += round(self.daily_resource_production * 1.13)
						return True
					else:
						options = {1: 0.13, 2: 0.28, 3: 0.5, 4: 0.8, 5: 1.2}
						production_resource = self.daily_resource_production / (1 + options[self.level - 1])
						self.game.resources.production[self.resource] += round((production_resource * self.effects) + production_resource)
						self.game.resources.production['cash'] += round((production_resource * self.effects) + production_resource)
						return True
				if isinstance(self, Recruiting_Station):
					if self.level == 1:
						self.game.resources.production[self.resource] += round(self.daily_resource_production * 1.35)
						return True
					else:
						options = {1: 0.35, 2: 1, 3: 2}
						manpower_resource = self.daily_resource_production / (1 + options[self.level - 1])
						print(manpower_resource)
						self.game.resources.production['manpower'] += round((manpower_resource * self.effects) + manpower_resource)
						return True
				return True
			else:
				return False
		else:
			return False
	def update(self, level=None, game=None, resource=None, daily_resource_production=None, affect_resources=True):
		if level:
			self.level = level
			if affect_resources:
				self.pay_costs()
		if game:
			self.game = game
		if daily_resource_production:
			self.daily_resource_production = daily_resource_production
		if resource:
			self.game.resources.production[self.resource] =
			self.resource = resource
			
	def __str__(self):
		info = f"Building Information\n{'-' * 50}\nLevel: {self.level}\nFaction: {self.game.faction}\n"
		if hasattr(self, "description"):
			info += f"Description: {self.description}\n"
		if hasattr(self, "health"):
			info += f"Health: {self.health}\n"
		if hasattr(self, "effects"):
			info += f"Effects: {self.effects * 100}%\n"
		if hasattr(self, "construction_costs"):
			info += f"Construction Costs: {self.construction_costs}\n"
		if hasattr(self, "construction_time"):
			info += f"Construction Time: {self.construction_time} hours\n"
		if hasattr(self, "refueling_time"):
			info += f"Refueling Time: {self.refueling_time} minutes\n"
		info += f"{'-' * 50}\n"
		return info
		

class Barracks(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "Barracks are required to recruit Infantry units. Each level of the Barracks halves the unit production time until the minimum production time of a unit is reached. Barracks can only be constructed in ubran provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 1	### Unit production effect ###
				self.construction_costs = {'steel': 1350, 'corn': 2250, 'cash': 3600}
				self.construction_time = 0.083	### 5 minutes ###
			case 2:
				self.health = 40
				self.effects = 2
				self.construction_costs = {'steel': 1800, 'corn': 3000, 'cash': 4800}
				self.construction_time = 4
			case 3:
				self.health = 80
				self.effects = 4
				self.construction_costs = {'steel': 2400, 'corn': 4000, 'cash': 6400}
				self.construction_time = 12
			case 4:
				self.health = 120
				self.effects = 8
				self.construction_costs = {'steel': 2720, 'corn': 4505, 'cash': 7225}
				self.construction_time = 24
			case 5:
				self.health = 160
				self.effects = 16
				self.construction_costs = {'steel': 4250, 'corn': 7050, 'cash': 11300}
				self.construction_time = 32
			case _:
				raise ValueError("This level does not exist")

class Ordance_Foundry(Buildings):	
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Ordance Foundry is required to produce support units that usualy feature larger gun calibers. Each level of the Ordance Foundry halves the unit production time until the minimum prodction time of a unit is reached. The Ordance Foundry can only be constructed un urban provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 1
				self.construction_costs = {'gas': 2400, 'corn': 1200, 'cash': 3600}
				self.construction_time = 0.083
			case 2:
				self.health = 40
				self.effects = 2
				self.construction_costs = {'gas': 3200, 'corn': 1600, 'cash': 4800}
				self.cosntruction_time = 4
			case 3:	
				self.health = 80
				self.effects = 4
				self.construction_costs = {'gas': 4250, 'corn': 2150, 'cash': 6400}
				self.construction_time = 12
			case 4:
				self.health = 120
				self.effects = 8
				self.construction_costs = {'gas': 5650, 'corn': 2850, 'cash': 8500}
				self.construction_time = 24
			case 5:
				self.health = 160
				self.effects = 16
				self.construction_costs = {'gas': 7500, 'corn': 3800, 'cash': 11300}
				self.construction_time = 32
			case _:
				raise ValueError("This level does not exist")
class Tank_Plant(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Tank Plant is required to produce tank units. Each level of the Tank Plant halves the unit production time until the minimum production time of a unit is reached. The Tank Plant can only be constructed in urban provices."
		match self.level:	
			case 1:
				self.health = 20
				self.effects = 1
				self.construction_costs = {'steel': 2100, 'gas': 1500, 'cash': 3600}
				self.construction_time = 0.083
			case 2:
				self.health = 40
				self.effects = 2
				self.construction_costs = {'steel': 2800, 'gas': 2000, 'cash': 4800}
				self.construction_time = 4
			case 3:
				self.health = 80
				self.effects = 4
				self.construction_costs = {'steel': 3700, 'gas': 2650, 'cash': 6400}
				self.construction_time = 12
			case 4:
				self.health = 120
				self.effects = 8
				self.construction_costs = {'steel': 4900, 'gas': 3500, 'cash': 8500}
				self.construction_time = 24
			case 5:
				self.health = 160
				self.effects = 16
				self.construction_costs = {'steel': 6500, 'gas': 4650, 'cash': 11300}
				self.construction_time = 32
			case _:
				raise ValueError("This level does not exist")

class Aircraft_Factory(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Aircraft Factory is required to produce air units and allows aircrafts to take off or land in this province. Each level of the Aircraft Factory halves the unit production time until the minimum production time of a unit is reached. Each building level also reduces the refueling times of airplanes in this province. The Aircraft Factory can only be constructed in urban provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 1
				self.refueling_time = 30	### in minutes ###
				self.construction_costs = {'gas': 2350, 'corn': 1250, 'cash': 3600}
				self.construction_time = 0.5
			case 2:
				self.health = 40
				self.effects = 2
				self.refueling_time = 25
				self.construction_costs = {'gas': 3150, 'corn': 1650, 'cash': 4800}
				self.construction_time = 4
			case 3:
				self.health = 80
				self.effects = 4
				self.refueling_time = 20
				self.construction_costs = {'gas': 4200, 'corn': 2200, 'cash': 6400}
				self.construction_time = 12
			case 4:
				self.health = 120
				self.effects = 8
				self.refueling_time = 15
				self.construction_costs = {'gas': 5600, 'corn': 2950, 'cash': 8500}
				self.construction_time = 24
			case 5:
				self.health = 160
				self.effects = 16
				self.refueling_time = 10
				self.construction_costs = {'gas': 7450, 'corn': 3900, 'cash': 11300}
				self.construction_time = 32
			case _:
				raise ValueError("This level does not exist")


class Secret_Lab(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Secret Lab is required to produce secret weapons. Each level of the Secret Lab halves the unit production time until the minimum production time of a unit is reached. The current level of the Secret Lab is hidden to others. The Secret Lab can only constructed in urban provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 1
				self.construction_costs = {'steel': 1400, 'gas': 2200, 'cash': 3600}
				self.construction_time = 0.5
			case 2:
				self.health = 40
				self.effects = 2
				self.construction_costs = {'steel': 1850, 'gas': 2950, 'cash': 4800}
				self.construction_time = 4
			case 3:
				self.health = 80
				self.effects = 4
				self.construction_costs = {'steel': 2450, 'gas': 3900, 'cash': 6400}
				self.construction_time = 12
			case 4:
				self.health = 120
				self.effects = 8
				self.construction_costs = {'steel': 3250, 'gas': 5200, 'cash': 8500}
				self.construction_time = 24
			case 5:
				self.health = 160
				self.effects = 16
				self.construction_costs = {'gas': 6900, 'steel': 4300, 'cash': 11300}
				self.construction_time = 32
			case _:
				raise ValueError("This level does not exist")


### Industry is a special building where the resource being produced also needs to be specified in text. Your options are "corn", "steel", "gas". ###

class Industry(Buildings):
	def __init__(self, level, game, resource, daily_resource_production):
		super().__init__(level, game)
		self.description = "The Industry increases the production rates of resorces and money in this province. Leveling up the Industry increases these production rates further. Industry can only be constructed in urban provinces."
		self.daily_resource_production = daily_resource_production
		options = ["corn", "steel", "gas"]
		is_a_resource = False
		for i in options:
			if i == resource:
				is_a_resource = True
		if is_a_resource:
			self.resource = resource
		else:
			raise ValueError("Not an available resource, please choose one of these: corn, steel, gas")

		match self.level:
			case 1:
				self.health = 20
				self.effects = 0.13	### Production boost in percentage ###
				self.construction_costs = {'steel': 1400, 'gas': 1600, 'cash': 3000}
				self.construction_time = 8	### in hours for next industry, so for industry 2 ###
			case 2:
				self.health = 40
				self.effects = 0.28
				self.construction_costs = {'steel': 1850, 'gas': 2150, 'cash': 4000}
				self.construction_time = 14
			case 3:
				self.health = 50
				self.effects = 0.50
				self.construction_costs = {'steel': 2450, 'gas': 2850, 'cash': 5300}
				self.construction_time = 20
			case 4:
				self.health = 120	
				self.effects = 0.80
				self.construction_costs = {'steel': 3250, 'gas': 3800, 'cash': 7050}
				self.construction_time = 26
			case 5:
				self.health = 160
				self.effects = 1.20
				self.construction_costs = {'steel': 4300, 'gas': 5050, 'cash': 9400}
				self.construction_time = 32
			case _:
				raise ValueError("This level does not exist")

class Recruiting_Station(Buildings):
	def __init__(self, level, game, daily_resource_production):
		super().__init__(level, game)
		self.description = "The Recruiting Station increases the manpower production rate in this province. Leveling up the Recruiting Station increases the manpower production rate further. The Recruiting Station can be constructed in all provinces."
		self.resource = "cash"
		self.daily_resource_production = daily_resource_production
		match self.level:
			case 1:
				self.health = 20
				self.effects = 0.35 	### manpower production boost in percentage ###
				self.construction_costs = {'steel': 1100, 'corn': 1600, 'cash': 2700}
				self.construction_time = 6 	### in hours ###
			case 2:
				self.health = 60
				self.effects = 1
				self.construction_costs = {'steel': 1450, 'corn': 2150, 'cash': 3600}
				self.construction_time = 12
			case 3:
				self.health = 120
				self.effects = 2
				self.construction_costs = {'steel': 1950, 'corn': 2850, 'cash': 4800}
				self.construction_time = 18
			case _:
				raise ValueError("This level does not exist")


class Propaganda_Office(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Propaganda Office helps to improve the morale of a province over time by raising its target morale. Province morale increases or decreases at daychange towards the target morale, by an amount that is dependent on the difference between the current morale and the target morale. Leveling up the Propaganda Office further increases the positive effect on the target morale. The Propaganda Office can be constructed in all provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 0.10 	### in percentage ###
				self.construction_costs = {'gas': 800, 'corn': 1000, 'cash': 1800}
				self.construction_time = 3
			case 2:
				self.health = 60
				self.effects = 0.23
				self.construction_costs = {'cash': 2400, 'corn': 1350, 'gas': 1050}
				self.construction_time = 6
			case 3:
				self.health = 120
				self.effects = 0.40
				self.construction_time = {'gas': 1400, 'corn': 1800, 'cash': 3200}
				self.construction_costs = 9
			case _:
				raise ValueError("This level does not exist")


class Bunkers(Buildings):
	def __init__(self, level, game):
		super().__init__(self, level, game)
		self.description = "Bunkers reduce the amount of damage taken by other buildings and units stationed in the center of this province. Leveling up Bunkers increases the damage reduction further. Bunkers at level 3 or higher also hide the army composition of stationed armies, which can be revealed by certain scout units. Bunkers can only be constructed in urban provinces."
		match self.level:
			case 1:
				self.health = 40
				self.effects = -0.15	### represents the percentage of damage reduction for stationed troops and buildings ###
				self.construction_costs = {'steel': 850, 'gas': 650, 'cash': 1500}
				self.construction_time = 6
			case 2:
				self.health = 80
				self.effects = -0.30
				self.construction_costs = {'steel': 1150, 'gas': 850, 'cash': 2000}
				self.construction_time = 9
			case 3:
				self.health = 120
				self.effects = -0.45
				self.construction_costs = {'steel': 1550, 'gas': 1150, 'cash': 2650}
				self.construction_time = 12
			case 4:
				self.health = 160
				self.effects = -0.60
				self.construction_costs = {'steel': 2050, 'gas': 1550, 'cash': 3500}
				self.construction_time = 15
			case 5:
				self.health = 200
				self.effects = -0.75
				self.construction_costs = {'gas': 2050, 'steel': 2750, 'cash': 4650}
				self.construction_time = 18
			case _:
				raise ValueError("This level does not exist")


class Infrastructure(Buildings):
	def __init__(self, level, game):
		super().__init__(self, level, game)
		self.description = "Infrasture increases the movement speed of units anywhere within this province. Leveling up the Infrastructure incrases the movement speed bonus further. Infrastrure can be constructed in all provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 0.67	### Unit speed percentage ###
				self.construction_costs = {'steel': 600, 'gas': 400, 'cash': 1000}
				self.construction_time = 4
			case 2:
				self.health = 60
				self.effects = 1.33
				self.construction_costs = {'steel': 700, 'gas': 500, 'cash': 1200}
				self.construction_time = 8
			case 3:
				self.health = 120
				self.effects = 2
				self.construction_costs = {'gas': 600, 'steel': 850, 'cash': 1450}
				self.construction_time = 12
			case _:
				raise ValueError("This level does not exist")


class Capital(Buildings):
	def __init__(self, level, game):
		super().__init__(self, level, game)
		self.description = "The Capitol is required to keep up morale n the territory of a country. The farther away a province is from the Capitol, the higher the negative impact on that province's morale. The Capitol also provides a positive effect on the morale influences of the capital province. Losing the Capitol reuces morale of the owner's provinces, increases the morale of the conquerer's provinces and lets the conquerer steal a portion of the owner's money. The Capitol can only exist once per country, but can be moved to another province. The Capitol can only be constructed in urban provinces."
		match self.level:
			case 1:
				self.health = 100
				self.effects = 0.10
				self.construction_costs = {'steel': 1250, 'corn': 1250, 'cash': 2500}
				self.construction_time = 12	### hours ##			
			case _:
				raise ValueError("This level does not exist")
#

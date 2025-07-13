class Buildings:
	def __init__(self, level, game):
		self.level = level
		self.game = game	### Python game object ###
	def upgrade(self, level=None):
		if level:
			self.level = level
		else:
			self.level += 1
	def __str__(self):
		return f"Level: {self.level}\nFaction: {self.game.faction}\n"

class Barracks(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "Barracks are required to recruit Infantry units. Each level of the Barracks halves the unit production time until the minimum production time of a unit is reached. Barracks can only be constructed in ubran provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 100	### Unit production effect ###
				self.costs = {'steel': 1350, 'corn': 2250, 'cash': 3600}
				self.construction_time = 0.083	### 5 minutes ###

class Ordance_Foundry(Buildings):	
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Ordance Foundry is required to produce support units that usualy feature larger gun calibers. Each level of the Ordance Foundry halves the unit production time until the minimum prodction time of a unit is reached. The Ordance Foundry can only be constructed un urban provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 100
				self.costs = {'gas': 2400, 'corn': 1200, 'cash': 3600}
				self.construction_time = 0.083
class Tank_Plant(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Tank Plant is required to produce tank units. Each level of the Tank Plant halves the unit production time until the minimum production time of a unit is reached. The Tank Plant can only be constructed in urban provices."
		match self.level:	
			case 1:
				self.health = 20
				self.effects = 100
				self.costs = {'steel': 2100, 'gas': 1500, 'cash': 3600}
				self.construction_time = 0.083

class Aircraft_Factory(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Aircraft Factory is required to produce air units and allows aircrafts to take off or land in this province. Each level of the Aircraft Factory halves the unit production time until the minimum production time of a unit is reached. Each building level also reduces the refueling times of airplanes in this province. The Aircraft Factory can only be constructed in urban provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 100
				self.refueling_time = 0.5	### in hours ###
				self.costs = {'gas': 2350, 'corn': 1250, 'cash': 3600}
				self.construction_time = 0.5

class Secret_Lab(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Secret Lab is required to produce secret weapons. Each level of the Secret Lab halves the unit production time until the minimum production time of a unit is reached. The current level of the Secret Lab is hidden to others. The Secret Lab can only constructed in urban provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 100
				self.costs = {'steel': 1400, 'gas': 2200, 'cash': 3600}
				self.construction_time = 0.5

class Industry(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Industry increases the production rates of resorces and money in this province. Leveling up the Industry increases these production rates further. Industry can only be constructed in urban provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 13	### Production boost in percentage ###
				self.costs = {'steel': 1400, 'gas': 1600, 'cash': 3000}
				self.construction_time = 8	### in hours ###
			case 2:
				self.health = 40
				self.effects = 28
				self.costs = {'steel': 1850, 'gas': 2150, 'cash': 4000}
				self.construction_time = 14

class Recruiting_Station(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Recruiting Station increases the manpower production rate in this province. LEveling up the Recruiting Station increases the manpower production rate further. The Recruiting Station can be constructed in all provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 35 	### manpower production boost in percentage ###
				self.costs = {'steel': 1100, 'corn': 1600, 'cash': 2700}
				self.construction_time = 6 	### in hours ###

class Propaganda_Office(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Propaganda Office helps to improve the morale of a province over time by raising its target morale. Province morale increases or decreases at daychange towards the target morale, by an amount that is dependent on the difference between the current morale and the target morale. Leveling up the Propaganda Office further increases the positive effect on the target morale. The Propaganda Office can be constructed in all provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 10 	### in percentage ###
				self.costs = {'gas': 800, 'corn': 1000, 'cash': 1800}
				self.construction_time = 3

class Bunkers(Buildings):
	def __init__(self, level, game):
		super().__init__(self, level, game)
		self.description = "Bunkers reduce the amount of damage taken by other buildings and units stationed in the center of this province. Leveling up Bunkers increases the damage reduction further. Bunkers at level 3 or higher also hide the army composition of stationed armies, which can be revealed by certain scout units. Bunkers can only be constructed in urban provinces."
		match self.level:
			case 1:
				self.health = 40
				self.effects = -15	### represents the percentage of damage reduction for stationed troops and buildings ###
				self.costs = {'steel': 850, 'gas': 650, 'cash': 1500}
				self.construction_time = 6

class Infrastructure(Buildings):
	def __init__(self, level, game):
		super().__init__(self, level, game)
		self.description = "Infrasture increases the movement speed of units anywhere within this province. Leveling up the Infrastructure incrases the movement speed bonus further. Infrastrure can be constructed in all provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 67	### Unit speed percentage ###
				self.costs = {'steel': 600, 'gas': 400, 'cash': 1000}
				self.construction_time = 4


class Capital(Buildings):
	def __init__(self, level, game):
		super().__init__(self, level, game)
		self.description = "The Capitol is required to keep up morale n the territory of a country. The farther away a province is from the Capitol, the higher the negative impact on that province's morale. The Capitol also provides a positive effect on the morale influences of the capital province. Losing the Capitol reuces morale of the owner's provinces, increases the morale of the conquerer's provinces and lets the conquerer steal a portion of the owner's money. The Capitol can only exist once per country, but can be moved to another province. The Capitol can only be constructed in urban provinces."
		match self.level:
			case 1:
				self.health = 100
				self.effects = 10
				self.costs = {'steel': 1250, 'corn': 1250, 'cash': 2500}
				self.construction_time = 12	### hours ###

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
				self.upgrade_costs = {'steel': 1350, 'corn': 2250, 'cash': 3600}
				self.upgrade_time = 0.083	### 5 minutes ###
			case 2:
				self.health = 40
				self.effects = 200
				self.upgrade_costs = {'steel': 1800, 'corn': 3000, 'cash': 4800}
				self.upgrade_time = 4

class Ordance_Foundry(Buildings):	
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Ordance Foundry is required to produce support units that usualy feature larger gun calibers. Each level of the Ordance Foundry halves the unit production time until the minimum prodction time of a unit is reached. The Ordance Foundry can only be constructed un urban provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 100
				self.upgrade_costs = {'gas': 2400, 'corn': 1200, 'cash': 3600}
				self.upgrade_time = 0.083
class Tank_Plant(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Tank Plant is required to produce tank units. Each level of the Tank Plant halves the unit production time until the minimum production time of a unit is reached. The Tank Plant can only be constructed in urban provices."
		match self.level:	
			case 1:
				self.health = 20
				self.effects = 100
				self.upgrade_costs = {'steel': 2100, 'gas': 1500, 'cash': 3600}
				self.upgrade_time = 0.083
			case 2:
				self.health = 40
				self.effects = 200
				self.upgrade_costs = {'steel': 2800, 'gas': 2000, 'cash': 4800}
				self.upgrade_time = 4

class Aircraft_Factory(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Aircraft Factory is required to produce air units and allows aircrafts to take off or land in this province. Each level of the Aircraft Factory halves the unit production time until the minimum production time of a unit is reached. Each building level also reduces the refueling times of airplanes in this province. The Aircraft Factory can only be constructed in urban provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 100
				self.refueling_time = 30	### in minutes ###
				self.upgrade_costs = {'gas': 2350, 'corn': 1250, 'cash': 3600}
				self.upgrade_time = 0.5
			case 2:
				self.health = 40
				self.effects = 200
				self.refueling_time = 25
				self.upgrade_costs = {'gas': 3150, 'corn': 1650, 'cash': 4800}
				self.upgrade_time = 4

class Secret_Lab(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Secret Lab is required to produce secret weapons. Each level of the Secret Lab halves the unit production time until the minimum production time of a unit is reached. The current level of the Secret Lab is hidden to others. The Secret Lab can only constructed in urban provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 100
				self.upgrade_costs = {'steel': 1400, 'gas': 2200, 'cash': 3600}
				self.upgrade_time = 0.5
			case 2:
				self.health = 40
				self.effects = 200
				self.upgrade_costs = {'steel': 1850, 'gas': 2950, 'cash': 4800}
				self.upgrade_time = 4

class Industry(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Industry increases the production rates of resorces and money in this province. Leveling up the Industry increases these production rates further. Industry can only be constructed in urban provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 13	### Production boost in percentage ###
				self.upgrade_costs = {'steel': 1400, 'gas': 1600, 'cash': 3000}
				self.upgrade_time = 8	### in hours for next industry, so for industry 2 ###
			case 2:
				self.health = 40
				self.effects = 28
				self.upgrade_costs = {'steel': 1850, 'gas': 2150, 'cash': 4000}
				self.upgrade_time = 14
			case 3:
				self.health = 50
				self.effects = 50
				self.upgrade_costs = {'steel': 2450, 'gas': 2850, 'cash': 5300}
				self.upgrade_time = 20
			case 4:
				self.health = 120	
				self.effects = 80
				self.upgrade_costs = {'steel': 3250, 'gas': 3800, 'cash': 7050}
				self.upgrade_time = 26
			case 5:
				self.health = 160
				self.effects = 120
				self.upgrade_costs = None
				self.upgrade_time = None
class Recruiting_Station(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Recruiting Station increases the manpower production rate in this province. LEveling up the Recruiting Station increases the manpower production rate further. The Recruiting Station can be constructed in all provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 35 	### manpower production boost in percentage ###
				self.upgrade_costs = {'steel': 1100, 'corn': 1600, 'cash': 2700}
				self.upgrade_time = 6 	### in hours ###
			case 2:
				self.health = 60
				self.effects = 100
				self.upgrade_costs = {'steel': 1450, 'corn': 2150, 'cash': 3600}
				self.upgrade_time = 12

class Propaganda_Office(Buildings):
	def __init__(self, level, game):
		super().__init__(level, game)
		self.description = "The Propaganda Office helps to improve the morale of a province over time by raising its target morale. Province morale increases or decreases at daychange towards the target morale, by an amount that is dependent on the difference between the current morale and the target morale. Leveling up the Propaganda Office further increases the positive effect on the target morale. The Propaganda Office can be constructed in all provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 10 	### in percentage ###
				self.upgrade_costs = {'gas': 800, 'corn': 1000, 'cash': 1800}
				self.upgrade_time = 3
			case 2:
				self.health = 60
				self.effects = 23
				self.upgrade_costs = {'cash': 2400, 'corn': 1350, 'gas': 1050}
				self.upgrade_time = 6
			case 3:
				self.health = 120
				self.effects = 40
				self.upgrade_

class Bunkers(Buildings):
	def __init__(self, level, game):
		super().__init__(self, level, game)
		self.description = "Bunkers reduce the amount of damage taken by other buildings and units stationed in the center of this province. Leveling up Bunkers increases the damage reduction further. Bunkers at level 3 or higher also hide the army composition of stationed armies, which can be revealed by certain scout units. Bunkers can only be constructed in urban provinces."
		match self.level:
			case 1:
				self.health = 40
				self.effects = -15	### represents the percentage of damage reduction for stationed troops and buildings ###
				self.upgrade_costs = {'steel': 850, 'gas': 650, 'cash': 1500}
				self.upgrade_time = 6
			case 2:
				self.health = 80
				self.effects = -30
				self.upgrade_costs = {'steel': 1150, 'gas': 850, 'cash': 2000}
				self.upgrade_time = 9
			case 3:
				self.health = 120
				self.effects = -45
				self.upgrade_costs = {'steel': 1550, 'gas': 1150, 'cash': 2650}
				self.upgrade_time = 12
			case 4:
				self.health = 160
				self.effects = -60
				self.upgrade_costs = {'steel': 2050, 'gas': 1550, 'cash': 3500}
				self.upgrade_time = 15
			case 5:
				self.health = 200
				self.effects = -75
				self.upgrade_costs = None
				self.upgrade_time = None

class Infrastructure(Buildings):
	def __init__(self, level, game):
		super().__init__(self, level, game)
		self.description = "Infrasture increases the movement speed of units anywhere within this province. Leveling up the Infrastructure incrases the movement speed bonus further. Infrastrure can be constructed in all provinces."
		match self.level:
			case 1:
				self.health = 20
				self.effects = 67	### Unit speed percentage ###
				self.upgrade_costs = {'steel': 600, 'gas': 400, 'cash': 1000}
				self.upgrade_time = 4
			case 2:
				self.health = 60
				self.effects = 133
				self.upgrade_costs = {'steel': 700, 'gas': 500, 'cash': 1200}
				self.upgrade_time = 8


class Capital(Buildings):
	def __init__(self, level, game):
		super().__init__(self, level, game)
		self.description = "The Capitol is required to keep up morale n the territory of a country. The farther away a province is from the Capitol, the higher the negative impact on that province's morale. The Capitol also provides a positive effect on the morale influences of the capital province. Losing the Capitol reuces morale of the owner's provinces, increases the morale of the conquerer's provinces and lets the conquerer steal a portion of the owner's money. The Capitol can only exist once per country, but can be moved to another province. The Capitol can only be constructed in urban provinces."
		match self.level:
			case 1:
				self.health = 100
				self.effects = 10
				self.upgrade_costs = {'steel': 1250, 'corn': 1250, 'cash': 2500}
				self.upgrade_time = 12	### hours ###

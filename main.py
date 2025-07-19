import game
import units
import buildings

def run_game():
	my_game = game.Game("Game 1", "Ohio", "Axis", resources={'corn': 10000, 'steel': 10000, 'gas': 10000, 'cash': 10000, 'manpower': 10000})

	building1 = my_game.add_building(buildings.Recruiting_Station, 3, 113)
	print(building1)
	unit1 = my_game.add_unit(units.Militia, 1)
	print(unit1)

	unit2 = my_game.add_unit(units.Motorized_Infantry, 3)
	print(unit2)

	building2 = my_game.add_building(buildings.Industry, 1, "corn", 2000)

	print(building2)

	print(my_game.resources)
	my_game.resources.day_change()
	print(my_game.resources)

if __name__ == "__main__":
	run_game()

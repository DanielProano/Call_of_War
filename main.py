import game, units, buildings, stack

def run_game():
	my_game = game.Game("Game 1", "Ohio", "Axis", resources={'corn': 50000, 'steel': 50000, 'gas': 50000, 'cash': 100000, 'manpower': 50000}, production={'corn': 50, 'steel': 60}, upkeep={'corn': 500, 'cash': 700})

	print(my_game)

	u1 = my_game.add_unit(units.Mechanized_Infantry, 3)

	print(u1)

	t1 = my_game.add_unit(units.Armored_Car, 2)

	b1 = my_game.add_building(buildings.Barracks, 4)

	b2 = my_game.add_building(buildings.Industry, 3, 'corn', 100)

	print(my_game.resources)

	stack1 = my_game.create_stack(territory='hills')

	stack1.create_units(units.Armored_Car, level=2, num=6)

	print(stack1)

	
if __name__ == "__main__":
	run_game()

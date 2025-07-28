import game
import units
import buildings

def run_game():
	my_game = game.Game("Game 1", "Ohio", "Axis", resources={'corn': 10000, 'steel': 10000, 'gas': 10000, 'cash': 100000, 'manpower': 10000})


	unit = my_game.add_unit(units.Infantry, 1)

	stack2 = my_game.create_stack(units.Militia, 2, number=2)

	joined = my_game.join_stacks(stack2, unit)

	for i in joined:
		print(i)

if __name__ == "__main__":
	run_game()

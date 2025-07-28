import game
import units
import buildings
import stack

def run_game():
	my_game = game.Game("Game 1", "Ohio", "Axis", resources={'corn': 10000, 'steel': 10000, 'gas': 10000, 'cash': 100000, 'manpower': 10000})


	stack1 = stack.Stack(my_game, territory="hills")

	stack1.create_units(units.Infantry, level=2, num=2)

	stack2 = stack.Stack(my_game, territory="mountains")
		
	stack2.create_units(units.Militia, level=3, num=1)

	stack1.combine_with(stack2)

	print(stack1.units)

	print(stack2.units)

if __name__ == "__main__":
	run_game()

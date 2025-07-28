import game
import units
import buildings
import stack

def run_game():
	my_game = game.Game("Game 1", "Ohio", "Axis", resources={'corn': 10000, 'steel': 10000, 'gas': 10000, 'cash': 100000, 'manpower': 10000})


	stack1 = my_game.create_stack(territory="hills")

	stack1.create_units(units.Infantry, level=2, num=3)

	stack2 = my_game.create_stack(territory="mountains")
		
	stack2.create_units(units.Militia, level=3, num=1)

	stack1.combine_with(stack2)

	print(stack1)
if __name__ == "__main__":
	run_game()

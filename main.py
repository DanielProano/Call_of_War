import game
import units
import buildings

def run_game():
	my_game = game.Game("Game 1", "Ohio", "Axis", resources={'corn': 10000, 'steel': 10000, 'gas': 10000, 'cash': 10000, 'manpower': 10000}, production={'corn': 150})

	building1 = my_game.add_building(buildings.Industry, 4, 'corn', 100)
	
	print(my_game.resources)

if __name__ == "__main__":
	run_game()

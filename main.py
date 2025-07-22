import game
import units
import buildings

def run_game():
	my_game = game.Game("Game 1", "Ohio", "Axis", resources={'corn': 10000, 'steel': 10000, 'gas': 10000, 'cash': 100000, 'manpower': 10000})

	building1 = my_game.add_building(buildings.Recruiting_Station, 1, 100)
	b2 = my_game.add_building(buildings.Barracks, 1)

	b3 = my_game.add_building(buildings.Ordance_Foundry, 2)

	b4 = my_game.add_building(buildings.Secret_Lab, 1)
	

if __name__ == "__main__":
	run_game()

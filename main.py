import game as Game
import units as Units
import buildings as Buildings

def run_game():
	game = Game.Game("Game 1", "Ohio", "Axis", resources={'corn': 10000, 'steel': 10000, 'gas': 10000, 'cash': 10000, 'manpower': 10000})

	building = game.add_building(Buildings.Recruiting_Station, 3, 113)

	print(building)
	print(game.resources)
	game.resources.day_change()
	print(game.resources)

if __name__ == "__main__":
	run_game()

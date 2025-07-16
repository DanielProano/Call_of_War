import game, units, buildings

game = game.Game("Game 1", "Ohio", "Axis", resources={'corn': 10000, 'steel': 10000, 'gas': 10000, 'cash': 50000, 'manpower': 30000})

building = game.add_building(buildings.Barracks, 1, game)

print(building)

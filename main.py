import game, units, buildings

game = game.Game("Game 1", "Ohio", "Axis", resources={'corn': 10000, 'steel': 10000, 'gas': 10000, 'cash': 10000, 'manpower': 10000})

building = game.add_building(buildings.Industry, 3, "corn", 113)

print(building)
print(game.resources)
print(game.buildings)

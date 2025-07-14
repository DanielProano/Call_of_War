import game, units

game = game.Game("Game 1", "Ohio", "Axis", resources={'corn': 10000, 'steel': 10000, 'gas': 10000, 'cash': 50000, 'manpower': 30000})

militia = game.add_unit(units.Militia, 3)

infantry = game.add_unit(units.Infantry, 1)

militia.fight(infantry)


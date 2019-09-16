from wifi import Cell, Scheme
#Cell.all('wlan0')
cell = Cell.all('wlan0')[0]
passkey='iloveicns'
scheme = Scheme.for_cell('wlan0', 'icnslab', cell, passkey)
scheme.save()
scheme.activate()

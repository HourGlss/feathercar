import microcontroller,board
for pin in dir(microcontroller.pin):
	if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
		pins = ["{:28s} ".format("microcontroller.pin."+pin)]
		for alias in dir(board):
			if getattr(board, alias) is getattr(microcontroller.pin, pin):
				pins.append("board.{}".format(alias))
		print(" ".join(pins))
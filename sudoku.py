import numpy as np


def printboard(board):
	size = len(board)
	lines = np.sqrt(size)
	for x in range(0, size):
		if np.mod(x, lines) == 0: 
			print(" "), 
			for z in range(0, size): 
				print("__ "),
			print("\n"), 
		for y in range(0, size):
			num = board[x][y]
			if np.mod(y, lines) == 0: ###y == 0:
				print("|"),
			else:
				print(" "),
			print(num),
		print("\n"), 


def main():
	print "Welcome to my sudoku solver!"
	size = input("Enter the size of the board:")
	print "Board size is", size
	if (int(np.sqrt(size)))**2 != size:
		print "size is not a square"

	###creating the board
	board = np.zeros((size, size), dtype=int)
	print board
	printboard(board)


	##entering known values to board




if __name__ == "__main__":
	main() 

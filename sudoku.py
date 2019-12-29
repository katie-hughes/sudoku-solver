import numpy as np



def main():
	print "Welcome to my sudoku solver!"
	size = input("Enter the size of the board:")
	print "Board size is", size
	if (int(np.sqrt(size)))**2 != size:
		print "size is not a square"

	###creating the board
	board = np.zeros((size, size))
	print board




if __name__ == "__main__":
	main() 

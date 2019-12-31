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


def countarray(arr, number):
	count = 0
	size = len(arr)
	for x in range(0, size):
		if arr[x] == number:
			count += 1
	return count

def checkline(arr):
	print "the array is", arr
	size = len(arr)
	for x in range(1, size+1):
		count = countarray(arr, x);
		###print "there are", count, x, "'s in the array", arr
		if count > 1:
			return 0
	return 1
	

###check that there are no duplicates in rows/cols/boxes
def sanitycheck(board): 
	size = len(board)
	print "checking the rows"
	for x in range(0, size):
		row = board[x]
		res = checkline(row)
		if res == 0:
			return 0 
	print "checking the columns"
	transp = np.transpose(board)
	for y in range(0, size): 
		col = transp[y]
		res = checkline(col)
		if res == 0:
			return 0
	print "checking the boxes"
	sqt = int(np.sqrt(size))
	for w in range(0, sqt):
		for x in range(0, sqt):
			box = np.zeros(size, dtype=int)
			count = 0; 
			for y in range(0, sqt):
				for z in range(0, sqt):
					num = board[sqt*w+y][sqt*x+z]
					##print "num is", num
					##print "position", str(sqt*w+y), str(sqt*x+z)
					box[count] = num
					count += 1
			count = 0
			res = checkline(box)
			if res == 0:
				return 0
	return 1; 

def fillinone(line):
	##first, check if there is only one number missing.
	c0 = countarray(line, 0)
	if c0 == 1:
		##find the missing number
		size = len(line)
		missing = 0
		for x in range(1, size+1):
			##counting occurences of x in the line.
			cx = countarray(line, x)
			if cx == 0:  ###x is the missing number. 
				missing = x
		for x in range(0, size):
			if line[x] == 0:
				line[x] = missing


def main():
	print "Welcome to my sudoku solver!"
	size = input("Enter the size of the board:")
	print "Board size is", size
	if (int(np.sqrt(size)))**2 != size:
		print "size is not a square"
		exit()
	###creating the board
	board = np.zeros((size, size), dtype=int)
	print board
	printboard(board)


	##entering known values to board
	print "please enter in the known numbers:"
	while(1):
		try:
			r, c, n = raw_input("[row] [column] [number]:").split()
			print "Entering", n, "to position (", r, ",", c, ")"
			r = int(r)
			c = int(c)
			n = int(n)
			if( (1<= r<= size) and (1<= c<=size) and (1<= n<=size)):
				board[r-1][c-1] = n   ##b/c 0 indexing
			else:
				print "One of your inputs does not fit the board size."
				continue
		except:
			print("That was a weird input")
		try:
			temp = raw_input("Type 0 if you are done inputting: ")
			if int(temp) == 0:
				break
		except:
			pass
	print "Going to start!"
	print "This puzzle requires numbers from 1 -", size, "in each row, column, and square."
	printboard(board)
	print "Performing preliminary check"
	sc = sanitycheck(board)
	if sc == 0:
		print("There is an error with the numbers you inputted.")
		exit()
	print "All good! Onwards!"
	printboard(board)


if __name__ == "__main__":
	main() 

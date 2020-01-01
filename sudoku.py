import numpy as np


possibilities = []

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
	return 1

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
		print "the missing number in line", line, "is", missing
		for y in range(0, size):
			if line[y] == 0:
				line[y] = missing
		return 1
	else:
		return 0


def singlemissing(board):
	size = len(board)
	ret = 0
	print "filling in one on rows"
	for x in range(0, size):
		row = board[x]
		res = fillinone(row)
		ret += res
	print "filling in one on columns"
	transp = np.transpose(board)
	for y in range(0, size): 
		col = transp[y]
		res = fillinone(col)
		ret += res
	print "filling in one on boxes"
	sqt = int(np.sqrt(size))
	for w in range(0, sqt):
		for x in range(0, sqt):
			box = np.zeros(size, dtype=int)
			count = 0; 
			for y in range(0, sqt):
				for z in range(0, sqt):
					num = board[sqt*w+y][sqt*x+z]
					box[count] = num
					count += 1
			count = 0
			res = fillinone(box)
			### the issue: the array created for the box is separate from the board array. 
			for a in range(0, sqt):
				for b in range(0, sqt):
					board[sqt*w+a][sqt*x+b] = box[count]
					count += 1
			count = 0
			ret += res
	return ret 

##given an element, return the row/col/box arrays:
def selectrow(board, row, col):
	return board[row]

def selectcol(board, row, col):
	transp = np.transpose(board)
	return transp[col]

def selectbox(board, row, col):
	###this is the tricky one.
	size = len(board)
	sqt = int(np.sqrt(size))
	r = row / sqt
	c = col / sqt ###returns number in range (0, sqt)
	box = np.zeros(size, dtype=int)
	count = 0
	for x in range(0, sqt):
		for y in range(0, sqt):
			num = board[sqt*r+x][sqt*c+y]
			box[count] = num
			count += 1
	return box

def nootheroptions(board):
	size = len(board)
	changes = 0
	for x in range(0, size):
		for y in range(0, size):
			num = board[x][y]
			if num == 0:
				row = selectrow(board, x, y)
				col = selectcol(board, x, y)
				box = selectbox(board, x, y)
				print "for position", str(x), str(y)
				print "row is", row
				print "col is", col
				print "box is", box
				options = range(1, size+1)
				###which numbers are allowed in box? 
				for z in range(1, size+1):
					cr = countarray(row, z)
					cc = countarray(col, z)
					cb = countarray(box, z)
					if ((cr == 1) or (cc == 1) or (cb == 1)):
						##z cannot go in position x, y. 
						print "removing", z, "as an option from position", x, y
						options.remove(z)
						changes += 1
				if len(options) == 1:  ### if there is only one number possible. 
					last = options[0]
					board[x][y] = last
				global possibilities
				possibilities[x][y] = options
	return changes


def checkdone(board):
	##there just needs to be no zeros.
	size = len(board)
	for x in range(0, size):
		line = board[x]
		for y in range(0, size):
			num = line[y]
			if num == 0:
				return 0
	return 1


def main():
	print "Welcome to my sudoku solver!"
	size = input("Enter the size of the board:")
	print "Board size is", size
	if (int(np.sqrt(size)))**2 != size:
		print "size is not a square"
		exit()
	###creating the board
	board = np.zeros((size, size), dtype=int)
	printboard(board)

	##entering known values to board
	print "please enter in the known numbers (for empty, type 0)"
	for x in range(0, size):
		print "For row", x+1, ":", 
		s = raw_input("enter the numbers from left to right: ")
		numbers = map(int, s.split())
		print "numbers are", numbers
		if len(numbers) != size:
			print "oops"
		else:
			numbers = np.array(numbers)
			board[x] = numbers
	"""
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
	"""
	print "Going to start!"
	print "This puzzle requires numbers from 1 -", size, "in each row, column, and square."
	printboard(board)
	raw_input("Press any key to continue.")
	print "Performing preliminary check"
	sc = sanitycheck(board)
	if sc == 0:
		print("There is an error with the numbers you inputted.")
		exit()
	print "All good! Onwards!"
	printboard(board)
	print "filling in one"
	ret = singlemissing(board)
	while(ret):
		print "ret is", ret
		ret = singlemissing(board)
		print "ret after is", ret
	done = checkdone(board)
	if done:
		print "It is solved!"
		printboard(board)
		exit()
	printboard(board)
	print "Something else needs to be done."
	print "Initializing possibilities list"
	global possibilities
	for x in range(0, size):
		possibilities.append([])
		for y in range(0, size):
			possibilities[x].append([])
	print "possibiliteis are", possibilities 
	ret = nootheroptions(board)
	print "possibiliteis are", possibilities 
	while(ret):
		print "ret is ", ret
		ret = nootheroptions(board)
	done = checkdone(board)
	if done:
		print "It is solved!"
		printboard(board)
		exit()
	print "I need to do something else again."
	printboard(board)

if __name__ == "__main__":
	main() 

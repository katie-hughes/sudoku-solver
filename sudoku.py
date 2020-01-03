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
			if num == 0:
				print(" "), 
			else:
				print(num),
			if y == (size-1):
				print("|"), 
		if x == (size-1):
			print("\n"), 
			for z in range(0, size):
				print("__ "), 
		print("\n"), 


def countarray(arr, number):
	count = 0
	size = len(arr)
	for x in range(0, size):
		if arr[x] == number:
			count += 1
	return count

def checkline(arr):
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
	##print "Checking the rows..."
	for x in range(0, size):
		row = board[x]
		res = checkline(row)
		if res == 0:
			return 0 
	##print "Checking the columns..."
	transp = np.transpose(board)
	for y in range(0, size): 
		col = transp[y]
		res = checkline(col)
		if res == 0:
			return 0
	##print "Checking the boxes..."
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
			if cx == 0: ##x is the missing number
				missing = x
		##finding the missing position
		for y in range(0, size):
			if line[y] == 0:
				line[y] = missing
		return 1
	else:
		return 0


def singlemissing(board):
	size = len(board)
	ret = 0
	##print "Filling in one on the rows..."
	for x in range(0, size):
		row = board[x]
		res = fillinone(row)
		board[x] = row
		ret += res
	##print "Filling in one on the columns..."
	transp = np.transpose(board)
	for y in range(0, size): 
		col = transp[y]
		res = fillinone(col)
		transp[y] = col
		board = np.transpose(transp)
		ret += res
	##print "Filling in one on boxes..."
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
			for a in range(0, sqt):
				for b in range(0, sqt):
					board[sqt*w+a][sqt*x+b] = box[count]
					count += 1
			count = 0
			ret += res
	return ret 

##given an square, select its row/column/box
def selectrow(board, row, col):
	return board[row]

def selectcol(board, row, col):
	transp = np.transpose(board)
	return transp[col]

def selectbox(board, row, col):
	size = len(board)
	sqt = int(np.sqrt(size))
	r = row / sqt
	c = col / sqt 
	box = np.zeros(size, dtype=int)
	count = 0
	for x in range(0, sqt):
		for y in range(0, sqt):
			num = board[sqt*r+x][sqt*c+y]
			box[count] = num
			count += 1
	return box


##for a possibilities row/column/box
def poss_occurances(poss, number):
	size = len(poss)
	count = 0
	for x in range(0, size):
		current = poss[x]
		l = len(current)
		for y in range(0, l):
			if current[y] == number:
				count += 1
	return count

##given a row/column/box index, return the list of possibilities
def poss_row(index):
	global possibilities
	return possibilities[index]

def poss_col(index):
	global possibilities
	size= len(possibilities)
	col_poss = []
	for x in range(0, size):
		col_poss.append(possibilities[x][index])
	return col_poss

def poss_box(index):
	global possibilities
	size = len(possibilities)
	sqt = int(np.sqrt(size))
	r = index / sqt
	c = index % sqt ###returns number in range (0, sqt)
	box_poss = []
	for x in range(0, sqt):
		for y in range(0, sqt):
			poss = possibilities[sqt*r+x][sqt*c+y]
			box_poss.append(poss)
	return box_poss

def box_index(size, row, col):
	sqt = int(np.sqrt(size))
	r = row / sqt
	c = col / sqt
	return sqt*r+c
	

##placing a number at a particular location, and updating possibilities list.
def place(num, row, col, board):
	##print "placing", num, "on board", row, col
	board[row][col] = num
	size = len(board)
	global possibilities
	possibilities[row][col] = []
	##fill_possibilities(board)
	remove_poss_row(row, num, board)
	remove_poss_col(col, num, board)
	remove_poss_box(box_index(size, row, col), num, board)
	oneoption(board)
	sc = sanitycheck(board)
	if sc==0:
		print "error"
		exit()

##remove a number from a row/column/box of possibilities.
def remove_poss_row(index, num, board):
	global possibilities
	size = len(possibilities)
	for x in range(0, size):
		poss = possibilities[index][x]
		if num in poss:
			poss.remove(num)
			possibilities[index][x] = poss

def remove_poss_col(index, num, board):
	global possibilities
	size = len(possibilities)
	for x in range(0, size):
		poss = possibilities[x][index]
		if num in poss:
			poss.remove(num)
			possibilities[x][index] = poss

def remove_poss_box(index, num, board): 
	global possibilities
	size = len(possibilities)
	sqt = int(np.sqrt(size))
	r = index / sqt
	c = index % sqt
	for x in range(0, sqt):
		for y in range(0, sqt):
			poss = possibilities[sqt*r+x][sqt*c+y]
			if num in poss:
				poss.remove(num)
				possibilities[sqt*r+x][sqt*c+y] = poss


def fill_possibilities(board):
	size = len(board)
	changes = 0
	for x in range(0, size):
		for y in range(0, size):
			num = board[x][y]
			if num == 0:
				row = selectrow(board, x, y)
				col = selectcol(board, x, y)
				box = selectbox(board, x, y)
				global possibilities
				if len(possibilities[x][y]) == 0:
					options = range(1, size+1)
				else:
					options = possibilities[x][y]
				copy = list(options)
				###which numbers are allowed in box? 
				for z in copy: 
					cr = countarray(row, z)
					cc = countarray(col, z)
					cb = countarray(box, z)
					if ((cr == 1) or (cc == 1) or (cb == 1)):
						##z cannot go in position x, y. 
						options.remove(z)
						changes += 1
				possibilities[x][y] = options
	return changes


def oneoption(board):
	##print "one option"
	size = len(board)
	ret = 0
	global possibilities
	for x in range(0, size):
		for y in range(0, size):
			if len(possibilities[x][y]) == 1:
				num = possibilities[x][y][0]
				place(num, x, y, board)
				ret += 1
	return ret



def onespot(board):
	ret = 0
	size = len(board)
	global possibilities
	for x in range(0, size):
		row_poss = poss_row(x)
		##print "row poss is", row_poss
		###count the occurences of each number in possibilities list. 
		for n in range(1, size+1):
			count = poss_occurances(row_poss, n)
			if count == 1:
				##raw_input("count of something is one")
				##find the corresponding square. 
				for z in range(0, size):
					if n in row_poss[z]:
						place(n, x, z, board)
						ret += 1
	for x in range(0, size):
		col_poss = poss_col(x)
		##print "col poss is", col_poss
		for n in range(1, size+1):
			count = poss_occurances(col_poss, n)
			if count == 1:
				##raw_input("count of something is one")
				for z in range(0, size):
					if n in col_poss[z]:
						##indez z in the col array
						place(n, z, x, board)
						ret += 1
	sqt = int(np.sqrt(size))
	for w in range(0, sqt):
		for x in range(0, sqt):
			box_poss = poss_box(sqt*w+x)
			##print "box poss is", box_poss
			for n in range(1, size+1):
				count = poss_occurances(box_poss, n)
				if count == 1:
					index = 0
					for a in range(0, size):
						if n in box_poss[a]:
							index = a
					itr = 0
					for b in range(0, sqt):
						for c in range(0, sqt):
							if itr == index:
								place(n, sqt*w+b, sqt*x+c, board)
								ret += 1
							itr += 1 
								
	return ret

### 0 false, 1 true
def list_equal(l1, l2):
	ret = 0
	if len(l1) == len(l2):
		size = len(l1)
		for x in range(0, size):
			if l1[x] != l2[x]:
				return 0
		ret = 1
	return ret

def poss_manip2(board):
	global possibilities
	print "doing the rows"
	size = len(board)
	for x in range(0, size):
		row_poss = poss_row(x)
		print "row poss is", row_poss
		indices = []
		for p in range(0, size): 
			if len(row_poss[p]) == 2:
				indices.append(p)
		if len(indices)==2:
			ret = list_equal(row_poss[indices[0]], row_poss[indices[1]])
			if ret:
				##remove the elements that form the two poss.
				n0 = row_poss[indices[0]][0]
				n1 = row_poss[indices[0]][1]
				print "removing", n0, n1, "from row poss"
				##remove_poss_row(x, n0, board) bad b/c removes it from entire row
				##remove_poss_row(x, n1, board) just want to remove from other boxes
				for s in range(0, size):
					if s not in indices:
						if n0 in possibilities[x][s]:
							possibilities[x][s].remove(n0)
						if n1 in possibilities[x][s]:
							possibilities[x][s].remove(n1)
				print "row poss is", poss_row(x)
				oneoption(board)
	print "doing the cols"
	for x in range(0, size):
		col_poss = poss_col(x)
		print "col poss is", col_poss
		indices = []
		for p in range(0, size): 
			if len(col_poss[p]) == 2:
				indices.append(p)
		if len(indices)==2:
			ret = list_equal(col_poss[indices[0]], col_poss[indices[1]])
			if ret:
				##remove the elements that form the two poss.
				n0 = col_poss[indices[0]][0]
				n1 = col_poss[indices[0]][1]
				print "removing", n0, n1, "from col poss"
				for s in range(0, size):
					if s not in indices:
						if n0 in possibilities[s][x]:
							possibilities[s][x].remove(n0)
						if n1 in possibilities[s][x]:
							possibilities[s][x].remove(n1)
				print "col poss is", col_poss
				oneoption(board)
	print "doing the boxes"
	for x in range(0, size):
		box_poss = poss_box(x)
		print "box poss is", box_poss
			

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

def isdone(board):
	done = checkdone(board)
	if done:
		print "It is solved!"
		printboard(board)
		exit()

def main():
	print "Welcome to my sudoku solver!"
	
	size = 0
	while(1):	
		try:
			s = raw_input("Enter the size of the board:")
			size = int(s)
			print "Initializing a", size, "x", size, "sudoku board."
			if (int(np.sqrt(size)))**2 != size:
				print "The size must be a square."
			else:
				break
		except:
			print "Input should be a single number."
	###creating the board
	print "This puzzle requires numbers from 1 -", size, "in each row, column, and box."
	board = np.zeros((size, size), dtype=int)

	##entering known values to board
	print "Please enter in the known numbers by row, from left to right, separated by spaces (for empty, type 0)"
	for x in range(0, size):
		while(1):
			try:
				print "Row", x+1, 
				s = raw_input(": ")
				numbers = map(int, s.split())
				##print "numbers are", numbers
				if len(numbers) != size:
					print "Input should contain", size, "numbers."
				else:
					numbers = np.array(numbers)
					board[x] = numbers
					break
			except:
				print "Unrecognized input."

	printboard(board)
	raw_input("Press any key to continue.")
	print "Performing preliminary check..."
	sc = sanitycheck(board)
	if sc == 0:
		print("There is an error with the numbers you inputted.")
		exit()
	print "All good!"

	print "Checking for cases where a row, column, or box is only missing one number.",
	raw_input("Press any key to continue.")
	c0 = 0
	ret = singlemissing(board)
	c0 += ret
	while(ret):
		ret = singlemissing(board)
		c0 += ret
	
	print c0, "numbers inputted with this method."

	isdone(board)
	printboard(board)

	print "Initializing a list of possible numbers for each square."
	global possibilities
	for x in range(0, size):
		possibilities.append([])
		for y in range(0, size):
			possibilities[x].append([])
	changes = fill_possibilities(board)
	print changes, "numbers removed from the possibilities list."
	
	print "Checking for cases where there is only one possible number allowed in a square.",
	raw_input("Press any key to continue.")
	c1 = 0
	ret = oneoption(board)
	c1 += ret
	while ret:
		ret = oneoption(board)
		c1 += ret
	
	print c1, "numbers inputted with this method."
	
	isdone(board)
	printboard(board)

	print "Checking for cases where a number is only allowed in one square in a row, column, or box.",
	raw_input("Press any key to continue.")
	c2 = 0
	ret = onespot(board)
	c2 += ret
	while(ret):
		ret = onespot(board)
		c2 += ret

	print c2, "numbers inputted with this method."

	isdone(board)
	printboard(board)
	
	raw_input("Performing further possibilities manipulations:")
	poss_manip2(board)
	isdone(board)
	printboard(board)
	print "I need to do something else."

if __name__ == "__main__":
	main()

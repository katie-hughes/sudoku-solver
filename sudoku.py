import numpy as np
from itertools import combinations
import time

possibilities = []


#=========================B=O=A=R=D===S=E=T=U=P=================================

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
			print(" "),
			for z in range(0, size):
				print("__ "),
		print("\n"),

#returns the number of occurances of a number in an array.
def countarray(arr, number):
	count = 0
	size = len(arr)
	for x in range(0, size):
		if arr[x] == number:
			count += 1
	return count

##helper for sanity check to ensure that there's not more
##than one number in a line.
def checkline(arr):
	size = len(arr)
	for x in range(1, size+1):
		count = countarray(arr, x);
		if count > 1:
			return 0
	return 1

###check that there are no duplicates in rows/cols/boxes
def sanitycheck(board):
	size = len(board)
	for x in range(0, size):
		row = board[x]
		res = checkline(row)
		if res == 0:
			return 0
	transp = np.transpose(board)
	for y in range(0, size):
		col = transp[y]
		res = checkline(col)
		if res == 0:
			return 0
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



#===============================================================================


##given a line, see if there is only one number missing.
##If yes, fill it into the line, and return 1.
def fillinone(line):
	##first, check if there is only one number missing.
	c0 = countarray(line, 0)
	if c0 == 1:
		##find the missing number
		size = len(line)
		missing = 0
		for x in range(1, size+1):
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

##checks for cases where rows/cols/boxes are only missing one number.
##does not use possibilities
def singlemissing(board):
	size = len(board)
	ret = 0
	for x in range(0, size):
		row = board[x]
		res = fillinone(row)
		board[x] = row
		ret += res
	transp = np.transpose(board)
	for y in range(0, size):
		col = transp[y]
		res = fillinone(col)
		transp[y] = col
		board = np.transpose(transp)
		ret += res
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


#===============================================================================


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


#===============================================================================


##for a possibilities row/column/box
##count the number of occurances of a number.
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

def printposs():
	global possibilities
	size = len(possibilities)
	##ROWS
	for x in range(0, size):
		print "row", x, poss_row(x)
	for y in range(0, size):
		print "col", y, poss_col(y)
	for z in range(0, size):
		print "box", z, poss_box(z)

def posscheck(board):
	size = len(board)
	ret = 1
	global possibilities
	for x in range(0, size):
		for y in range(0, size):
			num = board[x][y]
			poss = possibilities[x][y]
			l = len(poss)
			##print "num is", num, "poss is", poss
			if (num == 0) and (l == 0):
				print "error with poss!!!!"
				print "pos", x, y
				ret = 0
			if (num != 0) and (l != 0):
				print "error 2 with poss!!!"
				ret = 0
	return ret

def box_index(size, row, col):
	sqt = int(np.sqrt(size))
	r = row / sqt
	c = col / sqt
	return sqt*r+c


#===============================================================================


##placing a number at a particular location, and updating possibilities list.
def place(num, row, col, board):
	##print "placing", num, "on board", row, col
	if board[row][col] != 0:
		print "wtf"
		exit()
	else:
		board[row][col] = num
		size = len(board)
		global possibilities
		possibilities[row][col] = []
		remove_poss_row(row, num, board)
		remove_poss_col(col, num, board)
		remove_poss_box(box_index(size, row, col), num, board)
		oneoption(board)
		sc = sanitycheck(board)
		if sc==0:
			print "error"
			exit()

##remove a number from a row/column/box of possibilities.
def remove_poss_row(index, num, board):   ##indices = None
	global possibilities
	size = len(possibilities)
	#if indices=one:
	##print "row before:", poss_row(index)
	for x in range(0, size):
		poss = possibilities[index][x]
		if num in poss:
			poss.remove(num)
			possibilities[index][x] = poss
	##print "row after:", poss_row(index)

def remove_poss_col(index, num, board):
	global possibilities
	size = len(possibilities)
	##print "col before:", poss_col(index)
	for x in range(0, size):
		poss = possibilities[x][index]
		if num in poss:
			poss.remove(num)
			possibilities[x][index] = poss
	##print "col after:", poss_col(index)

def remove_poss_box(index, num, board):
	global possibilities
	size = len(possibilities)
	sqt = int(np.sqrt(size))
	r = index / sqt
	c = index % sqt
	##print "box before:", poss_box(index)
	for x in range(0, sqt):
		for y in range(0, sqt):
			poss = possibilities[sqt*r+x][sqt*c+y]
			if num in poss:
				poss.remove(num)
				possibilities[sqt*r+x][sqt*c+y] = poss
	##print "box after:", poss_box(index)


##fill the list of possibilities. Should be done after initialization
##of the possibilities list, but can in theory be done later too.
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

def initialize_possibilities(board, size, slow):
	if slow:
		print "Initializing a list of possible numbers for each square."
	global possibilities
	for x in range(0, size):
		possibilities.append([])
		for y in range(0, size):
			possibilities[x].append([])
	changes = fill_possibilities(board)
	if slow:
		print changes, "numbers removed from the overall list of possibilities."


#============================M=E=T=H=O=D=S======================================

###there is only one option in the possibilities list.
def oneoption(board):
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


#a number can only go in one spot in a row/col/box
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
				##find the corresponding square.
				for z in range(0, size):
					if n in row_poss[z]:
						place(n, x, z, board)
						ret += 1
						break
	for x in range(0, size):
		col_poss = poss_col(x)
		##print "col poss is", col_poss
		for n in range(1, size+1):
			count = poss_occurances(col_poss, n)
			if count == 1:
				for z in range(0, size):
					if n in col_poss[z]:
						##indez z in the col array
						place(n, z, x, board)
						ret += 1
						break
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


def list_manip(lst):
	size = len(lst)
	numbers = []
	for x in range(0, size):
		ind = lst[x]

def poss_manip(board):
	count = 0
	global possibilities
	size = len(board)
	for x in range(0, size):
		row_poss = poss_row(x)
		##print "row poss is", row_poss
		indices = []
		poss2 = []
		for p in range(0, size):
			if len(row_poss[p]) == 2:
				indices.append(p)
				poss2.append(row_poss[p])
		###indices contains a list of the indices in row with 2 elements
		###poss2 contains a list of the possibilities in row with 2 elements.
		comb_indices = combinations(indices, 2)
		comb_poss2 = combinations(poss2, 2)
		comb_indices = list(comb_indices)
		comb_poss2 = list(comb_poss2)
		##these are lists of tuples of all the combinations between 2 element pieces
		for c in range(0, len(comb_indices)):
			first = comb_poss2[c][0]
			second = comb_poss2[c][1]
			##print "comb is", first, second
			ret = list_equal(first, second)
			if ret:
				n0 = first[0]
				n1 = first[1]
				#print "removing", n0, n1, "from row poss"
				i0 = comb_indices[c][0]
				i1 = comb_indices[c][1]
				##these are the indices I want to step over.
				for s in range(0, size):
					if s!=i0 and s!=i1:
						if n0 in possibilities[x][s]:
							possibilities[x][s].remove(n0)
							count += 1
						if n1 in possibilities[x][s]:
							possibilities[x][s].remove(n1)
							count += 1
				#print "row poss is", poss_row(x)
				oneoption(board)
				break
	for x in range(0, size):
		col_poss = poss_col(x)
		##print "col poss is", col_poss
		indices = []
		poss2 = []
		for p in range(0, size):
			if len(col_poss[p]) == 2:
				indices.append(p)
				poss2.append(col_poss[p])
		comb_indices = list(combinations(indices, 2))
		comb_poss2 = list(combinations(poss2, 2))
		for c in range(0, len(comb_indices)):
			first = comb_poss2[c][0]
			second = comb_poss2[c][1]
			ret = list_equal(first, second)
			if ret:
				n0 = first[0]
				n1 = first[1]
				#print "removing", n0, n1, "from col poss"
				i0 = comb_indices[c][0]
				i1 = comb_indices[c][1]
				for s in range(0, size):
					if s != i0 and s!=i1:
						if n0 in possibilities[s][x]:
							possibilities[s][x].remove(n0)
							count += 1
						if n1 in possibilities[s][x]:
							possibilities[s][x].remove(n1)
							count += 1
				#print "col poss is", poss_col(x)
				oneoption(board)
				break
	for x in range(0, size):
		box_poss = poss_box(x)
		##print "box poss is", box_poss
		indices = []
		poss2 = []
		for p in range(0, size):
			if len(box_poss[p]) == 2:
				indices.append(p)
				poss2.append(box_poss[p])
		comb_indices = list(combinations(indices, 2))
		comb_poss2 = list(combinations(poss2, 2))
		for c in range(0, len(comb_indices)):
			first = comb_poss2[c][0]
			second = comb_poss2[c][1]
			ret = list_equal(first, second)
			if ret:
				n0 = first[0]
				n1 = first[1]
				#print "box poss before is", poss_box(x)
				i0 = comb_indices[c][0]
				i1 = comb_indices[c][1]
				sqt = int(np.sqrt(size))
				r = x / sqt
				c = x % sqt
				itr = 0
				for s in range(0, sqt):
					for t in range(0, sqt):
						if (itr != i0) and (itr != i1):
							poss = possibilities[sqt*r+s][sqt*c+t]
							if n0 in poss:
								possibilities[sqt*r+s][sqt*c+t].remove(n0)
								count += 1
							if n1 in poss:
								possibilities[sqt*r+s][sqt*c+t].remove(n1)
								count += 1
						itr += 1
				#print "box poss is after:", poss_box(x)
				oneoption(board)
				break
	return count

#===============================================================================

def checkdone(board):
	size = len(board)
	for x in range(0, size):
		line = board[x]
		for y in range(0, size):
			num = line[y]
			if num == 0:
				return 0
	return 1

def isdone(board, ti, slow):
	done = checkdone(board)
	if done:
		print "Solved! Hooray!"
		if slow == False:
			tf = time.time()
			dt = tf-ti
			print "Time to solve:", dt, "sec"
		printboard(board)
		exit()

def do_method(method, board, slow):
	ret = method(board)
	count = ret
	while(ret):
		ret = method(board)
		count += ret
	if slow:
		print count, "changes made with this method."
		printboard(board)
	return count


def num_empty(board):
	num = 0
	l = len(board)
	for r in range(0, l):
		for c in range(0, l):
			pos = board[r][c]
			if pos == 0:
				num += 1
	return num


#==========================B=R=U=T=E===F=O=R=C=E================================

def simple_place(board, row, col, val):
	board[row][col] = val
	return board

def simple_read(board, row, col):
	return board[row][col]


##tries to put a value at a position on the board.
##if the board already has something at that position, returns board.
#else, puts the number on the board. If there is a conflict, returns original board
##if this works, returns the updated board.

def try_val(board, row, col, val):
	open = simple_read(board, row, col)
	if open == 0:
		board_init = np.array(board)
		print "trying", val, "at", row, col
		board = simple_place(board, row, col, val)
		check_row = checkline(selectrow(board, row, col))
		check_col = checkline(selectcol(board, row, col))
		check_box = checkline(selectbox(board, row, col))
		##if any of these is 0 that is bad
		raw_input("pause")
		printboard(board)
		if check_row and check_col and check_box:
			print "This placement was ok. \n\n"
			return 1, board
		else:
			print "This placement was bad. "
			return 0, board_init
	else:
		#print "this spot was not open. "
		return -1, board


#use checkline on selectrow(board, row, col), selectcol, selectbox

def brute_force(board):
	print "tryign to brute force!"
	printboard(board)
	raw_input("do something")
	size = len(board)
	original = board
	history = np.zeros((size, size, 3), dtype=int)
	print "hisoty is", history
	r = 0
	c = 0
	v = 1
	lastr = 0
	lastc = 0
	lastv = 0
	while r < size:
		c = 0
		while c < size:
			v = 1
			while v < (size+1):
				res, board = try_val(board, r, c, v)
				if res == -1:
					break
				if res == 1:
					print "res is 1"
					if history[r][c][2] == 0:
						history[r][c][0] = lastr
						history[r][c][1] = lastc
						history[r][c][2] = lastv
					print "history is", history
					lastr = r
					lastc = c
					lastv = v
				if res == 0 and v == size:
					print "nothing fit!"
					r = lastr
					c = lastc
					v = lastv
					board = simple_place(board, r, c, 0)
					print "going back to row, col, val", r, c, v
					while v == size:
						print "need to continue going bacK"
						print "history is", history
						lr = r
						lc = c
						lv = v
						lastr = history[r][c][0]
						lastc = history[r][c][1]
						lastv = history[r][c][2]
						print "lastr, c, v, is", lastr, lastc, lastv
						r = lastr
						c = lastc
						v = lastv
						print "r, c, v are", r, c, v
						history[lr][lc][0] = 0
						history[lr][lc][1] = 0
						history[lr][lc][2] = 0
						print "updated history is", history
						board = simple_place(board, r, c, 0)
				v += 1
			c += 1
		r += 1
	printboard(board)
	exit()
	if checkdone(board):
		print "yay it is solved!"
	else:
		print "Something went wrong. sorry :("






#===============================================================================
#====================================:)=========================================
#================================S=U=D=O=K=U====================================
#====================================(:=========================================
#===============================================================================


def main():
	print "Welcome to my sudoku solver!!! :)"
	size = 0
	while(1):
		try:
			s = raw_input("Enter the size of the board: ")
			size = int(s)
			if (int(np.sqrt(size)))**2 != size:
				print "The size must be a square."
			elif s == 0:
				print "Board must be larger than 0."
			else:
				break
		except:
			print "Your input should be a single number."
	###creating the board
	#print "This puzzle requires numbers from 1 -", size, "in each row, column, and box."
	board = np.zeros((size, size), dtype=int)
	##entering known values to board
	print "Please enter in the known numbers by row, from left to right,",
	print "separated by spaces (for an empty square, type 0)"
	while(1):
		for x in range(0, size):
			while(1):
				try:
					print "Row", x+1,
					s = raw_input(": ")
					numbers = map(int, s.split())
					if len(numbers) != size:
						print "Input should contain", size, "numbers."
					else:
						numbers = np.array(numbers)
						max = numbers.max()
						min = numbers.min()
						if max>size or min<0:
							print "All numbers in the row must be between 1 and", size, "!"
						else:
							board[x] = numbers
							break
				except:
					print "Unrecognized input."
		printboard(board)
		print "^ ^ ^ Is this the correct board?"
		print "Press 1 to re-input your numbers,",
		mistake = raw_input("or any other key to continue: ")
		try:
			mistake = int(mistake)
			if mistake == 1:
				pass
		except:
			break
	print "Performing preliminary check..."
	sc = sanitycheck(board)
	if sc == 0:
		print("There is an error with the numbers you inputted.")
		exit()
	print "All good!"

	print "The BRUTE FORCE method will try every possible combination of",
	print "numbers until a solution is found."
	print "If you would like to brute force this sudoku, press 1.",
	bf = raw_input("Press anything else to try another method instead: ")
	try:
		bf = int(bf)
		if bf == 1:
			brute_force(board)
	except:
		print "The more elegant (?) technique generates lists of possible numbers",
		print "for each square and through various methods eliminates numbers until",
		print "the solution is found."
		print "Press 1 if you would like descriptions of the methods tried.",
		step = raw_input("Press anything else to go for speed: ")
		slow = False
		try:
			step = int(step)
			if step == 1:
				slow = True
		except:
			pass

		if slow == False:
			print "Going for SPEEEEED!"

		t0 = time.time()

		if slow:
			print "Checking the simple case where a row, column, or box is only missing one number.",
			raw_input("Press any key to continue.")
		c0 = do_method(singlemissing, board, slow)
		isdone(board, t0, slow)

		initialize_possibilities(board, size, slow)

		test = 1
		while(test):

			if slow:
				print "Checking for cases where there is only one possible number",
				print "allowed in a square based on the neighbors in the row, column, and box."
				raw_input("Press any key to continue.")
			c1 = do_method(oneoption, board, slow)
			test = c1
			isdone(board, t0, slow)

			if slow:
				print "Checking for cases where a certain number is only allowed in",
				print "a single square in a row, column, or box.",
				raw_input("Press any key to continue.")
			c2 = do_method(onespot, board, slow)
			test += c2
			isdone(board, t0, slow)

			if slow:
				print "Performing some possibilities manipulations. If the same two numbers are the only",
				print "possibilities in two squares of a row/column/box, they are eliminated as possibilities",
				print "from the other empty squares in the row/column/box.",
				raw_input("Press any key to continue.")
			c3 = do_method(poss_manip, board, slow)
			test += c3
			isdone(board, t0, slow)

		print "Another method needs to be tried to solve this sudoku. Sorry :( "
		printboard(board)

if __name__ == "__main__":
	main()

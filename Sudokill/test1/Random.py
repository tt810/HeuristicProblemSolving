import sys
import random
class Random(object):
	
	def __init__(self, boardInfo):
		self.NUM = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		self.board = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
		self.boardInfo = boardInfo
		self.lastMove = self.boardInfo[-1]
		self.initialNum = len(self.boardInfo) - 1
		for move in self.boardInfo:
			if move[0] != -1:
				self.board[move[1]][move[0]] = move[2]
		self.beginer = False
		if self.boardInfo[-1][0] == -1: self.beginer = True

	def makeMove(self):
		validMoves = []
		bestmove = []
		if self.beginer:
			print "********I am a beginer******"
			children = self.allPossibleNextMoves()
			
		else:
			print "********my opponent player's ", self.lastMove, "**********"
			children = self.possibleNextMoves(self.lastMove[0], self.lastMove[1])
		for child in children:
			self.board[child[1]][child[0]] = child[2]
			if self.invalid(child[0], child[1]) == False:
				validMoves.append(child)
			self.board[child[1]][child[0]] = 0
		print "my valid moves: ", validMoves
		minNextValidMoveNum = -sys.maxint-1
		for move in validMoves:
			print "for my move: ", move
			self.board[move[1]][move[0]] = move[2]
			yourvalidNums = self.predict(move)
			print "	you choose: ", yourvalidNums
			if yourvalidNums == 1: return move
			if minNextValidMoveNum < yourvalidNums:
				minNextValidMoveNum = yourvalidNums
				bestmove = move
			self.board[move[1]][move[0]] = 0
		return bestmove
	
	def predict(self, move):
		yourPretentialMoves = self.possibleNextMoves(move[0], move[1])
		yourvalidMoves = []
		for youmove in yourPretentialMoves:
			self.board[youmove[1]][youmove[0]] = youmove[2]
			if self.invalid(youmove[0], youmove[1]) == False:
				yourvalidMoves.append(youmove)
			self.board[youmove[1]][youmove[0]] = 0 
		print "	your valid moves: ", yourvalidMoves
		if yourvalidMoves == []: return 10000
		maxNextValidMoveNum = sys.maxint
		for validmove in yourvalidMoves:
			self.board[validmove[1]][validmove[0]] = validmove[2]
			myvalidNums = self.predict2(validmove)
			print "	I have: ", myvalidNums
			if maxNextValidMoveNum > myvalidNums:
				maxNextValidMoveNum = myvalidNums
			self.board[validmove[1]][validmove[0]] = 0
		return maxNextValidMoveNum
		
	def predict2(self, move):
		myPretentialMoves = self.possibleNextMoves(move[0], move[1])
		myvalidMoves = []
		for mymove in myPretentialMoves:
			self.board[mymove[1]][mymove[0]] = mymove[2]
			if self.invalid(mymove[0], mymove[1]) == False:
				myvalidMoves.append(mymove)
			self.board[mymove[1]][mymove[0]] = 0
		#print "		my valid moves: ", myvalidMoves
		if myvalidMoves == []: return -10000
		return len(myvalidMoves)
		
	def evaluate(self, state):
		score = 0
		x, y = state[0], state[1]
		nextMoves = self.possibleNextMoves(x, y)
		totalscore = len(nextMoves)
		for nextMove in nextMoves:
			nx, ny = nextMove[0], nextMove[1]
			self.board[ny][nx] = nextMove[2]
			if self.invalid(nx, ny):
				score -= 1
			self.board[ny][nx] = 0
		#print "totalScore: ", totalscore, " score: ", score
		return float(score) / float(totalscore)
	
	def invalid(self, x, y):
		def isViolate(nums):
			nums = sorted(nums)
			if len(nums)>9 or len(nums)<0: return True
			else:
				for i in range(len(nums)-1):
					if nums[i] == nums[i+1]: return True
			return False
		return isViolate(self._xList(y)[0]) or isViolate(self._yList(x)[0]) or isViolate(self._cubeList(x, y))
	
	def possibleNextMoves(self, x, y):
		moves = []
		xnums, unusedXIndex = self._xList(y)
		ynums, unusedYIndex = self._yList(x)
		unusedXs = self._unusedNums(xnums)
		unusedYs = self._unusedNums(ynums)
		if unusedXIndex == [] and unusedYIndex == []:
			return self.allPossibleNextMoves()
		if unusedXIndex != []:
			for uXIndex in unusedXIndex:
				for uXNum in unusedXs:
					moves.append([uXIndex, y, uXNum])
		if unusedYIndex != []:
			for uYIndex in unusedYIndex:
				for uYNum in unusedYs:
					moves.append([x, uYIndex, uYNum])
		return moves
		
	def allPossibleNextMoves(self):
		moves = []
		for y in range(len(self.board)):
			xnums, unusedXIndex = self._xList(y)
			unusedXs = self._unusedNums(xnums)
			if unusedXIndex != []:
				for uXIndex in unusedXIndex:
					for uXNum in unusedXs:
						moves.append([uXIndex, y, uXNum])
		return moves
		
	def _xList(self, y):
		nums = []
		unusedX = []
		for x, num in enumerate(self.board[y]):
			if num != 0: nums.append(num)
			else: unusedX.append(x)
		#print "the row: ", y, "the exsisting Xs: ", nums, "unused x index: ", unusedX
		return (nums, unusedX)
		
	def _unusedNums(self, usedNums):
		nums = sorted(usedNums)
		unused = []
		i = j = 0
		while i < 9:
			if j < len(nums):
				if self.NUM[i] != nums[j]:
					unused.append(self.NUM[i])
					i += 1
				elif self.NUM[i] == nums[j]:
					i += 1
					j += 1
			else:
				unused.append(self.NUM[i])
				i += 1
		#print "unused nums according to the exsists: ", unused
		return unused
		
	def _yList(self, x):
		nums = []
		unusedY = []
		for y in range(len(self.board)):
			if self.board[y][x] != 0: nums.append(self.board[y][x])
			else: unusedY.append(y)
		#print "the col: ", x, "the exsisting Ys: ", nums, "unused y index: ", unusedY
		return (nums, unusedY)
		
	def _cubeList(self, x, y):
		cube = []
		if y <= 2:
			if x <= 2:
				cube += [self.board[r][c] for r in range(3) for c in range(3) if self.board[r][c] != 0]
			elif x > 2 and x <= 5:
				cube += [self.board[r][c] for r in range(3) for c in range(3, 6) if self.board[r][c] != 0]
			else:
				cube += [self.board[r][c] for r in range(3) for c in range(6, 9) if self.board[r][c] != 0]
		elif y > 2 and y <= 5:
			if x <= 2:
				cube += [self.board[r][c] for r in range(3, 6) for c in range(3) if self.board[r][c] != 0]
			elif x > 2 and x <= 5:
				cube += [self.board[r][c] for r in range(3, 6) for c in range(3, 6) if self.board[r][c] != 0]
			else:
				cube += [self.board[r][c] for r in range(3, 6) for c in range(6, 9) if self.board[r][c] != 0]
		else:
			if x <= 2:
				cube += [self.board[r][c] for r in range(6, 9) for c in range(3) if self.board[r][c] != 0]
			elif x > 2 and x <= 5:
				cube += [self.board[r][c] for r in range(6, 9) for c in range(3, 6) if self.board[r][c] != 0]
			else:
				cube += [self.board[r][c] for r in range(6, 9) for c in range(6, 9) if self.board[r][c] != 0]
		#print "cube: ", cube
		return cube

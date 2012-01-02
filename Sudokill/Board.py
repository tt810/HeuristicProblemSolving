import sys

class Board(object):
	
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
		scores = []
		bestMove = []
		best = -sys.maxint-1
		depth = 2
		if self.beginer:
			print "********I am a beginer******"
			children = self.allPossibleNextMoves()
			if self.initialNum <= 80: depth = 1
		else:
			print "********my opponent player's ", self.lastMove, "**********"
			children = self.possibleNextMoves(self.lastMove[0], self.lastMove[1])
			if self.initialNum <= 80: depth = 1
		if len(children) == 1: return children[0]
		print "my possible moves: ", children
		for child in children:
			self.board[child[1]][child[0]] = child[2]
			if self.invalid(child[0], child[1]): result = -2
			else: result = self.miniMove(child, depth-1)
			print "if I choice ", child, ", I will get a score ", result
			scores.append(result)
			if result > best:
				best = result
				bestMove = child
			self.board[child[1]][child[0]] = 0
		print "my score choices are: ", scores
		print "so I best choice is ", bestMove, "score: ", best
		return bestMove
	
	def maxiMove(self, node, depth):
		print "		depth: ", depth, "	your move: ", node
		x, y = node[0], node[1]
		children = self.possibleNextMoves(x, y)
		maxs = []
		if len(children) == 0: maxs.append(0)
		if depth == 0:
			for child in children:
				if self.invalid(child[0], child[1]): maxs.append(-2)
				else:
					maxs.append(-self.evaluate(child))
		else:
			for child in children:
				if self.invalid(child[0], child[1]): maxs.append(-2)
				else:
					self.board[child[1]][child[0]] = child[2]
					maxs.append(self.miniMove(child, depth-1))
					self.board[child[1]][child[0]] = 0
		print "chooce max for me from List: ", maxs
		return max(maxs)
	
	def miniMove(self, node, depth):
		print "			depth: ", depth, "		 my move: ", node
		x, y = node[0], node[1]
		children = self.possibleNextMoves(x, y)
		mins = []
		if len(children) == 0: mins.append(0)
		if depth == 0:
			for child in children:
				if self.invalid(child[0], child[1]): mins.append(2)
				else:
					mins.append(self.evaluate(child))
		else:
			for child in children:
				if self.invalid(child[0], child[1]): mins.append(2)
				else:
					self.board[child[1]][child[0]] = child[2]
					mins.append(self.maxiMove(child, depth-1))
					self.board[child[1]][child[0]] = 0
		print "choose min for you from List: ", mins
		return min(mins)
	
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

import sys

class Board(object):
	"""
	[[2, 5, 7], [4, 4, 2], [0, 4, 4], [-1, -1, -1]]
	"""
	def __init__(self, boardInfo):
		self.NUM = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		self.board = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
		self.boardInfo = boardInfo
		self.lastMove = self.boardInfo[-1]
		for move in self.boardInfo[:-1]:
			if move[0] != -1:
				self.board[move[1]][move[0]] = move[2]
		self.beginer = False
		if self.boardInfo[-1][0] == -1: self.beginer = True
		
	def makeMove(self):
		if self.lastMove == [-1, -1, -1]:
			#beginer
		else:
			#make move according to the last move
			#if remain slots != empty:
				#make move regularly
			#else:
				#make move as beginer
		
	def allPossibleNextMoves(self):
		moves = []
		for y in range(len(self.board)):
			usedXs = []
			slots = []
			for x in range(len(self.board[y])):
				if self.board[y][x] == 0: 
					slots.append([x, y])
				else: usedXs.append(self.board[y][x])
				
		
	def myStep(self, move, depth):
		if depth == 0: 
			(totalScore, score) = self.evaluate(move)
			return float(score) / float(totalScore)
		x, y = move[0], move[1]
		self.board[y][x] = move[2]
		maxs = []
		for nextMove in self.possibleNextMoves(x, y):
			maxs.append(yourStep(nextMove, depth-1))
		self.board[y][x] = 0
		return max(maxs)
		
	def yourStep(self, move, depth):
		if depth == 0:
			(totalScore, score) = self.evaluate(move)
			return float(score) / float(totalScore)
		x, y = move[0], move[1]
		self.board[y][x] = move[2]
		mins = []
		for nextMove in self.possibleNextMoves(x, y):
			mins.append(myStep(nextMove, depth-1)
		self.board[y][x] = 0
		return min(mins)
		
	def evaluate(self, move):
		"""
		if this move can make the other player violate the rule, get score
		evaluate each slot with every possible number
		"""
		score = 0
		x, y = move[0], move[1]
		self.board[y][x] = move[2]
		nextMoves = self.possibleNextMoves(x,y)
		totalScore = len(nextMoves)
		for nextmove in nextMoves:
			nx, ny = nextmove[0], nextmove[1]
			self.board[ny][nx] = nextmove[2]
			if self.violate(nx, ny): 
				print "this move violate: ", nextmove
				score += 1
			self.board[ny][nx] = 0
		self.board[y][x] = 0
		print "totalScore: ", totalScore, " score: ", score
		return (totalScore, score)
	
	def possibleNextMoves(self, x, y):
		moves = []
		xnums, unusedX = self._xList(y)
		ynums, unusedY = self._yList(x)
		unusedXs = self.unusedNums(xnums)
		unusedYs = self.unusedNums(ynums)
		print "unused X nums: ", unusedXs
		print "unused Y nums: ", unusedYs
		for uX in unusedX:
			for uXNum in unusedXs:
				moves.append([uX, y, uXNum])
		for uY in unusedY:
			for uYNum in unusedYs:
				moves.append([x, uY, uYNum])
		print "possible next moves: ", moves
		if moves == []:
			#getherSlots()
		return moves
	
	def violate(self, x, y):
		def isViolate(nums):
			nums = sorted(nums)
			if len(nums)>9 or len(nums)<0: return True
			else:
				for i in range(len(nums)-1):
					if nums[i] == nums[i+1]: return True
			return False
		return isViolate(self._xList(y)[0]) or isViolate(self._yList(x)[0]) or isViolate(self._cubeList(x, y))
	
	def unusedNums(self, nums):
		nums = sorted(nums)
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
		return unused
	
	def _xList(self, y):
		nums = []
		unusedX = []
		for x, num in enumerate(self.board[y]):
			if num != 0: nums.append(num)
			else: unusedX.append(x)
		print "the same row: ", nums, "unused x: ", unusedX
		return (nums, unusedX)
		
	def _yList(self, x):
		nums = []
		unusedY = []
		for y in range(len(self.board)):
			if self.board[y][x] != 0: nums.append(self.board[y][x])
			else: unusedY.append(y)
		print "the same col: ", nums, "unused y: ", unusedY
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
		print "cube: ", cube
		return cube

"""
"""
import sys

class Board(object):
	"""
	"""
	def __init__(self):
		self.NUM = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		self.board = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
	
	def fillCell(self, row, col, num):
		self.board[row][col] = num
	def removeCell(self, row, col):
		self.board[row][col] = 0
	"""
	def minimax(self, row, col, num, depth):
		self.fillCell(row, col, num)
		if depth == 0: 
			score = self.evaluate(row, col)
			print "depth: ", depth, " score: ", score, "possible: ", [row, col, num]
			return score
		alpha = -sys.maxint - 1
		for kid in self.possibleKids(row, col):
			score = -self.minimax(kid[0], kid[1], kid[2], depth-1)
			alpha = max(alpha, score)
			print "alpha: ", score, " depth: ", depth, " possible: ", kid
		self.removeCell(row, col)
		return alpha
	"""
	def minimax(self, row, col, num, depth):
		self.fillCell(row, col, num)
		if depth == 0: 
			score = [row, col, num, self.evaluate(row, col)]
			print score
			return score
		alpha = [-1, -1, 0, -sys.maxint - 1]
		for kid in self.possibleKids(row, col):
			print kid
			score = -self.minimax(kid[0], kid[1], kid[2], depth-1)
			if alpha[3] < score:
				alpha[3] = score
				alpha[0], alpha[1], alpha[2] = kid[0], kid[1], kid[2]
		self.removeCell(row, col)
		return alpha
	
	def getNode(self, lastRow, lastCol, num, depth):
		result = self.minimax(lastRow, lastCol, num, depth)
		self.fillCell(lastRow, lastCol, num)
		return [result[0], result[1], result[2]]
	"""			
	def getNode(self, lastRow, lastCol, depth):
		print lastRow, " lastCol: ", lastCol
		me = self.possibleKids(lastRow, lastCol)
		maxi = -sys.maxint - 1
		row = -1
		col = -1
		num = 0
		for possiblem in me:
			alpha = self.minimax(possiblem[0], possiblem[1], possiblem[2], depth)
			print "possible: ", possiblem, " value: ", alpha
			if maxi < alpha:
				row = possiblem[0]
				col = possiblem[1]
				num = possiblem[2]
				maxi = alpha
		return [row, col, num]
	"""	
	def frontierValue(self, row, col, num):
		self.fillCell(row, col, num)
		value = 0
		if self.violate(row, col): value = -1		
		self.removeCell(row, col)
		return value
	
	def evaluate(self, row, col):
		score = 0
		for kid in self.lastStep(row, col):
			#print kid, " score: ", score
			score += self.frontierValue(kid[0], kid[1], kid[2])
		return -score
		
	def possibleKids(self, row, col):
		kids = self.lastStep(row, col)
		passedKids = [kid for kid in kids if self._sudoViolate(kid[0], kid[1], kid[2]) == False]	
		return passedKids	
		
	def lastStep(self, row, col):
		kids = []
		R = self.unFillRow(row)
		C = self.unFillCol(col)
		colIndex, rows = R[0], R[1]
		rowIndex, cols = C[0], C[1]
		if colIndex != 0 or rowIndex != 0:
			if colIndex != 0:
				rowKids = [[row, colI, num] for colI in colIndex for num in rows]
				kids += rowKids
			if rowIndex != 0:
				colKids = [[rowI, col, num] for rowI in rowIndex for num in cols]
				kids += colKids
		else:
			for r in range(len(self.board)):
				allR = self.unFillRow(r)
				cIndex, rNums = allR[0], allR[1]
				if cIndex != 0:
					rowKids = [[r, cI, num] for cI in cIndex for num in rNums]
					kids += rowKids
		return kids						
		
	def unFillRow(self, row):
		index = [i for i in range(len(self.board[row])) if self.board[row][i] == 0]
		usedNums = [num for num in self.board[row] if num != 0]
		unUsedNums = self._getUnused(usedNums)
		return [index, unUsedNums]
	
	def unFillCol(self, col):
		index = [j for j in range(len(self.board)) if self.board[j][col] == 0]
		usedNums = [self.board[j][col] for j in range(len(self.board)) if self.board[j][col] != 0]
		unUsedNums = self._getUnused(usedNums)
		return [index, unUsedNums]
	
	def _getUnused(self, nums):
		nums = sorted(nums)
		unUsed = []
		i=j=0
		while i < 9:
			if j < len(nums):
				if self.NUM[i] != nums[j]: 
					unUsed.append(self.NUM[i])
					i += 1
				elif self.NUM[i] == nums[j]:
					i += 1
					j += 1
			else:
				unUsed.append(self.NUM[i])
				i += 1
		return unUsed
	def _sudoViolate(self, row, col, num):
		self.fillCell(row, col, num)
		violate = self.violate(row, col)
		self.removeCell(row, col)
		return violate
		
	def violate(self, row, col):
		nums = [num for num in self.board[row] if num != 0]
		if self._isViolate(nums) == True: return True
		nums = [self.board[r][col] for r in range(len(self.board)) if self.board[r][col] != 0]
		if self._isViolate(nums) == True: return True
		return self._isViolate(self._cube(row, col))
	
	def _cube(self, row, col):
		cube = []
		if row <= 2:
			if col <= 2:
				for r in range(3):
					for c in range(3):
						if self.board[r][c] != 0:
							cube.append(self.board[r][c])
			elif col >2 and col <= 5:
				for r in range(3):
					for c in range(3, 6):
						if self.board[r][c] != 0:
							cube.append(self.board[r][c])
			else:
				for r in range(3):
					for c in range(6, 9):
						if self.board[r][c] != 0:
							cube.append(self.board[r][c])
		elif row > 2 and row <= 5:
			if col <= 2:
				for r in range(3, 5):
					for c in range(3):
						if self.board[r][c] != 0:
							cube.append(self.board[r][c])
			elif col >2 and col <= 5:
				for r in range(3, 5):
					for c in range(3, 6):
						if self.board[r][c] != 0:
							cube.append(self.board[r][c])
			else:
				for r in range(3, 5):
					for c in range(6, 9):
						if self.board[r][c] != 0:
							cube.append(self.board[r][c])
		else:
			if col <= 2:
				for r in range(6, 9):
					for c in range(3):
						if self.board[r][c] != 0:
							cube.append(self.board[r][c])
			elif col >2 and col <= 5:
				for r in range(6, 9):
					for c in range(3, 6):
						if self.board[r][c] != 0:
							cube.append(self.board[r][c])
			else:
				for r in range(6, 9):
					for c in range(6, 9):
						if self.board[r][c] != 0:
							cube.append(self.board[r][c])
		return cube
	
	def _isViolate(self, nums):
		nums = sorted(nums)
		if len(nums)>9 or len(nums)<0: return True
		else:
			for i in range(len(nums)-1):
				if nums[i] == nums[i+1]: return True
		return False


import random
import re
import fileinput
import sys
moves_made = []
dictionary_of_moves_mode = {}

class Player21(object):

		def __init__(self):
			self.symbol = ''
			self.threeXthree = [ '-' for x in range(9)]
			self.checkHowManyLines = 5500
			self.maxReached = [False,False,False,False]
			self.fileNo = 0
			self.count = 0

		def nextMove(self, current_node, move_by_opponent, current_status, level):
			this_is_a_board = current_node.checksumToBoard()
			flag = 0
			max_value = 0
			max_node = [-1,-1,0,0]
			min_node = [1,1,0,0]
			min_value = 1
			if(move_by_opponent[0] == move_by_opponent[1] == -1):
				this_is_a_board[4][4] = self.symbol
				current_node.boardToChecksum(this_is_a_board)
				this_is_a_board[4][4] = '-'
				return [4,4,current_node.board, self.checkFileForChecksum(current_node.board)]
			if((move_by_opponent[1]%3 + move_by_opponent[0]%3)%2 ==1 or move_by_opponent[0]%3 == move_by_opponent[1]%3 == 1 ):
				offset_i = 0
				offset_j = 0
				if(move_by_opponent[1]%3 == 1 and move_by_opponent[0]%3 == 0):
					offset_i = 0
					offset_j = 3
				if(move_by_opponent[1]%3 == 0 and move_by_opponent[0]%3 == 1):
					offset_i = 3
					offset_j = 0
				if(move_by_opponent[1]%3 == 2 and move_by_opponent[0]%3 == 1):
					offset_i = 3
					offset_j = 6
				if(move_by_opponent[1]%3 == 1 and move_by_opponent[0]%3 == 1):
					offset_i = 3
					offset_j = 3
				if(move_by_opponent[1]%3 == 1 and move_by_opponent[0]%3 == 2):
					offset_i = 6
					offset_j = 3
				for i in xrange(0,3):
					for j in xrange(0,3):
						if(this_is_a_board[offset_i + i][offset_j + j] == '-' and current_status[offset_i + offset_j/3] == '-'):
							temp_node = Node(-1,-1,-1,-1)
							this_is_a_board[offset_i + i][offset_j + j] = self.symbol
							temp_node.board = temp_node.boardToChecksum(this_is_a_board)
							temp_node.setParent(current_node)
							current_node.setChild(temp_node)
							this_is_a_board[offset_i + i][offset_j + j] = '-'
							flag = 1
							return_value = self.checkFileForChecksum(temp_node.board)
							if(level == 0):
								BestMove = self.setupBoard(this_is_a_board,offset_i + i,offset_j + j)
								if BestMove[0] == True:
									temp_node.hn = BestMove[1]
								else:
									MODIFIED_CURRENT_STATUS = current_status[:]
									if(self.symbol == 'o'):
										self.symbol = 'x'
									else:
										self.symbol = 'o'
									self.checkWin(temp_node.checksumToBoard(),MODIFIED_CURRENT_STATUS,offset_i + i,offset_j + j)
									if(self.symbol == 'x'):
										self.symbol = 'o'
									else:
										self.symbol = 'x'
									k = self.nextMove(temp_node,(offset_i + i, offset_j + j),MODIFIED_CURRENT_STATUS,1)
									count = 0
									for x in xrange(0,9):
										if(MODIFIED_CURRENT_STATUS[x] != '-'):
											count  += 1
									if(count == 9):
										temp_node.hn = 1
									else:
										temp_node.hn = k[3]

								if( temp_node.hn > max_value):
									max_value = temp_node.hn
									max_node = [offset_i + i, offset_j + j, temp_node.board,max_value]
							if(level == 1):
								temp_node.hn = return_value
								BestMove = self.setupBoard(this_is_a_board,offset_i + i, offset_j + j)
								if BestMove[0] == True:
									temp_node.hn = BestMove[1]
								if(temp_node.hn < min_value):
									min_value = temp_node.hn
									min_node = [offset_i + i, offset_j + j, temp_node.board,min_value]
			#Check if move made was corner
			if((move_by_opponent[1]%3 + move_by_opponent[0]%3)%2 ==0 and move_by_opponent[1] == move_by_opponent[1] != 1 ):
				offset_i = 0
				offset_j = 0
				offset_i_array = []
				offset_j_array = []
				if(move_by_opponent[1]%3 == 0 and move_by_opponent[0]%3 == 0):
					offset_i_array = [0,0,3]
					offset_j_array = [0,3,0]
				if(move_by_opponent[1]%3 == 0 and move_by_opponent[0]%3 == 2):
					offset_i_array = [3,6,6]
					offset_j_array = [0,0,3]
				if(move_by_opponent[1]%3 == 2 and move_by_opponent[0]%3 == 0):
					offset_i_array = [0,0,3]
					offset_j_array = [3,6,6]
				if(move_by_opponent[1]%3 == 2 and move_by_opponent[0]%3 == 2):
					offset_i_array = [6,6,3]
					offset_j_array = [3,6,6]
				for i in xrange(0,3):
					for j in xrange(0,3):
						for offset_i,offset_j in zip(offset_i_array,offset_j_array):
							if(this_is_a_board[offset_i + i][offset_j + j] == '-'  and current_status[offset_i + offset_j/3] == '-'):
								temp_node = Node(-1,-1,-1,-1)
								this_is_a_board[offset_i + i][offset_j + j] = self.symbol
								temp_node.board = temp_node.boardToChecksum(this_is_a_board)
								temp_node.setParent(current_node)
								current_node.setChild(temp_node)
								this_is_a_board[offset_i + i][offset_j + j] = '-'
								flag = 1
								return_value = self.checkFileForChecksum(temp_node.board)
								if(level == 0):
									BestMove = self.setupBoard(this_is_a_board,offset_i + i,offset_j + j)
									if BestMove[0] == True:
										temp_node.hn = BestMove[1]
									else:
										MODIFIED_CURRENT_STATUS = current_status[:]
										if(self.symbol == 'o'):
											self.symbol = 'x'
										else:
											self.symbol = 'o'
										self.checkWin(temp_node.checksumToBoard(),MODIFIED_CURRENT_STATUS,offset_i + i,offset_j + j)
										if(self.symbol == 'x'):
											self.symbol = 'o'
										else:
											self.symbol = 'x'
										k = self.nextMove(temp_node,(offset_i + i, offset_j + j),MODIFIED_CURRENT_STATUS,1)
										count = 0
										for x in xrange(0,9):
											if(MODIFIED_CURRENT_STATUS[x] != '-'):
												count  += 1
										if(count == 9):
											temp_node.hn = 1
										else:
											temp_node.hn = k[3]

									if(temp_node.hn > max_value):
										max_value = temp_node.hn
										max_node = [offset_i + i, offset_j + j, temp_node.board,max_value]
								if(level == 1):
									temp_node.hn = return_value
									temp_node.hn = return_value
									BestMove = self.setupBoard(this_is_a_board,offset_i + i, offset_j + j)
									if BestMove[0] == True:
										temp_node.hn = BestMove[1]
									if( temp_node.hn < min_value):
										min_value = temp_node.hn
										min_node = [offset_i + i, offset_j + j, temp_node.board, min_value]
										if min_node[3] < 0.3:
											return min_node
			# If no square is empty in a selection
			if(flag == 0):
				for i in xrange(0,9):
					for j in xrange(0,9):
						if(this_is_a_board[i][j] == '-'  and (current_status[int(i/3)*3 + j/3] == '-' or current_status[int(i/3)*3 + j/3] == '*')):
							temp_node = Node(-1,-1,-1,-1)
							this_is_a_board[ i][ j] = self.symbol
							temp_node.board = temp_node.boardToChecksum(this_is_a_board)
							temp_node.setParent(current_node)
							current_node.setChild(temp_node)
							this_is_a_board[ i][ j] = '-'
							return_value = self.checkFileForChecksum(temp_node.board)
							if(level == 0):
								MODIFIED_CURRENT_STATUS = current_status[:]
								BestMove = self.setupBoard(this_is_a_board,i,j)
								if BestMove[0] == True:
									temp_node.hn = BestMove[1]
								else:
									if(self.symbol == 'x'):
										self.symbol = 'o'
									else:
										self.symbol = 'x'
									self.checkWin(temp_node.checksumToBoard(),MODIFIED_CURRENT_STATUS,i,j)
									if(self.symbol == 'x'):
										self.symbol = 'o'
									else:
										self.symbol = 'x'
									k = self.nextMove(temp_node,(i, j),MODIFIED_CURRENT_STATUS,1)
									count = 0
									for x in xrange(0,9):
										if(MODIFIED_CURRENT_STATUS[x] != '-'):
											count  += 1
									if(count == 9):
										temp_node.hn = 1
									else:
										temp_node.hn = k[3]

								if(temp_node.hn > max_value):
									max_value = temp_node.hn
									max_node = [i, j, temp_node.board,max_value]
									if max_node[3] > 0.2:
										return max_node
							if(level == 1):
								temp_node.hn = return_value
								BestMove = self.setupBoard(this_is_a_board,i,j)
								if BestMove[0] == True:
									temp_node.hn = BestMove[1]
								if( return_value < min_value):
									min_value = return_value
									min_node = [i,j, temp_node.board,min_value]
									if min_node[3] < 0.5:
										return min_node
							flag = 1
			if(max_node[0] != -1):
				return max_node
			elif(min_node[2] != 0):
				return min_node
			return [-1,-1,0,0]

		def move(self, current_board_game, board_stat, move_by_opponent, flag):
			## Duplicating the variables as to not modify the lists
			self.symbol = flag
			duplicate_current_board_game = current_board_game[:]
			current_status = board_stat[:]
			## Finding the next move
			temp_node = Node(-1,-1,-1,-1)
			temp_node.boardToChecksum(duplicate_current_board_game)
			return_value_of_nextMove = self.nextMove(temp_node,move_by_opponent, current_status,0)
			self.count += 2
			return_value_of_nextMove.append(self.count)
			moves_made.append(return_value_of_nextMove)
			
			## check if move leads to a win/lose and update file accordingly
			## Comment out these lines when training
			score = self.checkWin(duplicate_current_board_game,current_status,return_value_of_nextMove[0],return_value_of_nextMove[1])
			scaled_score = self.scale(score)
			if(score != -1):
				self.updateFile(scaled_score)
			return (return_value_of_nextMove[0],return_value_of_nextMove[1])

		def checksumToString(self,checksum):
			s = "["
			for i in xrange(0,9):
				s += str(checksum[i]) + ", "
			s = s[:-2]
			s += "]"
			return s

		def scale(self, score):
			if(score == 4):
				return 1
			if(score == 2):
				return 0.7
			if(score == 1):
				return 0.4
			if(score == 0):
				return -0.1

		def checkFileForChecksum(self, checksum):
			## chosing which file to check from
			if self.count <= 20:
				fileString = "ProbDis1"
				self.fileNo = 0
			elif self.count > 20 and self.count <=30:
				fileString = "ProbDis21"
				self.fileNo = 1
			elif self.count > 30 and self.count <=40:
				fileString = "ProbDis22"
				self.fileNo = 2
			else:
				fileString = "ProbDis3"
				self.fileNo = 3

			checksum_in_string = self.checksumToString(checksum)
			temp = open(fileString, "r")
			i = 0
			for line in temp:
				half_line = re.split('#',line)
				if(half_line[0] == checksum_in_string):
					dictionary_of_moves_mode[checksum_in_string] = (line,float(half_line[1]),float(half_line[2]), self.count)
					num = float(half_line[2])
					denom = float(half_line[1])
					if(denom !=0):
						return num/denom
					else:
						return 0
				i += 1
				if i == self.checkHowManyLines:
					self.maxReached[self.fileNo] = True
					break
			return random.random()

		def updateFile(self, amount):
			for checksum in moves_made:
				checksum_in_string = self.checksumToString(checksum[2])
				if checksum[4] <= 20:
					self.fileNo = 1
					fileString = "ProbDis1"
				elif checksum[4] > 20 and checksum[4] <=30:
					fileString = "ProbDis21"
					self.fileNo = 1
				elif checksum[4] > 30 and checksum[4] <=40:
					fileString = "ProbDis22"
					self.fileNo = 2
				else:
					fileString = "ProbDis3"
					self.fileNo = 3

				if checksum_in_string in dictionary_of_moves_mode.keys():
					current_checksum = dictionary_of_moves_mode[checksum_in_string]
					j = 0
					for  line in fileinput.FileInput(fileString, inplace=1):
						if j == self.checkHowManyLines:
							break
						sys.stdout.write(line.replace(current_checksum[0],checksum_in_string + '#' + str(current_checksum[1] + 1) + "#" + str(current_checksum[2] + amount) + "\n") )
						j += 1
				else:
					if self.maxReached[self.fileNo] == False:
						with open(fileString, "a") as myfile:
						    myfile.write(checksum_in_string+"#"+str(1)+"#"+str(amount)+"\n")
					
		def check9x9(self,board):
			me = 0
			#Diagnols
			if (board[0][0] == 'x' and board[1][1] == 'x' and board[2][2] == 'x') or (board[0][2] == 'x' and board[1][1] == 'x' and board[2][0] == 'x'):
				#print 'X WON'
				if(self.symbol == 'x'):
					return ('x',2)
				else:
					return ('o',0)

			if (board[0][0] == 'o' and board[1][1] == 'o' and board[2][2] == 'o') or (board[0][2] == 'o' and board[1][1] == 'o' and board[2][0] == 'o'):
				#print 'O WON'
				if(self.symbol == 'o'):
					return ('o',2)
				else:
				    return ('x',0)


			#Rows
			for i in range(0,3):
				if(i%3 == 0):
					for j in range(0,3):
						if (board[i][j] == 'x' and board[i+1][j] == 'x' and board[i+2][j] == 'x'):
							#print 'x win'
							if(self.symbol == 'x'):
								return ('x',1)
							else:
								return ('o',0)
		
						if (board[i][j] == 'o' and board[i+1][j] == 'o' and board[i+2][j] == 'o'):
							#print 'o win'
							if(self.symbol == 'o'):
								return ('o',1)
							else:
								return ('x',0)

			#Colomns
			for i in range(0,3):
				if (board[i][0] == 'x' and board[i][1] == 'x' and board[i][2] == 'x'):
					#print 'x wins'
					if(self.symbol == 'x'):
						return ('x',1)
					else:
						return ('o',0)

				if (board[i][0] == 'o' and board[i][1] == 'o' and board[i][2] == 'o'):
					#print 'o wins'
					if(self.symbol == 'x'):
						return ('o',1)
					else:
						return ('x',0)

			return ('.',-1)

		def checkWin(self,duplicate_current_board_game, current_status , next_i, next_j):
			root1 = Node(-1,-1,-1,-1)
			root = Node(-1,-1,-1,-1)
			new_board_game = duplicate_current_board_game[:]
			new_board_game[next_i][next_j]  = self.symbol
			listt = root.boardToChecksum(new_board_game)
			new_board_game[next_i][next_j]  = '-'
			k =  root.checksumToBoard()
			board = []
			#Finding the index where the new move is being made
			block_i = 0
			if(next_i > 5):
				block_i = 2
			if(next_i < 6 and next_i > 2):
				block_i = 1
			if(next_i < 3):
				block_i = 0
			block_j = 0
			if(next_j > 5):
				block_j = 2
			if(next_j < 6 and next_j > 2):
				block_j = 1
			if(next_j < 3):
				block_j = 0
			iterr = block_i*3 + block_j;
			#If the new move can cause a new win to be possible
			if(current_status[iterr] == '-'):
				#get the value of the checksum for this subboard
				x = listt[iterr]
				#convert it to a board
				board =  self.giveBoardvals(x)
				#check the board for a win/lose
				ret = self.checkSubboard(board)
				#edit the list 
				current_status[iterr] = ret[0]
			for i in range(0,9):
				if(current_status[i] == '-'):
					x = listt[i]
					board =  self.giveBoardvals(x)
					ret = self.findDraws(board)
					current_status[i] = ret[0]
			return self.check3x3(current_status)

		def finddraw(self,board):
			#Diagnols
			if (board[0] == 'x' and board[4] == 'x' and board[8] == 'x') or (board[6] == 'x' and board[4] == 'x' and board[2] == 'x'):
				if(self.symbol == 'x'):
					return ('x',4)
				else:
					return ('x',1)
			if (board[0] == 'o' and board[4] == 'o' and board[8] == 'o') or (board[6] == 'o' and board[4] == 'o' and board[2] == 'o'):
				if(self.symbol == 'o'):
					return ('o',4)
				else:
					return ('o',1)

			return ('-',-1)

		def check3x3(self, board):
			""" Check for a win"""
			value = self.finddraw(board)
			if(value[1] != -1):
				return value[1]
			#Rows
			for i in range(0,9):
				if(i%3 == 0):
					if (board[i] == 'x' and board[i+1] == 'x' and board[i+2] == 'x'):
						if(self.symbol == 'x'):
							return 4
						else:
							return 0
	
					if (board[i] == 'o' and board[i+1] == 'o' and board[i+2] == 'o'):
						if(self.symbol == 'o'):
							return 4
						else:
							return 0

			#Colomns
			for i in range(0,3):
				if(i/3 == 0):
					if (board[i] == 'x' and board[i+3] == 'x' and board[i+6] == 'x'):
						if(self.symbol == 'x'):
							return 4
						else:
							return 0
	
					if (board[i] == 'o' and board[i+3] == 'o' and board[i+6] == 'o'):
						if(self.symbol == 'o'):
							return 4
						else:
							return 0

			count = 0
			savei = 0
			value = -1
			for i in range(0,9):
					if(board[i] != '-'):
						count += 1
					else:
						savei = i

			if(count == 9):
				return 1
			if(count == 8):
				if(self.symbol == 'x'):
					board[savei] = 'o'
					value = self.finddraw(board)
				if(self.symbol == 'o'):
					board[savei] = 'x'
					value = self.finddraw(board)
				if(value[1] > -1):
					if(value[1] == 1):
						return 1
					if(value[1] == 4):
						return 2

			return -1

		def findDiagonal(self,board):
			#Diagnols
			if (board[0][0] == 'x' and board[1][1] == 'x' and board[2][2] == 'x') or (board[0][2] == 'x' and board[1][1] == 'x' and board[2][0] == 'x'):
				if(self.symbol == 'x'):
					return ('x',4)
				else:
					return ('x',0)

			if (board[0][0] == 'o' and board[1][1] == 'o' and board[2][2] == 'o') or (board[0][2] == 'o' and board[1][1] == 'o' and board[2][0] == 'o'):
				if(self.symbol == 'o'):
					return ('o',4)
				else:
				    return ('o',0)

			return ('-',-1)
				
		def findDraws(self,board):
					#finding draws
					counto = 0
					countx = 0
					savei = 0
					savej = 0
					cornerx = 0
					cornero = 0

					for i in range(0,3):
						for j in range(0,3):
							if(board[i][j] != '-'):
								if(board[i][j] == 'x'):
									countx += 1
								else:
									counto += 1
							else:
								savej =  j
								savei = i

					if(countx + counto == 9):
						#comes in here, means there is a draw
						if(countx>counto):
							if(self.symbol == 'x'):
								return ('*', 2)
							else:
								return ('*', 1)
						if(countx == counto):
					            point1 = 0
						    point2 = 0
						    for i in range(len(board)):
							for j in range(len(board[i])):
							    if i%3!=1 and j%3!=1:
							        if game_board[i][j] == 'x':
							            point1+=1
							        elif game_board[i][j]=='o':
							            point2+=1
								    if point1>point2:
								        if(self.symbol == 'x'):
										return ('*', 2)
									else:
										return ('*', 1)
								    elif point2>point1:
									if(self.symbol == 'x'):
										return ('*', 2)
									else:
										return ('*', 1)
					    	    		    else:
									return ('*', 2)

						return ('-',0)

					if(countx + counto == 8):
						board[savei][savej] = 'o'
						value1 =self.findDiagonal(board)

						board[savei][savej] = 'x'
						value2 =self.findDiagonal(board)

						if(value1 > -1):
							if(self.symbol == value1[0]):
								return ('*',2)
							else:
								return ('*',1)
						if(value2 > -1):
							if(self.symbol == value2[0]):
								return ('*',2)
							else:
								return ('*',1)
					return ('-',-1)

		def checkSubboard(self,board):
			value =  self.findDiagonal(board)
			if(value[0] != '-'):
				return value

			#Rows
			for i in range(0,3):
				if(i%3 == 0):
					for j in range(0,3):
						if (board[i][j] == 'x' and board[i+1][j] == 'x' and board[i+2][j] == 'x'):
							if(self.symbol == 'x'):
								return ('x',4)
							else:
								return ('x',0)
		
						if (board[i][j] == 'o' and board[i+1][j] == 'o' and board[i+2][j] == 'o'):
							if(self.symbol == 'o'):
								return ('o',4)
							else:
								return ('o',0)

			#Colomns
			for i in range(0,3):
				if (board[i][0] == 'x' and board[i][1] == 'x' and board[i][2] == 'x'):
					if(self.symbol == 'x'):
						return ('x',4)
					else:
						return ('x',0)

				if (board[i][0] == 'o' and board[i][1] == 'o' and board[i][2] == 'o'):
					if(self.symbol == 'x'):
						return ('o',4)
					else:
						return ('o',0)

			return self.findDraws(board)

			return ('-',-1)
			
		def giveBoardvals(self,board):
			real_board = [[ '.' for x in range(3)] for x in range(3)] 
			xstart = 0
			xend = 3
			ystart = 0
			yend = 3
			for iterator in range(0,3):
				value = board
				value = bin(value)[2:]
				for pad in range(0,32 -len(value)):
					value = '0' + value
				it = 5  # padding of extra 5 bits (32 -27)

				for i in range(0,3):
					for j in range(0,3):
						temp = value[it]
						temp += value[it+1] 
						temp += value[it+2]
						it += 3
						var = int(temp,2)

						if( var == 0 ):
							real_board[i][j] =  '-'

						if( var == 1 ):
							real_board[i][j] =  'o'
								
						if( var == 2 ):
							real_board[i][j] =  'x'
			return real_board
					
		def setupBoard(self,board,movei,movej):
			offset_i = int(movei/3)*3
			offset_j = int(movej/3)*3
			new_board = [['-','-','-'] for i in xrange(0,3) ]
			for i in xrange(0,3):
				for j in xrange(0,3):
					new_board[i][j] = board[offset_i + i][offset_j + j]
			possibleMoves = self.biasBoard(new_board)
			if (movei%3,movej%3) in possibleMoves:
				return (True,1)
			elif movei%3 == movej%3 == 1:
				return (True, 0.4)
			else:
				return (False,0)

		def biasBoard(self,board):
			possibleMoves = []
			# Row 1,2,3  X X -
			if board[0][0] == board[0][1] != '-' and board[0][2] == '-':
				possibleMoves.append((0,2))
			if board[1][0] == board[1][1] != '-' and board[1][2] == '-':
				possibleMoves.append((1,2))
			if board[2][0] == board[2][1] != '-' and board[2][2] == '-':
				possibleMoves.append((2,2))

			#Row 1,2,3 X - X
			if board[0][0] == board[0][2] != '-' and board[0][1] == '-':
				possibleMoves.append((0,1))
			if board[1][0] == board[1][2] != '-' and board[1][1] == '-':
				possibleMoves.append((1,1))
			if board[2][0] == board[2][2] != '-' and board[2][1] == '-':
				possibleMoves.append((2,1))

			#Row 1,2,3 - X X
			if board[0][1] == board[0][2] != '-' and board[0][0] == '-':
				possibleMoves.append((0,0))
			if board[1][1] == board[1][2] != '-' and board[1][0] == '-':
				possibleMoves.append((1,0))
			if board[2][1] == board[2][2] != '-' and board[2][0] == '-':
				possibleMoves.append((2,0))

			#Col 1,2,3 X X -
			if board[0][0] == board[1][0] != '-' and board[0][2] == '-':
				possibleMoves.append((0,2))
			if board[0][1] == board[1][1] != '-' and board[2][1] == '-':
				possibleMoves.append((2,1))
			if board[0][2] == board[1][2] != '-' and board[2][2] == '-':
				possibleMoves.append((2,2))

			#Col 1,2,3, X - X
			if board[0][0] == board[2][0] != '-' and board[1][0] == '-':
				possibleMoves.append((1,0))
			if board[0][1] == board[2][1] != '-' and board[1][1] == '-':
				possibleMoves.append((1,1))
			if board[0][2] == board[2][2] != '-' and board[1][2] == '-':
				possibleMoves.append((1,2))

			#Col 1,2,3 - X X
			if board[1][0] == board[2][0] != '-' and board[0][0] == '-':
				possibleMoves.append((0,0))
			if board[1][1] == board[2][1] != '-' and board[0][1] == '-':
				possibleMoves.append((0,1))
			if board[1][2] == board[2][2] != '-' and board[2][2] == '-':
				possibleMoves.append((0,2))

			#Dia L-R
			if board[0][0] == board[1][1] != '-' and board[2][2] == '-':
				possibleMoves.append((2,2))
			if board[1][1] == board[2][2] != '-' and board[0][0] == '-':
				possibleMoves.append((0,0))
			if board[0][0] == board[2][2] != '-' and board[1][1] == '-':
				possibleMoves.append((1,1))

			#Dia R-L
			if board[0][2] == board[1][1] != '-' and board[2][0] == '-':
				possibleMoves.append((2,0))
			if board[0][2] == board[2][0] != '-' and board[1][1] == '-':
				possibleMoves.append((1,1))
			if board[2][0] == board[1][1] != '-' and board[0][2] == '-':
				possibleMoves.append((0,2))

			return possibleMoves

class Node(object):
	
	"""
		board = checksum value - int array
		parent = node object
		children = list of type node objects 
		hn = heuristic function - int
	"""

	def __init__(self, board, parent, children, hn):
		"""Basic data structure for game tree"""
		super(Node, self).__init__()
		self.board = []
		self.parent = parent
		self.children = []
		self.hn = hn 

	def getBoard(self):
		return self.board

	def getHeuristic(self):
		return self.hn

	def setHeuristic(self,hn):
		self.hn = hn

	def getChildren(self):
		return self.children

	def setChild(self,child):
		self.children.append(child)

	def getParent(self):
		return self.parent

	def setParent(self,parent):
		self.parent = parent

	def findchecksum(self,real_board,xstart,xend,ystart,yend):
		""" Helper function, called from boardToChecksum """
		string = '00000'
		for i in range(xstart,xend):		
			for j in range(ystart,yend):

				if(real_board[i][j] == 'x' or real_board[i][j] == 'X'):
					string += '010'
				if(real_board[i][j] == 'o' or real_board[i][j] == 'O'):
					string += '001'
				if(real_board[i][j] == ' ' or real_board[i][j] == '-'):
					string += '000'
		self.board.append(int(string, 2))
		return


	def boardToChecksum(self, real_board):
		""" converting the actual board layout to checksum values """
		self.board = []

		xstart = 0
		xend = 3
		ystart = 0
		yend = 3

		for i in range(0,3):
			self.findchecksum(real_board,xstart,xend,ystart,yend)
			ystart += 3
			yend += 3


		xstart = 3
		xend = 6
		ystart = 0
		yend = 3
		for i in range(3,6):
			self.findchecksum(real_board,xstart,xend,ystart,yend)
			ystart += 3
			yend += 3

		xstart = 6
		xend = 9
		ystart = 0
		yend = 3
		for i in range(3,6):
			self.findchecksum(real_board,xstart,xend,ystart,yend)
			ystart += 3
			yend += 3
	
		return self.board

	def makeBoard(self,iterator,real_board,xstart,xend,ystart,yend):
		""" Helper function, called from checksumToBoard """
		value = self.board[iterator]

		value = bin(value)[2:]
		for pad in range(0,32 -len(value)):
			value = '0' + value

		it = 5  # padding of extra 5 bits (32 -27)

		for i in range(xstart,xend):
			for j in range(ystart, yend):
				temp = value[it]
				temp += value[it+1] 
				temp += value[it+2]
				it += 3
				var = int(temp,2)

				if( var == 0 ):
					real_board[i][j] =  '-'
				if( var == 1 ):
					real_board[i][j] =  'o'
				
				if( var == 2 ):
					real_board[i][j] =  'x'
	

	def checksumToBoard(self):
		""" converting the checksum calculated to the actual layout of the board """
		real_board = [[ '.' for x in range(9)] for x in range(9)] 

		xstart = 0
		xend = 3
		ystart = 0
		yend = 3

		for i in range(0,3):
			self.makeBoard(i,real_board,xstart,xend,ystart,yend)
			ystart += 3
			yend += 3

	
		xstart = 3
		xend = 6
		ystart = 0
		yend = 3
		for i in range(3,6):
			self.makeBoard(i,real_board,xstart,xend,ystart,yend)
			ystart += 3
			yend += 3


		xstart = 6
		xend = 9
		ystart = 0
		yend = 3
		for i in range(6,9):
			self.makeBoard(i,real_board,xstart,xend,ystart,yend)
			ystart += 3
			yend += 3
		return real_board

	def printNode(self):
		real_board = self.checksumToBoard()
		print 'Board created from checksum values:'
		for i in range(0,9):
			for j in range(0,9):
				print real_board[i][j],
				if j%3 == 2:
					print "|",
			print
			if i%3 == 2:
				print " _ _ _ _ _ _ _ _ _"



#### Testing for making move
# root = Node(-1,-1,-1,-1)
# comp = Player21();
# empty_board = [['-','-', '-', '-', '-','-','-','-','-'] for x in xrange(0,9)]
# board_stat = [ '-' for i in xrange(0,9)]
# empty_board[4][4] = 'o'
# empty_board[5][5] = 'x'
# empty_board[7][7] = 'x'
# i = 7
# j = 7
# empty_board[i][j] = comp.symbol  #First move for now
# root.board = root.boardToChecksum(empty_board)
# print comp.move(empty_board,board_stat, (i,j), 'o');

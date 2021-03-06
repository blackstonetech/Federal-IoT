from player import *
from utils import load
import random
import threading
class QAgent(Player):
    def __init__(self, name):
        super().__init__(name)
        try:
            self.Memory = load()
        except:
            self.Memory = {}
        #print(self.Memory)
        self.CurrentMove = (-1,-1)
        self.lock = threading.Lock()

    def GetLeagalMoves(self, board):
        moves = []
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j] != 'X' and board[i][j] != 'O':
                    moves.append((i,j))
        return moves

    def GetQValueOfMove(self, move, board):
        return self.Memory.get(self.BoardAndNextMovetoString(board,move), 0)

    def GetMove(self, board):
        legalMoves = self.GetLeagalMoves(board)
        #print("All leagal moves: ", legalMoves)
        # always exploring, no policy yet
        # This is where the policy code would go
        # m = random.choice(legalMoves)
        m = random.choice(legalMoves)
        for c in legalMoves:
            if self.GetQValueOfMove(c,board) > self.GetQValueOfMove(m,board):
                m = c



        # --------------------------------

        if self.CurrentMove != (-1,-1):
            self.UpdateQval(board,self.BoardAndMovetoString(board, self.CurrentMove),self.BoardAndNextMovetoString(board,m))
        # else:
        #     self.Memory[self.BoardAndMovetoString(board, self.CurrentMove)] = 0

        self.CurrentMove = m
        #print(threading.activeCount())
        return m[0], m[1]
    
    def SendGameOverMessage(self, result, board):
        super().SendGameOverMessage(result,board)
        if result == self.Name:
            reward = 2
        elif result =="Tie":
            reward = 1
        else:
            reward = -1
        with self.lock:
            self.Memory[self.BoardAndMovetoString(board,self.CurrentMove)] = self.Memory.get(self.BoardAndMovetoString(board,self.CurrentMove),0) + reward
        #print(self.Memory)

    def BoardAndMovetoString(self, board, move):
        s = ""
        for i in range(0,3):
            for j in range(0,3):
                s+=str(board[i][j])
        return s+str(move[0])+str(move[1])

    def BoardAndNextMovetoString(self, board,move):
        s = ""
        for i in range(0,3):
            for j in range(0,3):
                if i == move[0] and j == move[1]:
                    s+=str(self.Name)
                else:
                    s+=str(board[i][j])
        return s+str(move[0])+str(move[1])

    def UpdateQval(self, board, state, nextstate):
        #print(state, self.Memory.get(state), nextstate, self.Memory.get(nextstate))
        with self.lock:
            if self.Memory.get(nextstate, False) and self.Memory.get(state, False):
                self.Memory[state] = self.Memory[state] + self.Memory.get(nextstate)*.5*len(self.GetLeagalMoves(board))
                #self.Memory[state] = self.Memory.get(state) + 0.9*(self.Memory.get(nextstate) - self.Memory.get(state))
            else:
                if self.Memory.get(nextstate, True):
                    # print("wrote0")
                    self.Memory[nextstate] = 0.0
                if self.Memory.get(state, True):
                    # print("wrote0")
                    self.Memory[state] = 0.0
            

        # try:
        #     self.Memory[state] = self.Memory[state] + self.Memory[nextstate]
        #     #print("\n\n\n\nupdated\n\n\n\n\n\n")
        #     #print(self.Memory)
        # except:
        #     self.Memory[nextstate] = 0.01
        #     #print("set 0")



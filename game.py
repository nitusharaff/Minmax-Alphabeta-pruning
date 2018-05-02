import numpy as np
import copy
from operator import itemgetter
class game:
 board_state=[]
 weight=[]
 depth=0
 count_nodes=0
 algorithm_use=""
 current_player= ""
 current_opponent=""
 player_pos=[]
 opponent_pos=[]
 circle_pass=0
 star_pass=0
 def cal_utility(self, boardstate,player):
    util=s=c=0

    for (elem, i), value in np.ndenumerate(boardstate):

                if (boardstate[elem][i])[:1]== "S":
                    s = s + int(self.weight[7- elem])* int((boardstate[elem][i])[1:2])

                if (boardstate[elem][i])[:1]== "C":
                    c = c + int(self.weight[elem])* int((boardstate[elem][i])[1:2])

                #elif boardstate[elem][i]=="C1":
                 #   c=c+ int(self.weight[elem])
                #elif boardstate[elem][i] == "C2":
                 #   c = c + int(self.weight[elem])*2
    if player == True:
        util= s-c
    else:
        util =c-s
    return util
     

 def game_end(self, boardstate, depthnw):

     star = circle = 0
     if int(depthnw) >= int(self.depth):
         return True

     elif self.circle_pass==1 and self.star_pass==1:
         return True

     for (elem, i), value in np.ndenumerate(boardstate):
             if boardstate[elem][i] == "S1":
                star=star+1

             elif boardstate[elem][i] == "S2":
                 star = star + 2

             elif boardstate[elem][i] == "C1":
                circle=circle+1
             elif boardstate[elem][i] == "C2":
                 circle = circle + 2
     if circle==0 and star!=0:
             return True
     elif circle!=0 and star==0:
             return True

     return False





 def possible_moves(self,board_state,player):
    available=[]
    if (player==0):
     player_pos = zip(*np.where(board_state == "C1"))
     for pos in player_pos:
        if pos[1] != 0 and pos[1] != 7  and pos[0]!=7:  #if not a corner element

          if board_state[pos[0]+1][pos[1]+1] == "0" or (pos[0]+1 ==7 and (board_state[pos[0]+1][pos[1]+1])[:1] == "C"):  #if diagonal way is empty
             available.append(str(pos[0])+ str(pos[1]) + "-"+str(pos[0]+1)+ str(pos[1]+1))


          if board_state[pos[0]+1][pos[1]-1] == "0" or (pos[0]+1 ==7 and (board_state[pos[0]+1][pos[1]-1])[:1] == "C"):  #if diagonal way is empty
              available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] + 1) + str(pos[1] - 1))

          if board_state[pos[0] + 1][pos[1] + 1] == ("C1"): #if diagonally theres the opponent
                if (pos[0]+2)<=7 and pos[1]+2<=7  and (board_state[pos[0] + 2][pos[1] + 2]== "0" or (pos[0]+2 ==7 and (board_state[pos[0]+2][pos[1]+2])[:1] == "C")) :  #if diagonal is opponent+ next to opponenet is empty
                    available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] + 2) + str(pos[1] + 2))

          if board_state[pos[0] +1][pos[1] - 1] == ( "C1"):  # if diagonally theres the opponent
                if (pos[0]+2)<=7 and pos[1]-1>=0 and board_state[pos[0] + 2][pos[1] - 2] == "0" or (pos[0]+2 ==7 and (board_state[pos[0]+2][pos[1]-2])[:1] == "C"):  # if diagonal is opponent+ next to opponenet is empty
                    available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] + 2) + str(pos[1] - 2))

        elif pos[1]==0 and pos[0]!=7: # first line without end corner 70
            if board_state[pos[0] + 1][pos[1] + 1] == "0" or  ((pos[0]+1)==7 and (board_state[pos[0] + 1][pos[1] + 1])[:1] == "C"):  # if diagonal way is empty
                available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] + 1) + str(pos[1] + 1))

            if board_state[pos[0] + 1][pos[1] + 1] == ("S1"):  # if diagonally theres the opponent
                if (pos[0]+2)<=7 and pos[1]+2<=7 and (board_state[pos[0] + 2][pos[1] + 2] == "0" or (pos[0]+2==0 and (board_state[pos[0] + 2][pos[1] + 2])[:1] == "C")):  # if diagonal is opponent+ next to opponenet is empty
                    available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] + 2) + str(pos[1] + 2))

        elif pos[1]==7 and pos[0]!=7: # last line without end corner 77
            if board_state[pos[0] + 1][pos[1] -1] == "0":  # if diagonal way is empty
                available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] + 1) + str(pos[1] - 1))

            if board_state[pos[0] + 1][pos[1] -1] == ("S1"):  # if diagonally theres the opponent
                if (pos[0]+2)<=7  and pos[1]+2<=7 and (board_state[pos[0] + 2][pos[1] - 2] == "0" or (pos[0]+2==0 and (board_state[pos[0] + 2][pos[1] - 2])[:1] == "C")):  # if diagonal is opponent+ next to opponenet is empty
                    available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] + 2) + str(pos[1] - 2))


    else:
         player_pos = zip(*np.where(board_state == "S1"))

         for pos in player_pos:
             if pos[1] != 0 and pos[1] != 7 and pos[0] != 0:  # if not a corner element

                 if board_state[pos[0] - 1][pos[1] + 1] == "0" or (pos[0] - 1 == 0 and (board_state[pos[0] - 1][pos[1] + 1])[:1] == "S"):  # if diagonal way is empty or last row reached
                     available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] - 1) + str(pos[1] + 1))

                 if board_state[pos[0] - 1][pos[1] - 1] == "0" or (pos[0] - 1 == 0 and (board_state[pos[0] - 1][pos[1] - 1])[:1] == "S"):  # if diagonal way is empty or last row reached
                     available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] - 1) + str(pos[1] - 1))

                 if board_state[pos[0] - 1][pos[1] + 1] == ("C1"):  # if diagonally theres the opponent
                     if (pos[0]-2)>=0 and (pos[1]+2)<=7 and (board_state[pos[0] - 2][pos[1] + 2] == "0" or (pos[0] - 2 == 0 and (board_state[pos[0] - 2][pos[1] + 2])[:1] == "S")):  # if diagonal is opponent+ next to opponenet is empty
                         available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] - 2) + str(pos[1] + 2))

                 if board_state[pos[0] - 1][pos[1] - 1] == ("C1"):  # if diagonally theres the opponent
                     if (pos[0]-2)>=0 and pos[1]-2>=0 and (board_state[pos[0] - 2][pos[1] - 2] == "0" or (pos[0] - 2 == 0 and (board_state[pos[0] - 2] [pos[1] - 2])[:1] == "S")):  # if diagonal is opponent+ next to opponenet is empty
                         available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] - 2) + str(pos[1] - 2))

             elif pos[1] == 0 and pos[0]!=0 : #first y line without 00
                 if board_state[pos[0] - 1][pos[1] + 1] == "0" or  ((pos[0]-1)==0 and (board_state[pos[0] - 1][pos[1] + 1])[:1] == "S") :  # if diagonal way is empty
                     available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] - 1) + str(pos[1] + 1))

                 elif board_state[pos[0] - 1][pos[1] + 1] == ("C1")  :  # if diagonally theres the opponent
                     if (pos[0]-2)>=0 and pos[1]+2<=7 and (board_state[pos[0] - 2][pos[1] + 2] == "0" or (pos[0]-2==0 and (board_state[pos[0] - 2][pos[1] + 2])[:1] == "S")) :  # if diagonal is opponent+ next to opponenet is empty
                         available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] - 2) + str(pos[1] + 2))

             elif pos[1] == 7 and pos[0]!=0: #last line of y without 77
                 if board_state[pos[0] - 1][pos[1] - 1] == "0":  # if diagonal way is empty
                     available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] - 1) + str(pos[1] - 1))

                 elif board_state[pos[0] - 1][pos[1] - 1] == ("C1"):  # if diagonally theres the opponent
                     if (pos[0]-2)>=0 and pos[1]-2>=0 and (board_state[pos[0] - 2][pos[1] - 2] == "0" or (pos[0]-2==0 and (board_state[pos[0] - 2][pos[1] - 2])[:1] == "S"))  :  # if diagonal is opponent+ next to opponenet is empty
                         available.append(str(pos[0]) + str(pos[1]) + "-" + str(pos[0] - 2) + str(pos[1] - 2))

    if not available:
        if player==1:
            self.star_pass=1
            available.append("pass")
        else:
            self.circle_pass=1
            available.append("pass")
    if available[0]!="pass":
      available.sort(key=lambda item: ((int(item[0])), (int(item[1])), (int(item[3])), int(item[4])))

    return available


 def next_state(self,boardgame,move):


    if (move!="pass"):
     move_from=np.asarray([int(move[0]),int(move[1])])
     move_to=  np.asarray([int(move[3]),int(move[4])])

     if move_to[0]!=7 and (move_to[0]==move_from[0]+1 and (move_to[1]==move_from[1]+1 or  move_to[1]==move_from[1]-1)): #circle moving diagonally not at end
         boardgame[move_to[0]][move_to[1]] = "C1"
         boardgame[move_from[0]][move_from[1]] = "0"

     elif move_to[0]!=0 and (move_to[0]==move_from[0]-1 and (move_to[1]==move_from[1]+1 or  move_to[1]==move_from[1]-1)): #for star moving diagonally not at end
         boardgame[move_to[0]][move_to[1]]= "S1"
         boardgame[move_from[0]][move_from[1]] = "0"

     elif  move_to[0]==move_from[0]+2 and  (move_to[1]==move_from[1]+2):  #circle
          if (move_to[0]==7) and (boardgame[move_to[0]][move_to[1]])[:1] == "C" :
              boardgame[move_to[0]][move_to[1]] = "C"+ str(int((boardgame[move_to[0]][move_to[1]])[1:2])+1)
          else:
              boardgame[move_to[0]][move_to[1]] = "C1"
          boardgame[move_from[0]+1][move_from[1]+1] = "0"
          boardgame[move_from[0]][move_from[1]] = "0"

     elif move_to[0] == move_from[0] + 2 and (move_to[1] == move_from[1] - 2):  # circle
         if (move_to[0] == 7) and (boardgame[move_to[0]][move_to[1]])[:1] == "C":
             boardgame[move_to[0]][move_to[1]] = "C" + str(int((boardgame[move_to[0]][move_to[1]])[1:2]) + 1)
         else:
             boardgame[move_to[0]][move_to[1]] = "C1"
         boardgame[move_from[0] + 1][move_from[1] - 1] = "0"
         boardgame[move_from[0]][move_from[1]] = "0"


     elif  move_to[0]==move_from[0]-2 and  (move_to[1]==move_from[1]+2): #star
         if (move_to[0] == 0) and (boardgame[move_to[0]][move_to[1]])[:1] == "S":
             boardgame[move_to[0]][move_to[1]] = "S" + str(int((boardgame[move_to[0]][move_to[1]])[1:2]) + 1)
         else:
             boardgame[move_to[0]][move_to[1]] = "S1"
         boardgame[move_from[0] - 1][move_from[1] + 1] = "0"
         boardgame[move_from[0]][move_from[1]] = "0"


     elif move_to[0] == move_from[0] - 2 and (move_to[1] == move_from[1] - 2): #star
         if (move_to[0] == 0) and (boardgame[move_to[0]][move_to[1]])[:1] == "S":
             boardgame[move_to[0]][move_to[1]] = "S" + str(int((boardgame[move_to[0]][move_to[1]])[1:2]) + 1)

         else:
             boardgame[move_to[0]][move_to[1]] = "S1"
         boardgame[move_from[0] - 1][move_from[1] - 1] = "0"
         boardgame[move_from[0]][move_from[1]] = "0"

     elif move_to[0]==0 and   boardgame[move_to[0]][move_to[1]] == "0":
         boardgame[move_to[0]][move_to[1]] = "S1"
         boardgame[move_from[0]][move_from[1]] = "0"

     elif move_to[0]==7 and   boardgame[move_to[0]][move_to[1]] == "0":
         boardgame[move_to[0]][move_to[1]] = "C1"
         boardgame[move_from[0]][move_from[1]] = "0"

     elif move_to[0] == 0 and (boardgame[move_to[0]][move_to[1]])[:1] == "S":
         boardgame[move_to[0]][move_to[1]] = "S" + str(int((boardgame[move_to[0]][move_to[1]])[1:2]) + 1)
         boardgame[move_from[0]][move_from[1]] = "0"


     elif move_to[0] == 7 and (boardgame[move_to[0]][move_to[1]])[:1] == "C":
         boardgame[move_to[0]][move_to[1]] = "C" + str(int((boardgame[move_to[0]][move_to[1]])[1:2]) + 1)
         boardgame[move_from[0]][move_from[1]] = "0"
     return boardgame



 def get_details(self):
    f = open("input.txt", "r")
    input_given = []
    for line in f:
        input_given.append(line)
    input_given = map(lambda s: s.strip(), input_given)
    self.weight = np.asarray(input_given[11].split(","))
    #weight.reshape((1,len(weight)))
    self.current_player= input_given[0]
    if self.current_player== "Star":
        self.current_opponent = "Circle"

    else:
        self.current_opponent= "Star"
    current= self.current_player[0]+"1"
    opp = self.current_opponent[0]+ "1"
    algorithm_use=input_given[1]
    self.depth=input_given[2]
    for i in input_given[3:11]:
        self.board_state.append(i.split(","))
    self.board_state= np.array(self.board_state)

  #  game_obj.cal_utility(self.board_state,self.current_player)
    if algorithm_use=="ALPHABETA":
        best= alphabeta(self.board_state,self.current_player)
    elif algorithm_use== "MINIMAX":
        best = minimax(self.board_state, self.current_player)
    return self.board_state


 def tiebreak(self, best_move,move):
     if best_move[0] == move[0]:
         if best_move[1]< move[1] and best_move[1] != move[1] :
             return  best_move
         else:
             return move

     elif best_move[0] == move[0] and best_move[1] == move[1]:

         if best_move[3]==move[3]:
             if best_move[4]< move[4]:
                 return  best_move
             else :
                 return move

         if best_move[3] < move[3]:
             return best_move
         else:
             return move

     elif  best_move[0]<move[0]:
         return  best_move

     else:
         return move

def minimax(board_state,player):
  if player=="Star":
      player =1
  else:
      player=0
  board = copy.deepcopy(board_state)
  moves = game_obj.possible_moves(board_state,player)
  best_move = moves[0]
  best_score = float('-inf')
  for move in moves:
    board_state = copy.deepcopy(board)
    game_obj.count_nodes = game_obj.count_nodes + 1
    if move=="pass":
        if game_obj.game_end(board_state, 0):
            return game_obj.cal_utility(board_state, not player)
        score = min_play(board_state, 0, not player)
    else:
     clone = game_obj.next_state(board_state,move)
     score = min_play(clone, 0, not player)
    if score== best_score:
        x = game_obj.tiebreak(best_move,move)
        best_move= x
    elif score > best_score:
        best_move = move
        best_score = score
  if best_move=="pass":
      myopo = game_obj.cal_utility(board, player)
  else:
     next= game_obj.next_state(board, best_move)
     myopo= game_obj.cal_utility(next,player)
  if best_move != "pass":
      bestmoveout = chr(72 - int(best_move[0])) + str(int(best_move[1]) + 1) + best_move[2] + chr(72 - int(best_move[3])) + str(int(best_move[4]) + 1)
  else:
      bestmoveout = "pass"
  f = open('output.txt', 'w')
  f.write(bestmoveout )
  f.write("\n")
  f.write(str(myopo))
  f.write("\n")
  f.write(str(best_score))
  f.write("\n")
  f.write(str(int(game_obj.count_nodes)+1))
  f.close()
  return best_move


def min_play(board_state,depth,player):
     depth=depth+1
     if game_obj.game_end(board_state, depth):
         return game_obj.cal_utility(board_state, not player)
     moves = game_obj.possible_moves(board_state,player)
     best_score = float('inf')
     board=copy.deepcopy(board_state)
     for move in moves:
        game_obj.count_nodes = game_obj.count_nodes + 1
        board_state = copy.deepcopy(board)
        if move=="pass":
            if game_obj.game_end(board_state, depth):
                return game_obj.cal_utility(board_state, not player)
            score= max_play(board_state,depth,not player)
        else:
         clone = (game_obj.next_state(board_state,move))
         score = max_play(clone,depth,not player)
        if score <= best_score:
             best_move = move
             best_score = score
     return best_score

def max_play(board_state,depth,player):
     depth=depth+1
     if game_obj.game_end(board_state, depth):
         return game_obj.cal_utility(board_state,player )
     moves = game_obj.possible_moves(board_state,player)
     best_score = float('-inf')
     board=copy.deepcopy(board_state)
     for move in moves:
         game_obj.count_nodes = game_obj.count_nodes + 1
         board_state = copy.deepcopy(board)
         if move == "pass":
             if game_obj.game_end(board_state, depth):
                 return game_obj.cal_utility(board_state, player)
             score = min_play(board_state,depth,not player)
         else:
            clone = game_obj.next_state(board_state, move)
            score = min_play(clone,depth,not player)
         if score >= best_score:
             best_move = move
             best_score = score
     return best_score


def alphabeta(board_state,player):
  if player=="Star":
      player =1
  else:
      player=0
  board = copy.deepcopy(board_state)
  moves = game_obj.possible_moves(board_state,player)
  best_move = moves[0]
  best_score = float('-inf')
  alpha= float('-inf')
  beta= float('inf')
  for move in moves:
    board_state = copy.deepcopy(board)
    game_obj.count_nodes = game_obj.count_nodes + 1
    if move=="pass":
        if game_obj.game_end(board_state, 0):
            return game_obj.cal_utility(board_state, player)
        score = min_play_ab(board_state, 0,not player,alpha,beta)
    else:
     clone = game_obj.next_state(board_state,move)
     score = min_play_ab(clone, 0, not  player,alpha,beta)
    if score== best_score:
        x = game_obj.tiebreak(best_move,move)
        best_move= x
    elif score > best_score:
        best_move = move
        best_score = score
    if best_score >= beta:
      return best_score
    alpha = max(best_score, alpha)
  if best_move=="pass":
      myopo = game_obj.cal_utility(board, player)
  else:
     next= game_obj.next_state(board, best_move)
     myopo= game_obj.cal_utility(next,player)
  if best_move!= "pass":
    bestmoveout = chr(72 - int(best_move[0])) + str(int(best_move[1]) + 1) + best_move[2] + chr(72 - int(best_move[3])) + str(int(best_move[4]) + 1)
  else:
      bestmoveout="pass"
  f = open('output.txt', 'w')
  f.write(bestmoveout)
  f.write("\n")
  f.write(str(myopo))
  f.write("\n")
  f.write(str(best_score))
  f.write("\n")
  f.write(str(int(game_obj.count_nodes) + 1))
  f.close()
  return best_move


def min_play_ab(board_state, depth, player, alpha, beta):
    depth = depth + 1
    if game_obj.game_end(board_state, depth):
        return game_obj.cal_utility(board_state, not player)
    moves = game_obj.possible_moves(board_state, player)
    best_score = float('inf')
    board = copy.deepcopy(board_state)
    for move in moves:

        game_obj.count_nodes = game_obj.count_nodes + 1
        board_state = copy.deepcopy(board)
        if move == "pass":
            if game_obj.game_end(board_state, depth):
                return game_obj.cal_utility(board_state,not player)
            score = max_play_ab(board_state, depth, not player, alpha, beta )
        else:
            clone = (game_obj.next_state(board_state, move))
            score = max_play_ab(clone, depth, not player,alpha,beta)
        if score <= best_score:
            best_move = move
            best_score = score
        if best_score <= alpha:
                return best_score
        beta = min(best_score, beta)
    return best_score



def max_play_ab(board_state,depth,player,alpha,beta):
     depth=depth+1
     if game_obj.game_end(board_state, depth):
         return game_obj.cal_utility(board_state,  player)
     moves = game_obj.possible_moves(board_state,player)
     best_score = float('-inf')
     board=copy.deepcopy(board_state)
     for move in moves:
         game_obj.count_nodes = game_obj.count_nodes + 1
         board_state = copy.deepcopy(board)
         if move == "pass":
             if game_obj.game_end(board_state, depth):
                 return game_obj.cal_utility(board_state,  player)
             score = min_play_ab(board_state,depth,not player,alpha,beta)
         else:
            clone = game_obj.next_state(board_state, move)
            score = min_play_ab(clone,depth,not player,alpha,beta)
         if score >= best_score:
             best_move = move
             best_score = score
         if best_score>= beta:
             return best_score
         alpha=max(best_score,alpha)
     return best_score



game_obj= game()
x=game_obj.get_details()

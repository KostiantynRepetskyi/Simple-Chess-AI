import time
import random
import sys
import berserk



   



class Chess():
    piece_dictionary = {"wn":"♘ ", "bn":"♞ ","wb":"♗ ", "bb":"♝ ", "wr":"♖ ", "br":"♜ ", "wq":"♕ ", "bq":"♛ ", "wk":"♔ ", "bk":"♚ ", "wp":"♙ ", "bp":"♟ "}
# this dictionary is used to change between display and input notation 

    Xnotation = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    inverse_Xnotation = {0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}
    Ynotation = {"8":0,"7":1,"6":2,"5":3,"4":4,"3":5,"2":6,"1":7}
    inverse_Ynotation = {0:"8",1:"7",2:"6",3:"5",4:"4",5:"3",6:"2",7:"1"}

    def __init__(self, chess_board, m, d):
        self.board = chess_board
        self.__mode = m
        self.__difficulty = d

        white_rook = Piece(["+1+0", "+0+1", "-1+0", "+0-1"], 5)
        black_rook = Piece(["+1+0", "+0+1", "-1+0", "+0-1"], -5)
        white_knight = PointMovingPiece(["+2+1", "+1+2", "-2+1", "+1-2", "+2-1", "-1+2", "-2-1", "-1-2"], 3)
        black_knight = PointMovingPiece(["+2+1", "+1+2", "-2+1", "+1-2", "+2-1", "-1+2", "-2-1", "-1-2"], -3)
        white_bishop = Piece(["+1+1", "+1-1", "-1+1", "-1-1"], 3)
        black_bishop = Piece(["+1+1", "+1-1", "-1+1", "-1-1"], -3)
        white_queen = Piece(["+1+1", "+1-1", "-1+1", "-1-1", "+1+0", "+0+1", "-1+0", "+0-1"], 9)
        black_queen = Piece(["+1+1", "+1-1", "-1+1", "-1-1", "+1+0", "+0+1", "-1+0", "+0-1"], -9)
        white_king = PointMovingPiece(["+1+1", "+0+1", "+1+0", "-1-1", "+0-1", "-1+0", "+1-1", "-1+1"], None)
        black_king = PointMovingPiece(["+1+1", "+0+1", "+1+0", "-1-1", "+0-1", "-1+0", "+1-1", "-1+1"], None)
        white_pawn = Pawn(["+0-1", "+0-2", "-1-1", "+1-1"], 1)
        black_pawn = Pawn(["+0+1", "+0+2", "-1+1", "+1+1"], -1)
# this is composition where the objects are the chess pieces 

        self.objects = {"wr":white_rook, "br":black_rook, "wn":white_knight, "bn":black_knight, "wb":white_bishop, "bb":black_bishop, "wq":white_queen, "bq":black_queen,
                        "wk":white_king, "bk":black_king, "wp":white_pawn, "bp":black_pawn}
        self.__game_over = False
       

    def __checks(self, yKing, xKing, check_board, opposite_colour, colour):
        check = False
        all_rook_moves = (self.objects[colour+"r"]).legal_moves(xKing, yKing, colour, check_board)
        for a in all_rook_moves: 
            piece_in_position_a = (check_board[int(a[1])][int(a[0])])[0:2]
            if piece_in_position_a == opposite_colour + "r" or piece_in_position_a == opposite_colour + "q":
                check = True
        all_bishop_moves = (self.objects[colour+"b"]).legal_moves(xKing, yKing, colour, check_board)
        for b in all_bishop_moves:
            piece_in_position_b = (check_board[int(b[1])][int(b[0])])[0:2]
            if piece_in_position_b == opposite_colour + "b" or piece_in_position_b == opposite_colour + "q":
                check = True
        all_knight_moves = (self.objects[colour+"n"]).legal_moves(xKing, yKing, colour, check_board)
        for c in all_knight_moves:
            if (check_board[int(c[1])][int(c[0])])[0:2] == opposite_colour + "n":
                check = True
        all_king_moves = (self.objects[colour+"k"]).legal_moves(xKing, yKing, colour, check_board)
        for d in all_king_moves:
            if (check_board[int(d[1])][int(d[0])])[0:2] == opposite_colour + "k":
                check = True
        all_pawn_moves = (self.objects[colour+"p"]).legal_moves(xKing, yKing, colour, check_board)
        for e in all_pawn_moves:
            if (check_board[int(e[1])][int(e[0])])[0:2] == opposite_colour + "p":
                check = True
        return check

# this method returns true if it is a check and false if it isn't. It does this by looking at all possible moves for each piece from the square where the king is in.
# If any of these moves land on the opponent's piece which is the same as the piece making the moves than it is check.


    def __chess_AI(self, AI_Board, Kside_moved, Qside_moved, PrevFromY, PrevToX, PrevToY, prevPiece, PieceNumber, pieces_positions):
      AI_board = self.__Copy(AI_Board)
      a = Kside_moved["b"]
      b = Kside_moved["w"]
      c = Qside_moved["b"]
      d = Qside_moved["w"]
      Moved_Kside = {"b":a,"w":b}
      Moved_Qside = {"b":c,"w":d}
      e = PieceNumber["wq"]
      f = PieceNumber["bq"]
      pieceNumber = {"wq":e,"bq":f}
      Tree = [[],[],[],[]]

# these are some things that are assigned to new arrays or dictionaries because I want the original values to not change
# if I just passed the values into tree_creation method than the orinal values would change too because these things are coppied by reference  
      
      Tree, First_moves = self.__tree_creation(Tree, 0, AI_board, "w", "b", Moved_Kside, Moved_Qside, PrevFromY, PrevToX, PrevToY, prevPiece, pieceNumber, "", pieces_positions)
# this is going to return the tree of possible moves 
    
      if self.__difficulty == "2":
          first_move_pick = self.__mini_max(1, "min", Tree[2], Tree)
          first_move_pick = self.__mini_max(0, "max", first_move_pick, Tree)
      elif self.__difficulty == "1":
          first_move_pick = self.__mini_max(0, "max", Tree[1], Tree)
      else:
           first_move_pick = self.__mini_max(2, "max", Tree[3], Tree)
           first_move_pick = self.__mini_max(1, "min", first_move_pick, Tree)
           first_move_pick = self.__mini_max(0, "max", first_move_pick, Tree)
# the best moves are found 
        
      best_move = min(first_move_pick)
      best_moves = []
      for i in range(len(first_move_pick)):
          if first_move_pick[i] == best_move:
              best_moves.append(i)
      
      best_move_index = random.choice(best_moves)
# a move is chosen from an array of best moves  

      return First_moves[best_move_index]

               
    def __mini_max(self, Index, min_or_max, List, Tree):
        new_list = []
        temp_list = []
        for i in Tree[Index]:
            for j in range(0, i):
                value = List.pop(0)
                temp_list.append(value)
            if min_or_max == "max":
                new_list.append(max(temp_list))
            else:
                new_list.append(min(temp_list))
            temp_list = []
        return new_list
# this funtion helps to choose the best original move by considering the possible move paths        

                
    def __tree_creation(self, Tree, index, AI_board, user_colour, AI_colour, Moved_Kside, Moved_Qside, PrevFromY, PrevToX, PrevToY, prevPiece, pieceNumber, gameover, pieces_positions):
      First_moves = []
      a = Moved_Kside["b"]
      b = Moved_Kside["w"]
      c = Moved_Qside["b"]
      d = Moved_Qside["w"]
      e = pieceNumber["wq"]
      f = pieceNumber["bq"]
      prev_Moved_Kside = {"b":a,"w":b}
      prev_Moved_Qside = {"b":c,"w":d}
      prev_pieceNumber = {"wq":e,"bq":f}
      prev_board = self.__Copy(AI_board)
      prevPrevToX, prevPrevToY = PrevToX, PrevToY
      prevPrevFromY, prevPrevPiece = PrevFromY, prevPiece
      prev_gameover = gameover 
      all_moves_count = 0
# these are some things that need to be stored in new variables so that any changes to these can be reversed when looking at a different move path 

      for a in pieces_positions:
# loop that goes through all the pieces of AI_colour 
        x ,y = int(a[0]), int(a[1])
        piece = AI_board[y][x]
# the piece in the position x and y is stored in piece
        Object = (self.objects[(AI_board[y][x])[0:2]])
        all_moves = Object.legal_moves(x, y, AI_colour, AI_board)
# all posible moves for the piece are stored in all_moves
        if piece[1] == "k":
            if Moved_Qside[AI_colour] == False:
                Qcastle_board, Qlegal, Moved_Kside, Moved_Qside = self.__Qcastling(AI_board, x, y, user_colour, AI_colour, Moved_Kside, Moved_Qside, True)
                if Qlegal == True:
                    all_moves.append("Qcastle")
# if queen's side castling is possible than it is added to all_moves
            if Moved_Kside[AI_colour] == False:
                Kcastle_board, Klegal, Moved_Kside, Moved_Qside = self.__Kcastling(AI_board, x, y, user_colour, AI_colour, Moved_Kside, Moved_Qside, True)
                if Klegal == True:
                    all_moves.append("Kcastle")
# if king's side castling is possible than it is added to all_moves
        if piece[1] == prevPiece[1] == "p":
            en_passant_value = Object.en_passant_conditions(x, y, PrevFromY, PrevToX, PrevToY)
            if en_passant_value != "":
                all_moves.append("en-passant")
# if en-passant is possible than it is added to all_moves            
        prevPiece = piece
        PrevFromY = y
        all_moves_count = all_moves_count + len(all_moves)
# all moves count stores the number of possible moves in a position for pieces of AI_colour and it does this by adding up the number of possible moves for each piece of that colour
        for i in all_moves:
# loop that goes through all the possible moves for the piece
            if i == "Qcastle":
                AI_board = self.__Copy(Qcastle_board)
            elif i == "Kcastle":
                AI_board = self.__Copy(Kcastle_board)
            elif i == "en-passant":
                AI_board = Object.new_en_passant_board(AI_board, x, y, int(en_passant_value[0]), int(en_passant_value[1]), PrevToX, PrevToY)
                PrevToX = int(en_passant_value[0])
                PrevToY = int(en_passant_value[1])
            else:
                AI_board = self.__oldboard_to_newboard(AI_board, x, y, int(i[0]), int(i[1]))
                if piece[0:2] == "wp" and i[1] == "0" or (piece[0:2] == "bp" and i[1] == "7"):
                    AI_board[int(i[1])][int(i[0])] = AI_colour + "q" + str(pieceNumber[AI_colour + "q"])
                    pieceNumber[AI_colour + "q"] = pieceNumber[AI_colour + "q"] + 1
                PrevToX = int(i[0])
                PrevToY = int(i[1])
# the board is updated with the move stored in i        
            pieces_positions, king1, king2 = self.__positions(AI_board, user_colour)   
            check = self.__checks(int(king2[1]), int(king2[0]), AI_board, user_colour, AI_colour)
# if check is true than its check for the side that just made a move and false if not   
            if check == False:
                Moved_Kside, Moved_Qside = self.__moved(piece, Moved_Kside, Moved_Qside)
# these variables are updated. They keep track if the king or the rooks have moved. If they have, than some of the castling conditions might not be met in the future
                if index == 0:
                    Board = self.__Copy(AI_board)
# coping the AI_board by value to Board
                    First_moves.append(Board)
# this position is added to initial possible moves (one of these is going to be played by the AI side). This only happens if the index is 0, so the first pass of recursion                 
                elif index == int(self.__difficulty):
                    score = self.__total_score(AI_board)
                    if self.__difficulty == "1":
                        if self.__mate(AI_board, AI_colour, user_colour, y, i[0], i[1], pieces_positions, int(king1[0]), int(king1[1])) == True:
                            score = 100
# if black gets checkmated and the difficulty is 1 than the score is 100 
                    Tree[int(self.__difficulty)].append(score)
# if it is the last recursive pass than the total score of the position is stored in the final depth of the tree. This depth depends on the chosen difficulty 
            else:
                all_moves_count = all_moves_count - 1
# if it is check than you don't want to consider that move so one is taken away from the all_moves_count
            if index < 2 and check == False and self.__difficulty == "2" or index == 0 and check == False and self.__difficulty == "1" or index < 3 and check == False and self.__difficulty == "3":
# base case when these conditions aren't met
                self.__tree_creation(Tree, index+1, AI_board, AI_colour, user_colour, Moved_Kside, Moved_Qside, PrevFromY, PrevToX, PrevToY, prevPiece, pieceNumber, gameover, pieces_positions)
# if these are conditions are met than the function tree_creation calls it self again but the colour is switched and the updated board is passed through 
            AI_board = self.__Copy(prev_board)
            Moved_Kside["w"], Moved_Kside["b"] = prev_Moved_Kside["w"], prev_Moved_Kside["b"] 
            Moved_Qside["w"], Moved_Qside["b"] = prev_Moved_Qside["w"], prev_Moved_Qside["b"]
            PrevToX, PrevToY = prevPrevToX, prevPrevToY
            pieceNumber["wq"], pieceNumber["bq"] = prev_pieceNumber["wq"], prev_pieceNumber["bq"]
            gameover = prev_gameover
        PrevFromY, prevPiece = prevPrevFromY, prevPrevPiece
# the recursion must have already been through one possible path of moves to get here. So some of the things need to regain there original values and than a different path of moves can be considered
      if all_moves_count == 0:
# if all_moves_count is 0 that means every move must have been a check and this means that its either stalemate of checkmate 
          kingY, kingX = self.__From(AI_colour+"k0", AI_board)        

          if self.__checks(kingY, kingX, AI_board, user_colour, AI_colour) == True:
# if the king is in check and all other moves result in a check, it is checkmate
              if AI_colour == "b":
                  if index == 1:
                      score = 300
                  elif index == 2:
                      score = 200
                  else:
                      score = 100
              else:
                  if index == 1:
                      score = -300
                  elif index == 2:
                      score = -200
                  else:
                      score = -100
# the sooner the checkmate happens the higher the score
          else:
              score = 0
# stalemate is a draw so the score of 0 is given
          if self.__difficulty == "2":
              Tree[2].append(score)
              if index < 3:
                  Tree[1].append(1)
              if index == 1:
                  Tree[0].append(1)
          elif self.__difficulty == "1":
              Tree[1].append(score)
              Tree[0].append(1)
          else:
              Tree[3].append(score)
              if index < 4:
                  Tree[2].append(1)
              if index < 3:
                  Tree[1].append(1)
              if index == 1:
                  Tree[0].append(1)
# if its checkmate or stalemate the you have to ignore any moves after it and a direct path is made to the end of the tree with the score
      elif index == 1:
          Tree[0].append(all_moves_count)
          
      elif index == 2:
          Tree[1].append(all_moves_count)

      elif index == 3:
          Tree[2].append(all_moves_count)
# all_moves_count is stored to keep track of how many children each node in the tree has and this is used later in the mini_max method    

      return Tree, First_moves
# this function creates a tree of possible moves 





    def __mate(self, mate_board, colour, opposite_colour, fromY, toX, toY, pieces_positions, kingX, kingY):
            temp_board = self.__Copy(mate_board)
# temp_board is assigned the contents of board because this method is going to be making changes to the chessboard and I dont want these changes to be made to the original board
# function copy is used because if you just made the two equal, than as you make a change to one, this change is going to automatically be done to the other

            prev_temp_board = self.__Copy(temp_board)
# the contents of temp_board are copied to prev_temp_board so I can reverse any changes made to temp_board 

            Mate = True
            for a in pieces_positions: 
                x ,y = int(a[0]), int(a[1])
                piece = temp_board[y][x]
                Object = (self.objects[piece[0:2]])
                all_moves = Object.legal_moves(x, y, opposite_colour, temp_board)
# for loop used to focus on a specific piece on the chess board and than all possible moves of that piece are stored in all_moves list 
                        
                for i in all_moves:
                     temp_board = self.__oldboard_to_newboard(temp_board, x, y, int(i[0]), int(i[1]))
                     if piece[1] == "k":
                         if self.__checks(int(i[1]), int(i[0]), temp_board, colour, opposite_colour) == False: 
                            Mate = False
                     else:
                         if self.__checks(kingY, kingX, temp_board, colour, opposite_colour) == False: 
                            Mate = False  
# for loop goes through all the moves in the all_moves list applaying them to temp_board and, after, seeing if the opponent is in check
# if it is not check than it can't be checkmate or stalemate 
                                
                     temp_board = self.__Copy(prev_temp_board)
# the move is undone so the loop can repeat the same process for a different move in all_moves 
                            
                if (temp_board[y][x])[1] == "p":
                    en_passant_value = Object.en_passant_conditions(x, y, fromY, toX, toY)
                    if en_passant_value != "":
                        temp_board = Object.new_en_passant_board(temp_board, x, y, int(en_passant_value[0]), int(en_passant_value[1]), toX, toY)
                        if self.__checks(kingY, kingX, temp_board, colour, opposite_colour) == False:
                            Mate = False
                        temp_board = self.__Copy(prev_temp_board)
# this does the same thing as the part above but for en-passant move which isn't in all_moves list
            return Mate
   



    def __gameover_output(self, gameover_board, move, prev_move, yFrom, xTo, yTo, pieces_positions, King1, King2, boards_stack):
            if self.__mate(gameover_board, move[0], prev_move[0], yFrom, xTo, yTo, pieces_positions, King1, King2) == True:
                self.__game_over = True
                if self.__checks(King2, King1, gameover_board, move[0], prev_move[0]) == True:
                    if move[0] == "w":
                        print ("white wins by checkmate")
                    else:
                        print ("black wins by checkmate")
                else:
                    print ("its a draw by stalemate")   

            elif self.__insufficient_material(gameover_board) == True:
                self.__game_over = True
                print ("its a draw by insufficient material")

            elif self.__repetition_draw(gameover_board, boards_stack, move[0]) == True:
                self.__game_over = True
                print ("its a draw by repetition")
            
            if self.__game_over == False:
                if self.__theoretical_win(gameover_board) == True:
                    self.__game_over = True
                    print ("This is a theoretical win for black")             
# this method calls other methods to check if the game has ended or not 


    def __insufficient_material(self, ins_board):
        ins_draw = False
        w_count, b_count, w_piece, b_piece = self.__count_pieces(ins_board)
        if w_count==1 and w_piece[1]=="b" or w_count==1 and w_piece[1]=="n":
            if b_count==1 and b_piece[1]=="b" or b_count==1 and b_piece[1]=="n" or b_count==0:
                ins_draw = True

        if b_count==1 and b_piece[1]=="b" and w_count==0 or b_count==1 and b_piece[1]=="n" and w_count==0:
            ins_draw = True 

        if w_count==0 and b_count==0:
            ins_draw = True

        return ins_draw
# this method checks if it is a draw by insufficient_material or not, if yes game_over = True is returned

    def __count_pieces(self, count_board):
        w_count = 0
        b_count = 0
        w_piece = ""
        b_piece = ""
        for row in count_board:
            for piece in row:
                if piece[0] == "w" and piece[1] != "k":
                    w_count = w_count + 1
                    w_piece = piece
                if piece[0] == "b" and piece[1] != "k":
                    b_count = b_count + 1
                    b_piece = piece
        return w_count, b_count, w_piece, b_piece
# this method return the number of white non king pieces on the board and the same for black
# if there is only one piece left for white this piece will be stored in w_piece and the same for the black side 

      
    def __theoretical_win(self, win_board):
        theory_win = False
        w_count, b_count, w_piece, b_piece = self.__count_pieces(win_board)
        if w_count == 0:
            if b_count > 1:
                theory_win = True
            else:
                if b_piece[1] != "p":
                    theory_win = True
                else:
                    y_pawn, x_pawn = self.__From(b_piece, win_board)
                    y_king, x_king = self.__From("wk0", win_board)
                    distance_to_end = 7 - y_pawn
                    if y_king < y_pawn:
                        theory_win = True
                    elif (x_pawn + distance_to_end) < x_king or (x_pawn - distance_to_end) > x_king:
                        theory_win = True 
        return theory_win
# in some positions a side will 100% win with perfect play. This method checks if the current position is one of those

  
    def __repetition_draw(self, rep_board, boards_stack, colour):
        rep_draw = False
        repetitions = 0

        for i in range(len(boards_stack)):
            if boards_stack[i] == rep_board:
                if (colour == "b" and i%2 == 0) or (colour == "w" and i%2 == 1):
                    repetitions += 1
          
        if repetitions == 2:
            rep_draw = True
            
        return rep_draw


    def __board_to_display(self, dis_board):
      display = [["","","","","","","",""],
                 ["","","","","","","",""],
                 ["","","","","","","",""],
                 ["","","","","","","",""],
                 ["","","","","","","",""],
                 ["","","","","","","",""],
                 ["","","","","","","",""],
                 ["","","","","","","",""]]
      for y in range(8):
        for x in range(8):
          if dis_board[y][x] != "___":
            display[y][x] = Chess.piece_dictionary[(dis_board[y][x])[0:2]]
          elif (x%2 == 0 and y%2 == 0) or (x%2 == 1 and y%2 == 1):
              display[y][x] = "  "
          else:
              display[y][x] = "██"
      return display
# this method converts the 2D list board into a display


    def __output_display(self, out_board):
      display = self.__board_to_display(out_board)
      print ("")
      print ("ᴀ ʙ ᴄ ᴅ ᴇ ғ ɢ ʜ")
      print ("")
      for y in range(8):
        display_row = ("")
        for x in range(8):
          display_row = display_row + display[y][x]
        print (display_row + "  " + str(8-y))
      print ("")
      for row in out_board:
          print (row)
      print ("")
# this method outputs the display

        
    def __From(self, piece, from_board):
        yFrom = ""
        xFrom = ""
        for y in range(8):
            for x in range(8):
                if from_board[y][x] == piece:
                    yFrom = y
                    xFrom = x 
        return yFrom, xFrom
# this method finds the position of a piece on the board 


    def __positions(self, positions_board, colour):
        pieces_positions = []
        for y in range(8):
            for x in range(8):
                piece = positions_board[y][x]
                if piece[0] == colour:
                    pieces_positions.append(str(x)+str(y))
                    if piece[1] == "k":
                        king1 = str(x)+str(y)
                else:
                    if piece[1] == "k":
                        king2 = str(x)+str(y)
        return pieces_positions, king1, king2
# this method returns the positions of all the pieces of a given colour in an array and also the positions of the kings            

    def __total_score(self, total_board):
        total = 0
        for row in total_board:
            for piece in row:
                if piece != "___" and piece[1] != "k":
                    total = total +  (self.objects[piece[0:2]]).get_value()
        return total
# this method calculates the total score of a position. If this is negative than black is winning and if positive than white is winning


    def __Copy(self, board_1):
        board_2 = [] 
        for i in board_1:
            array = []
            for item in i:
                array.append(item)
            board_2.append(array)
        return board_2
# this allows 2D lists to be copied by value when by defalt in python they are copied by reference because they are objects 


    def __oldboard_to_newboard(self, old_board, fromX, fromY, toX, toY):
        old_board[toY][toX] = old_board[fromY][fromX]
        old_board[fromY][fromX] = "___"
        return old_board
# this method updates the 2D list board with moves


    def __moved(self, Piece, Moved_Kside, Moved_Qside):
        if Piece[1] == "k":
            Moved_Kside[Piece[0]] = True
            Moved_Qside[Piece[0]] = True

        elif Piece[1] == "r":
            if Piece[2] == "1":
                Moved_Kside[Piece[0]] = True
            elif Piece[2] == "0":
                Moved_Qside[Piece[0]] = True
        return Moved_Kside, Moved_Qside
# this method sees if the king or any of the rooks have moved because you can't castle later when they have moved 


    def __wrong_move_input(self, input_board, move):
        flag = False
        while flag == False:
            try:
              yFrom, xFrom = self.__From(move[0:3], input_board)
              if move[3:] != "castlek" and move[3:] != "castleq":
                  yTo = Chess.Ynotation[move[4]]
                  xTo = Chess.Xnotation[move[3]]
            except:
              move = input("the input is not in the correct format, please try again:")
              flag = False
            else:
              flag = True 
        return move
# this method checks if the user entered a move in the correct format 

          
    def __wrong_propiece_input(self, pro_piece, pro_board, piece_number, yTo, xTo, colour):
      flag = False
      while flag == False:
        try:
          pro_board[yTo][xTo] = colour + pro_piece + str(piece_number[colour + pro_piece])
          piece_number[colour + pro_piece] = piece_number[colour + pro_piece] + 1
        except:
          pro_piece = input("the promotion input is not in the correct format, please try again:")
          flag = False
        else:
          flag = True
      return piece_number, pro_board, pro_piece
# this method asks the user to enter which piece they would like to promote to, than the board is changed with the pawn promoted to that piece


    def __find_move(self, move, find_board, newboard):
        for i in range(8):
            for j in range(8):
                if find_board[i][j] != newboard[i][j]:
                    if newboard[i][j] == "___":
                        if (find_board[i][j])[0] != move[0]:
                            xFrom = j
                            yFrom = i
                    else:
                        pro_yTo = i
                        pro_xTo = j
        piece = find_board[yFrom][xFrom]
        if piece[1] == "p" and yFrom == 6:
            yTo, xTo = pro_yTo, pro_xTo
        else:
            yTo, xTo = self.__From(piece, newboard)
        move = (piece + Chess.inverse_Xnotation[xTo] + Chess.inverse_Ynotation[yTo])
        return xFrom, yFrom, xTo, yTo, move
# this method takes an old board and a new board as argument and returns the move that was made 

  
    def __Kcastling(self, Castle_board, fromX, fromY, opposite_colour, colour, Moved_Kside, Moved_Qside, legal):
        Legal = False
        castle_board = self.__Copy(Castle_board)
        if self.__checks(fromY, fromX, castle_board, opposite_colour, colour) == False:
            if Moved_Kside[colour]==False:
                if castle_board[fromY][fromX+1]==castle_board[fromY][fromX+2]=="___" and (castle_board[fromY][fromX+3])[1]=="r":  
                    if self.__checks(fromY, fromX+1, castle_board, opposite_colour, colour) == False:
                        if self.__checks(fromY, fromX+2, castle_board, opposite_colour, colour) == False:
                            castle_board[fromY][fromX+2] = castle_board[fromY][fromX]
                            castle_board[fromY][fromX+1] = castle_board[fromY][fromX+3]
                            castle_board[fromY][fromX] = "___"
                            castle_board[fromY][fromX+3] = "___"
                            Moved_Kside[colour], Moved_Qside[colour] = True, True
                            Legal = True
        if Legal == False:
            legal = False
        return castle_board, legal, Moved_Kside, Moved_Qside


    def __Qcastling(self, Castle_board, fromX, fromY, opposite_colour, colour, Moved_Kside, Moved_Qside, legal):
        Legal = False
        castle_board = self.__Copy(Castle_board)
        if self.__checks(fromY, fromX, castle_board, opposite_colour, colour) == False:
            if Moved_Qside[colour]==False:
                if castle_board[fromY][fromX-1]==castle_board[fromY][fromX-2]==castle_board[fromY][fromX-3]=="___" and (castle_board[fromY][fromX-4])[1]=="r":
                    if self.__checks(fromY, fromX-1, castle_board, opposite_colour, colour) == False:
                        if self.__checks(fromY ,fromX-2, castle_board, opposite_colour, colour) == False:
                            castle_board[fromY][fromX-2] = castle_board[fromY][fromX]
                            castle_board[fromY][fromX-1] = castle_board[fromY][fromX-4]
                            castle_board[fromY][fromX] = "___"
                            castle_board[fromY][fromX-4] = "___"
                            Moved_Kside[colour], Moved_Qside[colour] = True, True
                            Legal = True
        if Legal == False:
            legal = False
        return castle_board, legal, Moved_Kside, Moved_Qside


    def __castle_conditions(self, castle, conditions_board, fromX, fromY, opposite_colour, colour, Moved_Kside, Moved_Qside, legal):
        #castle = input("how would you like to castle (k = king side, q = queen side):")
        while castle != "k" and castle != "q":
            castle = input("the input is not in the correct format, please try again:")
        if castle == "k":
            conditions_board, legal, Moved_Kside, Moved_Qside = self.__Kcastling(conditions_board, fromX, fromY, opposite_colour, colour, Moved_Kside, Moved_Qside, legal)
        elif castle == "q":
            conditions_board, legal, Moved_Kside, Moved_Qside = self.__Qcastling(conditions_board, fromX, fromY, opposite_colour, colour, Moved_Kside, Moved_Qside, legal)
        else:
            legal = False
        if legal == False:
            print ("this move is not legal")
        return conditions_board, legal, Moved_Kside, Moved_Qside    

# the method castle_conditions calls either Qcastling to castle on the queen's side by changing the board or Kcastling to castle king's side by changing the board 

    def __undo(self,prev_move,prev_from,prev_to,prev_prev_move,prev_prev_from,prev_prev_to,prev_moved_Kside,prev_moved_Qside,boards_stack,board,moved_Kside,moved_Qside):
        undo = ""
        while undo != "y" and undo != "n":
            undo = input("Do you want to undo the last two moves. Type y for yes and n for no:")
# ask the user if they want to undo the last two moves
        if undo == "y":
            prev_move = prev_prev_move
            prev_from = prev_prev_from
            prev_to = prev_prev_to
            a = prev_moved_Kside["b"]
            b = prev_moved_Kside["w"]
            c = prev_moved_Qside["b"]
            d = prev_moved_Qside["w"]
            moved_Kside = {"b":a,"w":b}
            moved_Qside = {"b":c,"w":b}
# when undoing moves these are somethings which need their value to be changed back 
            boards_stack.pop()
            boards_stack.pop()
# pop board of the stack when undoing move
            board = self.__Copy(boards_stack[-1])
# change the board back when undoing a move
            self.__output_display(board)
        a = moved_Kside["b"]
        b = moved_Kside["w"]
        c = moved_Qside["b"]
        d = moved_Qside["w"]
        prev_moved_Kside = {"b":a,"w":b}
        prev_moved_Qside = {"b":c,"w":d}
# here I am storing the current values of moved_Kside and moved_Qside into different variables, so when the value of moved_Kside and moved_Qside changes their old values are kept
# the old values are used when undoing moves

        return prev_move, prev_from, prev_to, prev_moved_Kside, prev_moved_Qside, boards_stack, board, moved_Kside, moved_Qside
    
    



    def move_converter(self, move, board):

        if move == "e1g1" and move[0:2] == "e1" and board[Chess.Ynotation[move[1]]][Chess.Xnotation[move[0]]] == "wk0":
            move = "wk0castlek"
        elif move == "e1c1" and move[0:2] == "e1" and board[Chess.Ynotation[move[1]]][Chess.Xnotation[move[0]]] == "wk0":
            move = "wk0castleq"
        elif move == "e8g8" and move[0:2] == "e8" and board[Chess.Ynotation[move[1]]][Chess.Xnotation[move[0]]] == "bk0":
            move = "bk0castlek"
        elif move == "e8c8" and move[0:2] == "e8" and board[Chess.Ynotation[move[1]]][Chess.Xnotation[move[0]]] == "bk0":
            move = "bk0castleq"
        elif move[0] == "7":
            x_from = Chess.Xnotation[move[1]]
            y_from = Chess.Ynotation[move[0]]
            move = board[y_from][x_from] + move[1:]
        else:
            x_from = Chess.Xnotation[move[0]]
            y_from = Chess.Ynotation[move[1]]
            move = board[y_from][x_from] + move[2:]

        return (move)
    

    def lichess_moves(self, move, x_From, y_From, xTo, yTo, client, game_id):
        lichess_x_from = Chess.inverse_Xnotation[x_From]
        lichess_y_from = Chess.inverse_Ynotation[y_From]
        lichess_move = lichess_x_from + lichess_y_from + move[3:]
        
        if move[0:2] == "wp" and yTo == 0 or move[0:2] == "bp" and yTo == 7:
            lichess_move = lichess_move + "q"
        print (lichess_move)
        client.bots.make_move(game_id, lichess_move)

    
    
    
    
      
    def game_loop(self, stream, client, game_id):
        analyse = ""
        board = self.__Copy(self.board)
        piece_number = {"wn":2, "wb":2, "wr":2, "wq":1, "bn":2, "bb":2, "br":2, "bq":1}
        boards_stack =[self.__Copy(board)]
        moved_Kside = {"b":False, "w":False}
        moved_Qside = {"b":False, "w":False}
        prev_moved_Kside = {"b":False, "w":False}
        prev_moved_Qside = {"b":False, "w":False}
        prev_move = "b_"
        prev_from = [9,9]
        prev_to = [9,9]
        prev_prev_move = "b_"
        prev_prev_from = [9,9]
        prev_prev_to = [9,9]
# these are some things that need to be defined before the main code runs 

        self.__output_display(board)
# output the display  


        counter = 0

        for event2 in stream:
            if event2['type'] == 'gameState':
                if counter%2 == 0:
                    move = (event2['moves'])[-4:]
                    print (move)
                    move = self.move_converter(move, board)

                    prev_board = self.__Copy(board)
        # copy board to prev_board so that any changes mede to board can be reversed by coping prev_board to board
                    legal = True 
                    yFrom, xFrom = self.__From(move[0:3], board)
                    if xFrom == "":
                        legal = False
                        print ("this piece is not on the board")
                    elif move[0] == prev_move[0]:
                        legal = False
                        print ("wrong colour")
        # if the colour of the piece the user is trying to move is the same as the colour of the piece that was moved previously than the user is trying to move a piece of the wrong colour 
                    elif move[3:9] == "castle":
                        if move[1] == "k":
                            board, legal, moved_Kside, moved_Qside = self.__castle_conditions(move[-1], board, xFrom, yFrom, prev_move[0], move[0], moved_Kside, moved_Qside, legal)
                        else:
                            print ("only the king can castle")
                            legal = False
        # this allows the user to castle if they can 
                    else:
                        yTo = Chess.Ynotation[move[4]]
                        xTo = Chess.Xnotation[move[3]]
                        if str(xTo) + str(yTo) ==  (self.objects[move[0]+"p"]).en_passant_conditions(xFrom, yFrom, prev_from[1], prev_to[0], prev_to[1]) and move[1] == prev_move[1] == "p":
                            board = (self.objects[move[0]+"p"]).new_en_passant_board(board, xFrom, yFrom, xTo, yTo, prev_to[0], prev_to[1])
        # this allows the user to en-passant if they can 
                        elif  str(xTo) + str(yTo) not in (self.objects[move[0:2]]).legal_moves(xFrom, yFrom, move[0], board):
                            legal = False
                            print ("this move is not legal")
        # if the move isn't catsle or en-passant, and not in a list of possible moves for the chosen piece than the move illegal 
                        else:
                            board = self.__oldboard_to_newboard(board, xFrom, yFrom, xTo, yTo)
        # if none of the obove conditions are met than the board is changed in the standard way 
                            if move[0:2] == "wp" and yTo == 0 or move[0:2] == "bp" and yTo == 7:
                                piece_number, board, pro_piece = self.__wrong_propiece_input(move[5], board, piece_number, yTo, xTo, move[0])
        # if a pawn got to the end than it is promoted 
                            moved_Kside, moved_Qside = self.__moved(move, moved_Kside, moved_Qside)
        # this part checks if the king or any of the rooks have moved because you can't castle later when they have moved
                    pieces_positions, king1, king2 = self.__positions(board, prev_move[0])
                    if self.__checks(int(king2[1]), int(king2[0]), board, prev_move[0], move[0]) == True:
                        print ("you are in check")
                        board = self.__Copy(prev_board)
        # this part checks if the user is in check after making that move, if yes than the changes to the board are undone 
                    elif legal == True:
                        self.__output_display(board)
                        print ("the total score is", self.__total_score(board))
        # output the display and the total score
                        self.__gameover_output(board, move, prev_move, yFrom, xTo, yTo, pieces_positions, int(king1[0]), int(king1[1]), boards_stack)
        # this part sees if the game has ended either by a win, loss or a draw 
                        boards_stack.append(self.__Copy(board))
        # every time the board changes it is pushed into a stack
                        if move[0] == "w":
                            prev_prev_move = prev_move
                            prev_prev_from = prev_from
                            prev_prev_to = prev_to
                        prev_move = move
        # the current values of these data structures are stored so these values can be used even after the data structures have been updated

                        if self.__mode == "analyse" and move[0] == "w":
                            analyse = ""
                            while analyse != "y" and analyse != "n":
                                analyse = input("Do you want to see next suggested move. Type y for yes and n for no:")
                            if analyse == "y": 
                                difficulty = ""
                                while difficulty != "1" and difficulty != "2" and difficulty != "3":
                                    difficulty  = input("Choose analysis strength between 1 and 3, where 3 is strongest (but is might take over a minute):")
                                self.__difficulty = difficulty
        # does the user want to see which move the AI would play in this position (if analysis was chose)

                        if self.__mode == "1" or analyse == "y":
                            if self.__game_over == False:
        # if the user chose to play against the AI than the next block of code is executed if the game hasn't ended
                                print ("processing...")
                                start_time = time.time()
        # starts the timer to see how long the AI takes to generate a move
                                newboard = self.__chess_AI(board, moved_Kside, moved_Qside, yFrom, xTo, yTo, move[0:3], piece_number, pieces_positions)
        # the method which will pick a move to play against the user is called and the move is returned in new board
                                pieces_positions, king1, king2 = self.__positions(newboard, move[0])
        # position of the kings and the other pieces need to be found for when game_over_output is called 
                                xFrom, yFrom, xTo, yTo, move = self.__find_move(move, board, newboard)
                                self.lichess_moves(move, xFrom, yFrom, xTo, yTo, client, game_id)
        # the move and somethings about the move are found so that they can later be stored in previous move, previous from and so on 
                                moved_Kside, moved_Qside = self.__moved(move, moved_Kside, moved_Qside)
        # check if the king or the rooks have moved 
                                print ("")
                                board = self.__Copy(newboard)
        # new board is copied to board only now because the values of both board and new board were needed to find the move
                                self.__output_display(board)
                                print ("the total score is", self.__total_score(board))
        # the board is outputed wiht the total score
                                self.__gameover_output(board , move, prev_move, yFrom, xTo, yTo, pieces_positions, int(king1[0]), int(king1[1]), boards_stack)
        # this part calls a method which checks if the game has ended or not
                                prev_move = move
                                prev_from, prev_to = [xFrom, yFrom], [xTo, yTo]
        # previous variables are defined for the next loop 
                                boards_stack.append(self.__Copy(board))
        # every time the board changes it is pushed into a stack
                                print ("AI took", time.time() - start_time, "seconds")
        # the timer is stopped and the time is outputed
                            else:
                                sys.exit()
                        else:
        # next section is executed if the user chose to play 2 player mode
                            if move[3:] != "castle":
                                prev_from, prev_to = [xFrom, yFrom], [xTo, yTo]
        # some things that need to be updated for the next loop 
                counter += 1

            

class Piece:
    def __init__(self, vectors, value):
        self._vectors = vectors
        self.__value = value
# vectors contain a list of vectors used to simulate a move of a chess piece and value contains its relative worth

    def get_value(self):
        return self.__value
# getter method to give access to protected attribute value

    def legal_moves(self, fromX, fromY, colour, legal_board):
# fromX and fromY contain the original position of a chess piece, colour contains the colour of that piece and legal_board contains the current layout of the chessboard 

        all_moves = []
        for i in self._vectors:
                Xmove = fromX
                Ymove = fromY
                XYmove = "___"

                while 0 <= Xmove < 8 and 0 <= Ymove < 8 and XYmove[0] == "_":
                        Xmove = Xmove + int(i[0:2])
                        Ymove = Ymove + int(i[2:4])
                        
                        if 0 <= Xmove < 8 and 0 <= Ymove < 8:
                            XYmove = legal_board[Ymove][Xmove]
                            if XYmove[0] != colour:
                                all_moves.append(str(Xmove) + str(Ymove))
        return all_moves
# this method generates a list of all possible moves for a chess piece that moves in a line (bishop, rook and queen)
# inner while loop repeatably adds a vector to the original position of a chess piece to simulate it moving in a line and the outer for loop repeats this for all vectors for that piece 


class PointMovingPiece(Piece):
    def legal_moves(self, fromX, fromY, colour, legal_board):
        all_moves = []
        for i in self._vectors:
                Xmove = fromX + int(i[0:2])
                Ymove = fromY + int(i[2:4])

                if 0 <= int(Xmove) < 8 and 0 <= int(Ymove) < 8 and (legal_board[Ymove][Xmove])[0] != colour:
                    all_moves.append(str(Xmove) + str(Ymove))
        return all_moves
# this method is the same as the legal_moves method from the class Pieces but for pieces that move only to specific points (king, knight) and therefore doesnt need the inner while loop 

    
class Pawn(Piece):
    def legal_moves(self, fromX, fromY, colour, legal_board):
        all_moves = []
        for i in range(len(self._vectors)):
                Xmove = (fromX + int((self._vectors[i])[0:2]))
                Ymove = (fromY + int((self._vectors[i])[2:4]))
                
                if 0 <= int(Xmove) < 8 and 0 <= int(Ymove) < 8:
                    XYmove = legal_board[Ymove][Xmove]
                    if colour=="w" and fromY==6 and legal_board[Ymove+1][Xmove]=="___" or colour=="b" and fromY==1 and legal_board[Ymove-1][Xmove]=="___":
                        if i==1 and XYmove=="___":
                            all_moves.append(str(Xmove) + str(Ymove))
                    if i == 0 and XYmove == "___" or XYmove != "___" and XYmove[0] != colour and i > 1:
                        all_moves.append(str(Xmove) + str(Ymove))
        return  all_moves
# this method is similar to the legal_moves method from class PointMovingPieces but with some more conditions because the rules for how pawns move are more complex

    def en_passant_conditions(self, fromX, fromY, prevFromY, prevToX, prevToY):
        en_passant = ""
        if prevToX==fromX+1 and prevToY==fromY and prevFromY-int((self._vectors[1])[2:4])==prevToY:
            en_passant = str(fromX + int((self._vectors[3])[0:2])) + str(fromY + int((self._vectors[3])[2:4]))
        if prevToX==fromX-1 and prevToY==fromY and prevFromY-int((self._vectors[1])[2:4])==prevToY:
            en_passant = str(fromX + int((self._vectors[2])[0:2])) + str(fromY + int((self._vectors[2])[2:4]))
        return en_passant
# this method contains the conditions needed for en_passant to be carried out and if they are met the move is stores in variable en_passant 

    def new_en_passant_board(self, old_board, fromX, fromY, toX, toY, prevToX, prevToY):
        old_board[toY][toX] = old_board[fromY][fromX]
        old_board[fromY][fromX] = "___"
        old_board[prevToY][prevToX] = "___"
        return old_board  
# this method changes the board to carry out en-passant 

initial_position = [["br0","bn0","bb0","bq0","bk0","bb1","bn1","br1"],
                    ["bp1","bp2","bp3","bp4","bp5","bp6","bp7","bp8"],
                    ["___","___","___","___","___","___","___","___"],
                    ["___","___","___","___","___","___","___","___"],
                    ["___","___","___","___","___","___","___","___"],
                    ["___","___","___","___","___","___","___","___"],
                    ["wp1","wp2","wp3","wp4","wp5","wp6","wp7","wp8"],
                    ["wr0","wn0","wb0","wq0","wk0","wb1","wn1","wr1"]]



# this 2D list represents the chessboard


Game = Chess(initial_position, "1", "2")
# Game is an object with atributes: initial position of the chess pieces on the board, game mode(1 or 2 player or analyse) and the difficulty

token = ""

session = berserk.TokenSession(token)

client = berserk.Client(session)


for event1 in client.bots.stream_incoming_events():
    if event1['type'] == 'gameStart':
        game = event1['game']
        game_id = game['gameId']
        stream = client.bots.stream_game_state(game_id)
        Game.game_loop(stream, client, game_id)
    

       
















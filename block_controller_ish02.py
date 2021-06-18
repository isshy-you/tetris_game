#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pprint
import copy
import random

class Block_Controller(object):

    # init parameter
    board_backboard = 0
    board_data_width = 0
    board_data_height = 0
    ShapeNone_index = 0
    CurrentShape_class = 0
    NextShape_class = 0

    # GetNextMove is main function.
    # input
    #    nextMove : nextMove structure which is empty.
    #    GameStatus : block/field/judge/debug information. 
    #                 in detail see the internal GameStatus data.
    # output
    #    nextMove : nextMove structure which includes next shape position and the other.
    def GetNextMove(self, nextMove, GameStatus):

        t1 = datetime.now()

        # print GameStatus
        print("=================================================>")
        pprint.pprint(GameStatus, width = 61, compact = True)

        # get data from GameStatus
        # current shape info
        CurrentShapeDirectionRange = GameStatus["block_info"]["currentShape"]["direction_range"]
        self.CurrentShape_class = GameStatus["block_info"]["currentShape"]["class"]
        self.CurrentShape_index = GameStatus["block_info"]["currentShape"]["index"]
        # next shape info
        NextShapeDirectionRange = GameStatus["block_info"]["nextShape"]["direction_range"]
        self.NextShape_class = GameStatus["block_info"]["nextShape"]["class"]
        # current board info
        self.board_backboard = GameStatus["field_info"]["backboard"]
        # default board definition
        self.board_data_width = GameStatus["field_info"]["width"]
        self.board_data_height = GameStatus["field_info"]["height"]
        self.ShapeNone_index = GameStatus["debug_info"]["shape_info"]["shapeNone"]["index"]

        # search best nextMove -->
        strategy = None
        LatestEvalValue = -100000
        # add additional code by isshy-you

        # search with x range
        EvalValue,x0,direction0 = self.calcEvaluationValuePAT1(self.board_backboard)
        if EvalValue > 0 :
            strategy = (direction0,x0,1,1)
            LatestEvalValue = EvalValue
        print("<<< isshy-you:(EvalValue,shape,strategy)=(",LatestEvalValue,self.CurrentShape_index,strategy,")")

        # sample code
        # search with current block Shape
        for direction0 in CurrentShapeDirectionRange:
            # search with x range
            x0Min, x0Max = self.getSearchXRange(self.CurrentShape_class, direction0)
            for x0 in range(x0Min, x0Max):
                # get board data, as if dropdown block
                board = self.getBoard(self.board_backboard, self.CurrentShape_class, direction0, x0)

                # evaluate board
                EvalValue = self.calcEvaluationValueSample(board)
                # update best move
                if EvalValue > LatestEvalValue:
                    print(">>> SAMPLE (EvalValue,shape,strategy)=(",EvalValue,self.CurrentShape_index,(direction0, x0, 1, 1),")")
                    strategy = (direction0, x0, 1, 1)
                    LatestEvalValue = EvalValue

        # search best nextMove <--

        print("===  processing time  ===(", datetime.now() - t1,")")
        print("=== (EvalValue,shape,strategy)=( ",LatestEvalValue,self.CurrentShape_index,strategy,")")
        nextMove["strategy"]["direction"] = strategy[0]
        nextMove["strategy"]["x"] = strategy[1]
        nextMove["strategy"]["y_operation"] = strategy[2]
        nextMove["strategy"]["y_moveblocknum"] = strategy[3]
        print("=== nextMove:",nextMove)
        print("###### ISH02(ALPHA:12553/9166/2789) w/SAMPLE CODE ######")
        return nextMove

        
    def getSearchXRange(self, Shape_class, direction):
        #
        # get x range from shape direction.
        #
        minX, maxX, _, _ = Shape_class.getBoundingOffsets(direction) # get shape x offsets[minX,maxX] as relative value.
        xMin = -1 * minX
        xMax = self.board_data_width - maxX
        return xMin, xMax

    def getShapeCoordArray(self, Shape_class, direction, x, y):
        #
        # get coordinate array by given shape.
        #
        coordArray = Shape_class.getCoords(direction, x, y) # get array from shape direction, x, y.
        return coordArray

    def getBoard(self, board_backboard, Shape_class, direction, x):
        # 
        # get new board.
        #
        # copy backboard data to make new board.
        # if not, original backboard data will be updated later.
        board = copy.deepcopy(board_backboard)
        _board = self.dropDown(board, Shape_class, direction, x)
        return _board

    def dropDown(self, board, Shape_class, direction, x):
        # 
        # internal function of getBoard.
        # -- drop down the shape on the board.
        # 
        dy = self.board_data_height - 1
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        # update dy
        for _x, _y in coordArray:
            _yy = 0
            while _yy + _y < self.board_data_height and (_yy + _y < 0 or board[(_y + _yy) * self.board_data_width + _x] == self.ShapeNone_index):
                _yy += 1
            _yy -= 1
            if _yy < dy:
                dy = _yy
        # get new board
        _board = self.dropDownWithDy(board, Shape_class, direction, x, dy)
        return _board

    def dropDownWithDy(self, board, Shape_class, direction, x, dy):
        #
        # internal function of dropDown.
        #
        _board = board
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        for _x, _y in coordArray:
            _board[(_y + dy) * self.board_data_width + _x] = Shape_class.shape
        return _board

    def calcEvaluationValuePAT1(self,board):
        score = -10000
        direction = 0
        x0 = 0
        width = self.board_data_width #width=10
        height = self.board_data_height #height=22
        dic_pat1 = {0x0ff:0,0x0f7:0,0x0f3:0,0x0f1:0,0x0f0:0, \
                    0x07f:0,0x077:0,0x073:0,0x071:0,0x070:0}
#        dic_pat1 = {0x0ff:0,0x0f7:0,0x0f3:0,0x0f1:0,0x0f0:0,\
#                    0x07f:0,0x077:0,0x073:0,0x071:0,0x070:0,\
#                    0x03f:0,0x037:0,0x033:0,0x031:0,0x030:0}
        dic_pat2 = {0x011:1,0x003:0,0x001:0,0x007:0,\
                    0x30f:2,0x307:2,0x303:2,0x301:2,0x300:2,\
                    0x000:3}
        dic_pat3 = {0x110:3,\
                    0x00f:0,0x007:0,0x003:0,0x001:0,\
                    0x030:2,0x031:2,0x033:2,0x037:2,0x03f:2,\
                    0x000:1}
        dic_pat4 = {0x101:1,\
                    0x010:0,0x011:0,0x013:0,0x017:0,0x01f:0,\
                    0x100:2,0x101:2,0x103:2,0x107:2,0x10f:2,\
                    0x000:3}
        dic_pat5 = {0x003:0,0x007:0,0x00f:0,0x001:0,0x000:0,0x110:0}
        dic_pat6 = {0x001:0,0x100:1,0x101:1,0x103:1,0x107:1,0x10f:1}
        dic_pat7 = {0x100:0,0x010:1,0x011:1,0x013:1,0x017:1,0x01f:1}

#       if random.randrange(2)==0:
#            print("%%%% RANDOM==0 %%%%")
#            x_start = 0
#            x_end = width-1
#            x_step = 1
#        else:
#            print("%%%% RANDOM==1 %%%%")
#            x_start = width-1
#            x_end = 0
#            x_step = -1

        x_start = 0
        x_end = width-1
        x_step = 1
        for x in range(x_start,x_end,x_step):
            for y in range(height - 4, 0, -1):
                if x > (width-1) :
                    pat0=15
                else:
                    pat0=0
                    if board[y * width + x]!=0:
                        pat0 += 8
                    if board[(y+1) * width + x]!=0:
                        pat0 += 4
                    if board[(y+2) * width + x]!=0:
                        pat0 += 2
                    if y > (height-4):
                        pat0 += 1
                    elif board[(y+3) * width + x]!=0:
                        pat0 += 1

                    if pat0==0 and y<(height-4) and self.CurrentShape_index!=1:
                        if board[(y+4) * width + x]==0:
                            pat0 = 16
                            
                if x > (width-2) :
                    pat1=15
                else:
                    pat1=0
                    if board[y * width + (x + 1)]!=0:
                        pat1 += 8
                    if board[(y+1) * width + (x + 1)]!=0:
                        pat1 += 4
                    if board[(y+2) * width + (x + 1)]!=0:
                        pat1 += 2
                    if y > (height-4):
                        pat1 += 1
                    elif board[(y+3) * width + (x + 1)]!=0:
                        pat1 += 1

                    if pat1==0 and y<(height-4) and self.CurrentShape_index!=1:
                        if board[(y+4) * width + (x + 1)]==0:
                            pat1 = 16

                if x > (width-3) :
                    pat2=15
                else:
                    pat2=0
                    if board[y * width + (x + 2)]!=0:
                        pat2 += 8
                    if board[(y+1) * width + (x + 2)]!=0:
                        pat2 += 4
                    if board[(y+2) * width + (x + 2)]!=0:
                        pat2 += 2
                    if y > (height-4):
                        pat2 += 1
                    elif board[(y+3) * width + (x + 2)]!=0:
                        pat2 += 1

                    if pat2==0 and y<(height-4) and self.CurrentShape_index!=1 and self.CurrentShape_index!=5:
                    #if pat2==0 and y<(height-4) and self.CurrentShape_index!=1:
                        if board[(y+4) * width + (x + 2)]==0:
                            pat2 = 16

                #matching

                if pat0!=16 and pat1!=16 and pat2!=16 :
                    pat = pat0*256+pat1*16+pat2
                    #DEBUG
                    #print("(shape,x,y,pat)=(",self.CurrentShape_index,x,y,format(pat,'03x'),")")
                else:
                    pat = 0xfff
                    
                if self.CurrentShape_index==1 :
                    if pat in dic_pat1:
                        direction = dic_pat1[pat]
                        for yy in range(height - 4, y, -1):
                             if board[(yy) * width + (x)] != 0:
                                 break
                        score = 19
                        x0 = x
                        print("(shape,x0,x,y,direction,pat)=(",self.CurrentShape_index,x0,x,y,direction,format(pat,'03x'),")")
                        break
                if self.CurrentShape_index==2 :
                    if pat in dic_pat2:
                        direction = dic_pat2[pat]
                        score = 19
                        if direction==0:
                            x0 = x
                        elif direction==1 or direction==2 or direction==3:
                            x0 = x+1
                        else:
                            x0 = x
                        print("(shape,x0,x,y,direction,pat)=(",self.CurrentShape_index,x0,x,y,direction,format(pat,'03x'),")")
                        break
                if self.CurrentShape_index==3 :
                    if pat in dic_pat3:
                        direction = dic_pat3[pat]
                        score = 19
                        if direction==0 or direction==1 or direction==3:
                            x0 = x+1
                        else:
                            x0 = x
                        print("(shape,x0,x,y,direction,pat)=(",self.CurrentShape_index,x0,x,y,direction,format(pat,'03x'),")")
                        break
                if self.CurrentShape_index==4 :
                    if pat in dic_pat4:
                        direction = dic_pat4[pat]
                        score = 19
                        if direction==2 or direction==3:
                            x0 = x+1
                        else:
                            x0 = x
                        print("(shape,x0,x,y,direction,pat)=(",self.CurrentShape_index,x0,x,y,direction,format(pat,'03x'),")")
                        break
                if self.CurrentShape_index==5 :
                    if pat in dic_pat5:
                        direction = dic_pat5[pat]
                        score = 19
                        x0 = x+0
                        print("(shape,x0,x,y,direction,pat)=(",self.CurrentShape_index,x0,x,y,direction,format(pat,'03x'),")")
                        break
                if self.CurrentShape_index==6 :
                    if pat in dic_pat6:
                        direction = dic_pat6[pat]
                        score = 19
                        if direction==0 :
                            x0 = x+1
                        else:
                            x0 = x
                        print("(shape,x0,x,y,direction,pat)=(",self.CurrentShape_index,x0,x,y,direction,format(pat,'03x'),")")
                        break
                if self.CurrentShape_index==7 :
                    if pat in dic_pat7:
                        direction = dic_pat7[pat]
                        score = 19
                        if direction==0:
                            x0 = x+1
                        else:
                            x0 = x
                        print("(shape,x0,x,y,direction,pat)=(",self.CurrentShape_index,x0,x,y,direction,format(pat,'03x'),")")
                        break

                if score > 18 :
                    break                    
        #            
        return score,x0,direction

        
    def calcEvaluationValueSample(self, board):
        #
        # sample function of evaluate board.
        #
        width = self.board_data_width
        height = self.board_data_height

        # evaluation paramters
        ## lines to be removed
        fullLines = 0
        ## number of holes or blocks in the line.
        nHoles, nIsolatedBlocks = 0, 0
        ## absolute differencial value of MaxY
        absDy = 0
        ## how blocks are accumlated
        BlockMaxY = [0] * width
        holeCandidates = [0] * width
        holeConfirm = [0] * width

        ### check board
        # each y line
        for y in range(height - 1, 0, -1):
            hasHole = False
            hasBlock = False
            # each x line
            for x in range(width):
                ## check if hole or block..
                if board[y * self.board_data_width + x] == self.ShapeNone_index:
                    # hole
                    hasHole = True
                    holeCandidates[x] += 1  # just candidates in each column..
                else:
                    # block
                    hasBlock = True
                    BlockMaxY[x] = height - y                # update blockMaxY
                    if holeCandidates[x] > 0:
                        holeConfirm[x] += holeCandidates[x]  # update number of holes in target column..
                        holeCandidates[x] = 0                # reset
                    if holeConfirm[x] > 0:
                        nIsolatedBlocks += 1                 # update number of isolated blocks

            if hasBlock == True and hasHole == False:
                # filled with block
                fullLines += 1
            elif hasBlock == True and hasHole == True:
                # do nothing
                pass
            elif hasBlock == False:
                # no block line (and ofcourse no hole)
                pass

        # nHoles
        for x in holeConfirm:
            nHoles += abs(x)

        ### absolute differencial value of MaxY
        BlockMaxDy = []
        for i in range(len(BlockMaxY) - 1):
            val = BlockMaxY[i] - BlockMaxY[i+1]
            BlockMaxDy += [val]
        for x in BlockMaxDy:
            absDy += abs(x)

        #### maxDy
        #maxDy = max(BlockMaxY) - min(BlockMaxY)
        #### maxHeight
        #maxHeight = max(BlockMaxY) - fullLines

        ## statistical data
        #### stdY
        #if len(BlockMaxY) <= 0:
        #    stdY = 0
        #else:
        #    stdY = math.sqrt(sum([y ** 2 for y in BlockMaxY]) / len(BlockMaxY) - (sum(BlockMaxY) / len(BlockMaxY)) ** 2)
        #### stdDY
        #if len(BlockMaxDy) <= 0:
        #    stdDY = 0
        #else:
        #    stdDY = math.sqrt(sum([y ** 2 for y in BlockMaxDy]) / len(BlockMaxDy) - (sum(BlockMaxDy) / len(BlockMaxDy)) ** 2)


        # calc Evaluation Value
        score = 0
        score = score + fullLines * 10.0           # try to delete line 
        score = score - nHoles * 1.0               # try not to make hole
        score = score - nIsolatedBlocks * 1.0      # try not to make isolated block
        score = score - absDy * 1.0                # try to put block smoothly
        #score = score - maxDy * 0.3                # maxDy
        #score = score - maxHeight * 5              # maxHeight
        #score = score - stdY * 1.0                 # statistical data
        #score = score - stdDY * 0.01               # statistical data

        # print(score, fullLines, nHoles, nIsolatedBlocks, maxHeight, stdY, stdDY, absDy, BlockMaxY)
        return score

BLOCK_CONTROLLER = Block_Controller()


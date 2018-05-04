import copy;

class GameState(object):
	N=8;
	def __init__(self,board,starWeight,circleWeight,player):
		self.board=board;
		self.starWeight=starWeight;
		self.circleWeight=circleWeight;
		self.player=player;
		self.starCount=0;
		self.circleCount=0;
		self.setCount();

	def setCount(self):
		star,circle=0,0;
		for i in range(self.N):
			for j in range(self.N):
				curr=self.board[i][j];
				if curr[0]=='S':
					self.starCount+=int(curr[1]);
				elif curr[0]=='C':
					self.circleCount+=int(curr[1]);

	def calculateUtility(self):
		star,circle=0,0;
		for i in range(self.N):
			for j in range(self.N):
				curr=self.board[i][j];
				if curr[0]=='S':
					star+=(int(curr[1])*self.starWeight[i]);
				elif curr[0]=='C':
					circle+=(int(curr[1])*self.circleWeight[i]);
		if self.player=='Star':
			return star-circle;
		else:
			return circle-star;

class Checkers(object):

	MIN_VALUE = -2147483648;
	MAX_VALUE = 2147483647;
	N=8;
	result={ "move":[], "utility":MIN_VALUE,"myopicUtility":MIN_VALUE ,"farsightedUtility":MIN_VALUE, "nodes":1 };
	def getMaxValue(self,checkers,alpha,beta,currDepth,player,isPass1,isPass2,isAlphaBeta):
		playerUtility={"utility":self.MIN_VALUE,"farsightedUtility":0};

		self.result["nodes"]=self.result["nodes"]+1;

		if currDepth>=self.maxDepth or self.isTerminal(checkers):
			playerUtility["utility"]=checkers.calculateUtility();
			playerUtility["farsightedUtility"]=playerUtility["utility"];
			return playerUtility;
	
		moves=self.getAllMoves(checkers,player);
		
		if len(moves)==0:
			if isPass1:
				if isPass2:
					playerUtility["utility"]=checkers.calculateUtility();
					playerUtility["farsightedUtility"]=playerUtility["utility"];
					return playerUtility;
				else:
					isPass2=True;
			isPass1=True;
			return self.getMinValue(checkers,alpha,beta,currDepth+1,self.reverse(player),isPass1,isPass2,isAlphaBeta);

		for m in moves:
			new_checkers=self.executeMove(checkers,m);
			minVal=self.getMinValue(new_checkers,alpha,beta,currDepth+1,self.reverse(player),False,False,isAlphaBeta);
		
			if minVal["utility"]>playerUtility["utility"]:
				playerUtility["utility"]=minVal["utility"];
				playerUtility["farsightedUtility"]=minVal["farsightedUtility"];
			
			if isAlphaBeta:
				if playerUtility["utility"]>=beta:
					return playerUtility;
			
			alpha=max(alpha,playerUtility["utility"]);
	
		return playerUtility;
	
	def getMinValue(self,checkers,alpha,beta,currDepth,player,isPass1,isPass2,isAlphaBeta):
		playerUtility={"utility":self.MAX_VALUE,"farsightedUtility":0};
		
		self.result["nodes"]=self.result["nodes"]+1;
		
		if currDepth>=self.maxDepth or self.isTerminal(checkers):
			playerUtility["utility"]=checkers.calculateUtility();
			playerUtility["farsightedUtility"]=playerUtility["utility"];
			return playerUtility;
	
		moves=self.getAllMoves(checkers,player);
		
		if len(moves)==0:
			if isPass1:
				if isPass2:
					playerUtility["utility"]=checkers.calculateUtility();
					playerUtility["farsightedUtility"]=playerUtility["utility"];
					return playerUtility;
				else:
					isPass2=True;
			isPass1=True;
			return self.getMaxValue(checkers,alpha,beta,currDepth+1,self.reverse(player),isPass1,isPass2,isAlphaBeta);
	
		for m in moves:
			new_checkers=self.executeMove(checkers,m);
			maxVal=self.getMaxValue(new_checkers,alpha,beta,currDepth+1,self.reverse(player),False,False,isAlphaBeta);
		
			if maxVal["utility"]<playerUtility["utility"]:
				playerUtility["utility"]=maxVal["utility"];
				playerUtility["farsightedUtility"]=maxVal["farsightedUtility"];
			
			if isAlphaBeta:
				if playerUtility["utility"]<=alpha:
					return playerUtility;
			
				beta=min(playerUtility["utility"],beta);

		return playerUtility;
	
	def playCheckers(self,checkers,alpha,beta,currDepth,player,isPass1,isPass2,isAlphaBeta):
		moves=self.getAllMoves(checkers,player);
		if len(moves)==0:
			isPass1=True;
			self.result["move"]=[-1,-1,-1,-1];
			self.result["utility"]=checkers.calculateUtility();
			self.result["myopicUtility"]=self.result["utility"];
			minVal=self.getMinValue(checkers,alpha,beta,currDepth+1,self.reverse(player),isPass1,isPass2,isAlphaBeta);
			self.result["farsightedUtility"]=minVal["farsightedUtility"];

		for m in moves:
			new_checkers=self.executeMove(checkers,m);
			minVal=self.getMinValue(new_checkers,alpha,beta,currDepth+1,self.reverse(player),False,False,isAlphaBeta);
		
			if minVal["utility"]>self.result["utility"]:
				self.result["move"]=m;
				self.result["utility"]=minVal["utility"];
				self.result["myopicUtility"]=new_checkers.calculateUtility();
				self.result["farsightedUtility"]=minVal["farsightedUtility"];

			if isAlphaBeta:
				if self.result["utility"]>=beta:
					return;			
				alpha=max(alpha,self.result["utility"]);

	def reverse(self,player):
		if player=='Star':
			return 'Circle';
		return 'Star';
	
	def getAllMoves(self,checkers,player):
		if player=='Star':
			check='S';
		else:
			check='C';
			
		moves=[];
		for i in range(self.N):
		    for j in range(self.N):
		        currCell=checkers.board[i][j];
		        if currCell[0]==check:
		            self.getValidMoves(i,j,checkers.board,moves,player);
		
		return moves;
	
	def getValidMoves(self,i,j,board,moves,player):
		if player=='Star':
			if i-2>=0 and j-2>=0:
				jumpcell=board[i-2][j-2];
				adjcell=board[i-1][j-1];
				if adjcell[0]=='C' and (jumpcell[0]=='0' or (i-2==0 and jumpcell[0]=='S')):
					moves.append([i,j,i-2,j-2]);
						
			if i-2>=0 and j+2<=7:
				jumpcell=board[i-2][j+2];
				adjcell=board[i-1][j+1];
				if adjcell[0]=='C' and (jumpcell[0]=='0' or (i-2==0 and jumpcell[0]=='S')):
					moves.append([i,j,i-2,j+2]);
					
			if i-1>=0 and j-1>=0:
				adjcell=board[i-1][j-1];
				if adjcell[0]=='0' or (i-1==0 and adjcell[0]=='S'):
					moves.append([i,j,i-1,j-1]);
			
			if i-1>=0 and j+1<=7:
				adjcell=board[i-1][j+1];
				if adjcell[0]=='0' or (i-1==0 and adjcell[0]=='S'):
					moves.append([i,j,i-1,j+1]);
			
		else:
			if i+1<=7 and j-1>=0:
				adjcell=board[i+1][j-1];
				if adjcell[0]=='0' or (i+1==7 and adjcell[0]=='C'):
					moves.append([i,j,i+1,j-1]);
				
			if i+1<=7 and j+1<=7:
				adjcell=board[i+1][j+1];
				if adjcell[0]=='0' or (i+1==7 and adjcell[0]=='C'):
					moves.append([i,j,i+1,j+1]);
				
			if i+2<=7 and j-2>=0:
				jumpcell=board[i+2][j-2];
				adjcell=board[i+1][j-1];
				if adjcell[0]=='S' and (jumpcell[0]=='0' or (i+2==7 and jumpcell[0]=='C')):
					moves.append([i,j,i+2,j-2]);
				
			if i+2<=7 and j+2<=7:
				jumpcell=board[i+2][j+2];
				adjcell=board[i+1][j+1];
				if adjcell[0]=='S' and (jumpcell[0]=='0' or (i+2==7 and jumpcell[0]=='C')):
					moves.append([i,j,i+2,j+2]);
						
	def executeMove(self,checkers,move):
		new_board=copy.deepcopy(checkers.board);
		newPos=new_board[move[2]][move[3]];
		oldPos=new_board[move[0]][move[1]];

		if newPos[0]=='0':
		    new_board[move[2]][move[3]]=oldPos;
		else:
		    new_board[move[2]][move[3]]=newPos[0]+str(int(newPos[1])+1);
		new_board[move[0]][move[1]]='0';
		if int(abs(move[0]-move[2]))==2:
		    new_board[int((move[0]+move[2])/2)][int((move[1]+move[3])/2)]='0';
		
		return GameState(new_board,checkers.starWeight,checkers.circleWeight,checkers.player);

	def isTerminal(self,checkers):
		if checkers.starCount == 0 or checkers.circleCount == 0:
			return True;
		return False;

	def main(self):
		inputFile = open('input.txt', 'r');
		
		#Read input File
		self.mainPlayer=inputFile.readline().rstrip('\n');
		algorithm=inputFile.readline().rstrip('\n');
		self.maxDepth=int(inputFile.readline().rstrip('\n'));
		self.initialBoard=[];
		for i in range(self.N):
			line=inputFile.readline().rstrip('\n');
			self.initialBoard.append(line.split(","));

		line=inputFile.readline().rstrip('\n');
		weight=[int(x) for x in line.split(",")];
		self.circleWeight=weight;
		self.starWeight=list(reversed(weight));

		#Initial state of game
		checkerObj=GameState(self.initialBoard,self.starWeight,self.circleWeight,self.mainPlayer);

		#Start the algorithm
		nextMove=self.playCheckers(checkerObj,self.MIN_VALUE,self.MAX_VALUE,0,self.mainPlayer,False,False,algorithm == 'ALPHABETA');

		#Move calculation
		output_move='';
		temp=self.result["move"];
		if temp[0] == -1:
			output_move+='pass';
		else:
			output_move+=chr(72-temp[0]);
			output_move+=str(temp[1]+1)
			output_move+="-";
			output_move+=chr(72-temp[2]);
			output_move+=str(temp[3]+1);

		#Write the output file
		output_file = open("output.txt", "w");
		output_file.write(output_move+"\n");
		output_file.write(str(self.result["myopicUtility"])+"\n");
		output_file.write(str(self.result["farsightedUtility"])+"\n");
		output_file.write(str(self.result["nodes"]));
		output_file.close();

		  
checkerObj=Checkers();
checkerObj.main();
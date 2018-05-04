import copy;

class MDP(object):
	matrix=[];
	pwalk,prun=0.0,0.0;
	rrun,rwalk=0.0,0.0;
	terminal=[];
	m,n=0,0;
	rewards=[];
	wall=[];
	gamma=0.0;
	result=[];
	pq = []                        
	factor=0;
	policy=["Walk Up","Walk Down","Walk Left","Walk Right","Run Up","Run Down","Run Left","Run Right"];

	def prioritized_sweeping(self):
		while len(self.pq)>0:
			task = self.pq.pop(0);
			self.addNeigbhor(task);

	def addNeigbhor(self,task):
		i=task[0];
		j=task[1];

		if self.isValid(i-2,j) and [i-2,j] not in self.wall and [i-2,j] not in self.terminal:
			old_utility=self.matrix[i-2][j];
			self.matrix[i-2][j]=self.getUtility(i-2,j);
			sigma=abs(self.matrix[i-2][j]-old_utility);
			if  sigma > self.factor and [i-2,j] not in self.pq:
				self.pq.append([i-2,j]);

		if self.isValid(i+2,j) and [i+2,j] not in self.wall and [i+2,j] not in self.terminal:
			old_utility=self.matrix[i+2][j];
			self.matrix[i+2][j]=self.getUtility(i+2,j);
			sigma=abs(self.matrix[i+2][j]-old_utility);
			if sigma > self.factor and [i+2,j] not in self.pq:
				self.pq.append([i+2,j]);

		if self.isValid(i-1,j) and [i-1,j] not in self.wall and [i-1,j] not in self.terminal:
			old_utility=self.matrix[i-1][j];
			self.matrix[i-1][j]=self.getUtility(i-1,j);
			sigma=abs(self.matrix[i-1][j]-old_utility);
			if sigma > self.factor and [i-1,j] not in self.pq:
				self.pq.append([i-1,j]);

		if self.isValid(i+1,j) and [i+1,j] not in self.wall and [i+1,j] not in self.terminal:
			old_utility=self.matrix[i+1][j];
			self.matrix[i+1][j]=self.getUtility(i+1,j);
			sigma=abs(self.matrix[i+1][j]-old_utility);
			if sigma > self.factor and [i+1,j] not in self.pq:
				self.pq.append([i+1,j]);

		if self.isValid(i,j+2) and [i,j+2] not in self.wall and [i,j+2] not in self.terminal:
			old_utility=self.matrix[i][j+2];
			self.matrix[i][j+2]=self.getUtility(i,j+2);
			sigma=abs(self.matrix[i][j+2]-old_utility);
			if sigma > self.factor and [i,j+2] not in self.pq:
				self.pq.append([i,j+2]);

		if self.isValid(i,j-2) and [i,j-2] not in self.wall and [i,j-2] not in self.terminal:
			old_utility=self.matrix[i][j-2];
			self.matrix[i][j-2]=self.getUtility(i,j-2);
			sigma=abs(self.matrix[i][j-2]-old_utility);
			if sigma > self.factor and [i,j-2] not in self.pq:
				self.pq.append([i,j-2]);

		if self.isValid(i,j+1) and [i,j+1] not in self.wall and [i,j+1] not in self.terminal:
			old_utility=self.matrix[i][j+1];
			self.matrix[i][j+1]=self.getUtility(i,j+1);
			sigma=abs(self.matrix[i][j+1]-old_utility);
			if sigma > self.factor and [i,j+1] not in self.pq:
				self.pq.append([i,j+1]);

		if self.isValid(i,j-1) and [i,j-1] not in self.wall and [i,j-1] not in self.terminal:
			old_utility=self.matrix[i][j-1];
			self.matrix[i][j-1]=self.getUtility(i,j-1);
			sigma=abs(self.matrix[i][j-1]-old_utility);
			if sigma > self.factor and [i,j-1] not in self.pq:
				self.pq.append([i,j-1]);

	def isValid(self,i,j):
		if i<0 or j<0 or i>=self.m or j>=self.n:
			return False;

		return True;

	def getUtility(self,i,j):

		direction=[0 for x in range(8)];
		direction[0]=self.getWalkUp(i,j);
		direction[1]=self.getWalkDown(i,j);
		direction[2]=self.getWalkLeft(i,j);
		direction[3]=self.getWalkRight(i,j);
		direction[4]=self.getRunUp(i,j);
		direction[5]=self.getRunDown(i,j);
		direction[6]=self.getRunLeft(i,j);
		direction[7]=self.getRunRight(i,j);

		id=self.getMax(direction);
		self.result[i][j]=self.policy[id];
		return direction[id];


	def getMax(self,direction):
		id=0;
		for i in range(8):
			if direction[i]>direction[id]:
				id=i;
		return id;
		

	def getWalkUp(self,i,j):
		sum=0.0;

		if i-1<0 or [i-1,j] in self.wall:
			sum+=self.pwalk * (self.rwalk+ self.gamma * self.matrix[i][j]);
		else:
			sum+=self.pwalk * (self.rwalk+ self.gamma * self.matrix[i-1][j]);

		if j-1<0 or [i,j-1] in self.wall:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk+ self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk+ self.gamma * self.matrix[i][j-1]);

		if j+1>=self.n or [i,j+1] in self.wall:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk+ self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk+ self.gamma * self.matrix[i][j+1]);

		return sum;

	def getWalkDown(self,i,j):
		sum=0.0;

		if i+1>=self.m or [i+1,j] in self.wall:
			sum+=self.pwalk * (self.rwalk + self.gamma * self.matrix[i][j]);
		else:
			sum+=self.pwalk * (self.rwalk + self.gamma * self.matrix[i+1][j]);

		if j-1<0 or [i,j-1] in self.wall:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk + self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk + self.gamma * self.matrix[i][j-1]);

		if j+1>=self.n or [i,j+1] in self.wall:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk + self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk + self.gamma * self.matrix[i][j+1]);

		return sum;

	def getWalkLeft(self,i,j):
		sum=0.0;

		if j-1<0 or [i,j-1] in self.wall:
			sum+=self.pwalk * (self.rwalk + self.gamma * self.matrix[i][j]);
		else:
			sum+=self.pwalk * (self.rwalk + self.gamma * self.matrix[i][j-1]);

		if i-1<0 or [i-1,j] in self.wall:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk + self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk + self.gamma * self.matrix[i-1][j]);

		if i+1>=self.m or [i+1,j] in self.wall:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk + self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk + self.gamma * self.matrix[i+1][j]);

		return sum;

	def getWalkRight(self,i,j):
		sum=0.0;

		if j+1>=self.n or [i,j+1] in self.wall:
			sum+=self.pwalk * (self.rwalk + self.gamma * self.matrix[i][j]);
		else:
			sum+=self.pwalk * (self.rwalk + self.gamma * self.matrix[i][j+1]);

		if i-1<0 or [i-1,j] in self.wall:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk + self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk + self.gamma * self.matrix[i-1][j]);

		if i+1>=self.m or [i+1,j] in self.wall:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk + self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.pwalk) * (self.rwalk + self.gamma * self.matrix[i+1][j]);

		return sum;

	def getRunUp(self,i,j):
		sum=0.0;

		if i-2<0 or [i-2,j] in self.wall or [i-1,j] in self.wall:
			sum+=self.prun * (self.rrun + self.gamma * self.matrix[i][j]);
		else:
			sum+=self.prun * (self.rrun + self.gamma * self.matrix[i-2][j]);

		if j-2<0 or [i,j-2] in self.wall or [i,j-1] in self.wall:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i][j-2]);

		if j+2>=self.n or [i,j+2] in self.wall or [i,j+1] in self.wall:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i][j+2]);

		return sum;

	def getRunDown(self,i,j):
		sum=0.0;

		if i+2>=self.m or [i+2,j] in self.wall or [i+1,j] in self.wall:
			sum+=self.prun * (self.rrun + self.gamma * self.matrix[i][j]);
		else:
			sum+=self.prun * (self.rrun + self.gamma * self.matrix[i+2][j]);

		if j-2<0 or [i,j-2] in self.wall or [i,j-1] in self.wall:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i][j-2]);

		if j+2>=self.n or [i,j+2] in self.wall or [i,j+1] in self.wall:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i][j+2]);

		return sum;

	def getRunLeft(self,i,j):
		sum=0.0;

		if j-2<0 or [i,j-2] in self.wall or [i,j-1] in self.wall:
			sum+=self.prun * (self.rrun + self.gamma * self.matrix[i][j]);
		else:
			sum+=self.prun * (self.rrun + self.gamma * self.matrix[i][j-2]);

		if i-2<0 or [i-2,j] in self.wall or [i-1,j] in self.wall:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i-2][j]);

		if i+2>=self.m or [i+2,j] in self.wall or [i+1,j] in self.wall:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i+2][j]);

		return sum;

	def getRunRight(self,i,j):
		sum=0.0;

		if j+2>=self.n or [i,j+2] in self.wall or [i,j+1] in self.wall:
			sum+=self.prun * (self.rrun + self.gamma * self.matrix[i][j]);
		else:
			sum+=self.prun * (self.rrun + self.gamma * self.matrix[i][j+2]);

		if i-2<0 or [i-2,j] in self.wall or [i-1,j] in self.wall:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i-2][j]);

		if i+2>=self.m or [i+2,j] in self.wall or [i+1,j] in self.wall:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i][j]);
		else:
			sum+=0.5 * (1-self.prun) * (self.rrun + self.gamma * self.matrix[i+2][j]);

		return sum;

	def main(self):
		inputFile = open('input.txt', 'r');	
		#Read input File
		dimension=inputFile.readline().rstrip('\n').split(",");
		self.m=int(dimension[0]);
		self.n=int(dimension[1]);

		wallNo=int(inputFile.readline().rstrip('\n'));
		for i in range(wallNo):
			wallDim=inputFile.readline().rstrip('\n').split(",");
			self.wall.append([int(self.m-int(wallDim[0])),int(int(wallDim[1])-1)]);

		terminalNo=int(inputFile.readline().rstrip('\n'));
		for i in range(terminalNo):
			terminalDim=inputFile.readline().rstrip('\n').split(",");
			self.terminal.append([int(self.m-int(terminalDim[0])),int(int(terminalDim[1])-1)]);
			self.rewards.append(float(terminalDim[2]));
		
		prob=inputFile.readline().rstrip('\n').split(",");
		self.pwalk=float(prob[0]);
		self.prun=float(prob[1]);

		rew=inputFile.readline().rstrip('\n').split(",");
		self.rwalk=float(rew[0]);
		self.rrun=float(rew[1]);

		self.gamma=float(inputFile.readline().rstrip('\n'));

		self.matrix=[[0 for x in range(self.n)] for y in range(self.m)];
		self.result=[[0 for x in range(self.n)] for y in range(self.m)]

		for i in range(len(self.terminal)):
			temp=self.terminal[i];
			self.matrix[temp[0]][temp[1]]=self.rewards[i];
			self.pq.append(temp);
			self.result[temp[0]][temp[1]]="Exit"

		for w in self.wall:
			self.result[w[0]][w[1]]="None";

		self.prioritized_sweeping();

		output_file = open("output.txt", "w");
		for i in range(self.m):
			output_file.write(",".join(self.result[i]));
			if i<self.m-1:
				output_file.write("\n");
			
mdpObj=MDP();
mdpObj.main();



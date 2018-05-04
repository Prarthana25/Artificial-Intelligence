import copy;

class Group(object):
	def __init__(self,groupId,count):
		self.groupId=groupId;
		self.count=count;
		self.pot=[];
		self.conf=[];
		self.country=[];

	def addCountry(self,country,pot,conf):
		self.country.append(country);
		self.pot.append(pot);
		self.conf.append(conf);
		self.count+=1;

	def removeCountry(self,country,pot,conf):
		self.country.remove(country);
		self.pot.remove(pot);
		self.conf.remove(conf);
		self.count-=1;


class CSP(object):
	groupCount,potCount=0,0;
	pot=list();
	conf=dict();
	group=list(); 
	value=0;
	variables=list();

	def setVariables(self):
		for potList in self.pot:
			for var in potList:
				self.variables.append(var);
				self.value+=1;

	def setDomains(self,initialDomain):
		for var in self.variables:
			domains[var]=initialDomain;

	def getGroupList(self,currPot,currConf):
		sortedList=[];

		for grp in self.group:
			if(currPot not in grp.pot):
				if(currConf not in grp.conf or (currConf=='UEFA' and grp.conf.count(currConf)<2)):
					sortedList.append(grp);

		return sortedList;

	def getPot(self,country):
		for i in range(len(self.pot)):
			if country in self.pot[i]:
				return i;
		return -1;

	def getConf(self,country):
		for key in self.conf:
			if country in self.conf[key]:
				return key;
		return None;

	def backTracking(self,index):
		if(index >= self.value): return True;

		country=self.variables[index];

		currPot=self.getPot(country);
		currConf=self.getConf(country);
		availableGroup=self.getGroupList(currPot,currConf);

		for grp in availableGroup:
				grp.addCountry(country,currPot,currConf);
				if(self.backTracking(index+1)):
					return True;
				grp.removeCountry(country,currPot,currConf);

		return False;

	def checkValidInput(self):
		for potList in self.pot:
			if len(potList)>self.groupCount:
				return False;

		for key in self.conf:
			if((key!='UEFA' and len(self.conf[key])>self.groupCount) or (key=='UEFA' and len(self.conf[key])>2*self.groupCount)):
				return False;
		return True;
	
	def main(self):
		inputFile = open('input.txt', 'r');
		self.groupCount=int(inputFile.readline().rstrip('\n'));
		self.potCount=int(inputFile.readline().rstrip('\n'));

		for i in range(self.potCount):
			potList=inputFile.readline().rstrip('\n');
			self.pot.append(potList.split(","));

		for i in range(6):
			confList=inputFile.readline().rstrip('\n');
			confArray=confList.split(":");
			if confArray[1]=="None":
				self.conf[confArray[0]]=[];
			else:
				self.conf[confArray[0]]=confArray[1].split(",");

		result=self.checkValidInput();
		output_file = open("output.txt", "w");

		if(result==False):
			output_file.write("No");
		else:
			for i in range(self.groupCount):
				self.group.append(Group(i,0));

			self.setVariables();
			result=self.backTracking(0);
		
			if(result==True):
				output_file.write("Yes");
				for grp in self.group:
					if len(grp.country)==0:
						output_file.write("\nNone");
					else:
						output_file.write("\n");
						output_file.write(",".join(grp.country));
			else:
				output_file.write("No");
		output_file.close();

csp=CSP();
csp.main();
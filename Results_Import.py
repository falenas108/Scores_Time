#Analyzes data from students
#M=Math on the ACT
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import math
from scipy import optimize,loadtxt,genfromtxt
import datetime
import subprocess
from datetime import datetime as dt

Forw={'ACT Math':0,'ACT Science':1,'Math 1':2,'Math 2':3,'Physics':4,'Chemistry':5}
Rev=dict((v,k) for k,v in Forw.iteritems())
#Dictionary that allows me to sort students by test.
f=open('Results.txt','r')

def linear(p,xvar):
	return p[0]*xvar

residual=lambda p,resid, x, y, err: (resid(p, x)-y)/err

#Class for student records
class Student(object):
	def __init__(self,name,ttype,scores,dates,complete):
		self.name=name
		self.dates=np.array(dates)
		self.scores=np.array(scores)
		self.ttype=ttype
		self.complete=complete
	def showscores(self):
		print '%s\'s scores were %s, which she took on days %s' %(self.name,self.scores,self.dates)


def datetonum(dates):
#Finds how many weeks a date is from the starting day
	li=[]
	for dat in dates:
		li.append(((dt.strptime(dat,'%m/%d/%y').date()-dt.strptime(dates[0],'%m/%d/%y').date()).days)/7)
	return li
def scorediff(scores):
#Finds the difference in scores between the start and all other points
	li=[]
	for sc in scores:
		li.append(int(sc)-int(scores[0]))
	return li

def elim_empty(lis):
		return [s for s in lis if s]

def changeovertime(Students,title):
#Graphs students scores on practice and actual tests over the time tutored
	for St in Students:
		plt.plot(St.dates,scorediff(St.scores),'o',label=St.name+St.ttype)
	plt.xlabel('Number of Weeks Tutored')
	plt.ylabel('Score Change')
	plt.title(title)
	plt.savefig('Results/'+title)
	plt.clf()

def changeoverall(Students, title):
	AveInc=0
	Percinc=[]
	Dates=[]
#Graphs the percent of attainable points at the end of a program
	for St in Students:
		Dates.append(St.dates[-1])
		Percinc.append((int(St.scores[-1])-int(St.scores[0]))/(float(36-int(St.scores[0]))))
		AveInc+=Percinc[-1]
	Dates=np.array(Dates)
	Percinc=np.array(Percinc)
	plt.plot(Dates,Percinc,'bo')
	plt.xlabel('Number of Weeks Tutored')
	plt.ylabel('Percent of Attainable Points')
	plt.title('Percent of Attainable Points for '+title)
	plt.xlim(0,10)
	plt.ylim(0,1)
	print AveInc/float(len(Students))
#Creates a line of best fit
	p0=[.5]
	pferr=[]
	Distrib=[[]for i in range(2)]
	pf, cov, info, mesg, success = optimize.leastsq(residual, p0, args=(linear,Dates,Percinc,[1/i for i in Percinc]),full_output=1)
	print pf,success
	chisq = sum(info["fvec"]*info["fvec"])
	dof=len(Students)-len(p0)
	for i in range(len(pf)):
		pferr.append(sqrt(cov[i,i]))
	Distrib[0]=linspace(0,10,10000)
	Distrib[1]=(linear(pf,Distrib[0]))
	plt.plot(Distrib[0],Distrib[1])
	for m in range(len(pf)):
		p=subprocess.check_output(['python RoundValues.py %s %s' %(str(pf[m]),str(pferr[m]))],shell=True)
		p=p.split()
		pf[m]=float(p[0])
		pferr[m]=float(p[1])
	textfit = '$f(x)= ax$\n' \
   	          '$a = %s \pm %s \, Percent\, points/week$\n' \
   	          % (pf[0], pferr[0])
	plt.text(5,.8, textfit,fontsize=14)
	plt.show()
	return

#Reads data and separates by students
Dat=f.read()
Dat=Dat.split('\r')
Data=[[]for i in range(len(Dat)-1)]
StList=[[]for i in  range(6)]
for n,line in enumerate(Dat):
	Data[n-1]=line.split('\t')
for n in range(len(Data)/2):
#Enters students in the class 'Student'. The first dimension sorts by test type.
	StList[int(Forw[Data[2*n][1]])].append(Student(Data[2*n][0],Data[2*n][1],elim_empty(Data[2*n][3:]),datetonum(elim_empty(Data[2*n+1][3:])),Data[2*n][2]))
StList=np.array(StList)
for j in range(6):
	changeovertime([StList[j][i] for i in range(len(StList[5]))],Rev[j]+' Score Changes')

#Finds the students who have finished their program
studcomplete=[]
for j in StList.flat:
	for k in j:
		if k.complete=='Complete':
			studcomplete.append(k)
changeoverall(studcomplete,'All Students')
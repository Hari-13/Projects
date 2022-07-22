import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

from scipy.stats import norm

from math import *

#parameters:

time_to_maturity=3.0

t_steps=25

r=0.03

d=0.02

sigma=0.2

K=100.0

S0=100.0

def Pay_off(x):

    global K

    return max(x-K,0)

class Binomial_Tree:

    def __init__(self,time_to_maturity,steps,risk_free_rate,dividend,sigma,strike,spot,tree_trait):

        self.dt=time_to_maturity/steps

        self.r=risk_free_rate

        self.d=dividend

        self.sigma=sigma

        self.K=strike

        self.S0=spot

        self.t_steps=steps

        self.lattice=np.zeros([self.t_steps+1,self.t_steps+1])

        self.rlattice=np.zeros([self.t_steps+1,self.t_steps+1])

        self.up=tree_trait.up(self)

        self.down=tree_trait.down(self)

        self.up_prob=tree_trait.up_prob(self)

        self.down_prob=1.0-self.up_prob

        self.lattice_constructor()

    def lattice_constructor(self):

       self.lattice[0,0]=self.S0

       for i in range(1,self.t_steps+1):

         for j in range(i):

          self.lattice[i][j]=self.lattice[i-1][j]*self.down

         if(i<=self.t_steps):

          self.lattice[i][i]=self.lattice[i-1][i-1]*self.up

    def roll_back(self,Pay_off):

        self.lattice[self.t_steps]=map(Pay_off, self.lattice[self.t_steps])

        for i in range(self.t_steps,0,-1):

         for j in range(i):

           self.lattice[i-1][j]=exp(-self.r*self.dt)*(self.lattice[i][j]*self.down_prob+self.lattice[i][j+1]*self.up_prob)

class Jarrow_Rudd_trait:

    @staticmethod

    def up(tree):

        up=exp((tree.r-tree.d-0.5*tree.sigma**2)*tree.dt+tree.sigma*sqrt(tree.dt))

        return up

    @staticmethod

    def down(tree):

        down=exp((tree.r-tree.d-0.5*tree.sigma**2)*tree.dt-tree.sigma*sqrt(tree.dt))

        return down

    @staticmethod

    def up_prob(tree):

        return 0.5

class Cox_Ross_Rubinstein_trait:

    @staticmethod

    def up(tree):

        up=exp(tree.sigma*sqrt(tree.dt))

        return up

    @staticmethod

    def down(tree):

        down=exp(-tree.sigma*sqrt(tree.dt))

        return down

    @staticmethod

    def up_prob(tree):

        return 0.5 + 0.5 * (tree.r - tree.d - 0.5 * tree.sigma**2) * tree.dt/tree.sigma/sqrt(tree.dt)



class ABinomial_Tree(Binomial_Tree):

    def roll_back(self,Pay_off):

     self.lattice[self.t_steps]=map(Pay_off, self.lattice[self.t_steps])

     for i in range(self.t_steps,0,-1):

         for j in range(i):

           con_val=exp(-self.r*self.dt)*(self.lattice[i][j]*self.down_prob+self.lattice[i][j+1]*self.up_prob)

           exe_val=Pay_off(self.lattice[i-1][j])

           if(exe_val>con_val):

               self.lattice[i-1][j]=exe_val

           else:

               self.lattice[i-1][j]=con_val

\

JR=[]

CRR=[]

AJR=[]

ACRR=[]

step_range=range(25,500,25)

for i in step_range:

    tree1=Binomial_Tree(time_to_maturity,i,r,d,sigma,K,S0,Jarrow_Rudd_trait)

    tree1.roll_back(Pay_off)

    tree2=Binomial_Tree(time_to_maturity,i,r,d,sigma,K,S0,Cox_Ross_Rubinstein_trait)

    tree2.roll_back(Pay_off)

    tree3=ABinomial_Tree(time_to_maturity,i,r,d,sigma,K,S0,Jarrow_Rudd_trait)

    tree3.roll_back(Pay_off)

    tree4=ABinomial_Tree(time_to_maturity,i,r,d,sigma,K,S0,Cox_Ross_Rubinstein_trait)

    tree4.roll_back(Pay_off)

    JR.append(tree1.lattice[0,0])

    CRR.append(tree2.lattice[0,0])

    AJR.append(tree3.lattice[0,0])

    ACRR.append(tree4.lattice[0,0])

sns.set_style("ticks")

plt.plot(step_range,JR,"-.",marker="o",markersize=10)

plt.plot(step_range,CRR,"-.",marker="d",markersize=10)

plt.plot(step_range,AJR,"-.",marker="s",markersize=10)

plt.plot(step_range,ACRR,"-.",marker="p",markersize=10)

plt.legend(["Jarrow Rudd Tree(E)","Cox Ross Rubinstein Tree(E)","Jarrow Rudd Tree(A)","Cox Ross Rubinstein Tree(a)"],fontsize=12)

plt.title("Convergence test", fontsize=16)

plt.show()

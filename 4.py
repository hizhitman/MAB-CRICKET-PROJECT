# -*- coding: utf-8 -*-
"""Q4_um.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Q8Xs8uGFSRrObTUvpPXpPqXgEjiouJJl
"""

import numpy as np
import time
# Students will submit their files with their team-name.py
# Student have to use the Team as their parent class

"""Recent Version of the Code"""

class ROLLNUMBER_Q4:
  def __init__(self,num_balls,num_matches):
    self.N= np.zeros(6)
    self.S =np.zeros(6)
    self.W= np.zeros(6)
    self.VW = np.zeros(6)
    self.VS = np.zeros(6)
    self.prev = -1
    self.t = 0
    self.ucb =np.ones(6)*np.inf
    self.curr_wick = 4
    self.curr_ball = num_balls
    self.r = np.zeros(6)





  def get_action(self,wicket,runs_scored):
    if(self.t//num_balls>num_matches//5):
      self.curr_wick -= wicket

      self.curr_ball -= 1

      if(self.curr_ball<0):
        self.curr_ball = num_balls
        self.curr_wick=4
      if(self.curr_wick>0):
        probs = []
        for arm in range(6):
          if(self.N[arm]/self.W[arm]>self.curr_ball/self.curr_wick):
            probs.append(arm)

        prem = n
        pre = np.inf
        for arm in range(6):
          if(self.N[arm]/self.W[arm]<pre):
            pre = self.N[arm]/self.W[arm]
            prem = arm
        sel = prem
        pre = 0

        for prob in probs:
          if(self.S[prob]/self.N[prob]>pre):
            pre = self.S[prob]/self.N[prob]
            sel = prob
        self.prev = sel

    else:

      if self.prev != -1:
        self.N[self.prev] += 1
        self.t += 1
        self.S[self.prev] += runs_scored
        self.VS[self.prev] += (runs_scored-self.S[self.prev]/self.N[self.prev])** 2
        self.W[self.prev] += wicket
        self.VW[self.prev] += (wicket-self.W[self.prev]/self.N[self.prev])** 2

        self.r[self.prev] = self.S[self.prev] / max(self.W[self.prev],1e-8)
        eps = (np.sqrt(2*self.VS[self.prev])*np.log(self.t**2)/(self.N[self.prev] **2)+18*np.log(self.t**2)) /self.N[self.prev]
        eta = (np.sqrt(2*self.VW[self.prev])*np.log(self.t**2)/(self.N[self.prev] **2)+3*np.log(self.t**2)) /self.N[self.prev]
        c = 1.4*(eps + self.r[self.prev]*eta) / max(self.W[self.prev]/self.N[self.prev],1e-8)
        self.ucb[self.prev] = self.r[self.prev]+c
      self.prev = np.argmax(self.ucb)
    #print(self.prev)
    return self.prev

class Environment:
  def __init__(self,num_balls,agent):
    self.num_balls = num_balls
    self.agent = agent
    self.__run_time = 0
    self.__total_runs = 0
    self.__total_wickets = 0
    self.__runs_scored = 0
    self.__start_time = 0
    self.__end_time = 0
    self.__p_out =np.array([0.001,0.01,0.02,0.03,0.1,0.3])
    self.__p_run =np.array([1,0.9,0.85,0.8,0.75,0.7])
    self.__action_runs_map = np.array([0,1,2,3,4,6])
    self.__wickets_left = 4
    self.__wicket = 0
    self.__runs_scored = 0
    self.__start_time = 0
    self.__end_time = 0
    self.__batting_order = np.array([0,1,2,3])

  def __get_action(self):
    self.__start_time      = time. time()
    action          = self.agent.get_action(self.__wicket, self.__runs_scored)
    self.__end_time        = time. time()
    self.__run_time   = self.__run_time + self.__end_time - self.__start_time
    return action


  def __get_outcome(self, action):
    pout = self.__p_out[action]
    prun = self.__p_run[action]
    wicket = np.random.choice(2,1,p=[1-pout,pout])[0]
    runs = 0
    if(wicket==0):
      runs = self.__action_runs_map[action]*np.random.choice(2,1,p=[1-prun,prun])[0]
    return wicket, runs


  def innings(self):
    self.__wickets_left = 4
    self.__runs_scored = 0
    self.__wickets_left = 4
    self.__total_runs = 0
    self.__total_wickets = 0
    self.__run_time = 0
    self.__start_time = 0
    self.__end_time = 0

    for ball in range(self.num_balls):
      if (self.__wickets_left > 0 ) :
        action = self.__get_action()
        self.__wicket, self.__runs_scored   = self.__get_outcome(action)
        self.__total_runs     = self.__total_runs + self.__runs_scored
        if (self.__wicket > 0 ):
          self.__wickets_left = self.__wickets_left -1
        self.__total_wickets  = self.__total_wickets + self.__wicket
        if (self.__wickets_left == 0):
          self.__get_action()
    return self.__total_runs, self.__total_wickets, self.__run_time

num_matches = 100
num_balls = 60
agent = ROLLNUMBER_Q4(num_balls,num_matches)
environment = Environment(num_balls,agent)
score = np.zeros((num_matches,1))
run_time = np.zeros((num_matches,1))
wicket = np.zeros((num_matches,1))
for i in range(num_matches):
  score[i],wicket[i],run_time[i] = environment.innings()

print(np.mean(score))


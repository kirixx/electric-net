import os
import operator
import sys, time
import xml.etree.cElementTree as ET
from random import randint
from enum import Enum
from time import clock

#faultTree
tree = None
node = None
findCheck = False


State = type("State",(object,),{})

class Initial(State):
    def Execute(self):
        print('Initial')
        time.sleep(1)

class Emergency(State):
    def Execute(self):
        print('Emergency')
        time.sleep(10)

class Transition(object):
    def  __init__(self,toState):
        self.toState = toState

    def Execute(self):
        print('Transitioning...')

class FSm(object):
    def __init__(self, char):
        self.char = char
        self.states = {}
        self.transitions = {}
        self.curState = None
        self.trans = None
    
    def setState(self, stateName):
        self.curState = self.states[stateName]
    
    def transition(self, transName):
        self.trans = self.transitions[transName]

    def Execute(self):
        if(self.trans):
            self.trans.Execute()
            self.setState(self.trans.toState)
            self.trans = None
        self.curState.Execute()

class Char(object):
    def __init__(self):
        self.FSM = FSm(self)
        self.Initial = True


treeFaultSignals ={
            'NoCurrentFromDCCurrentSource'    : 0,
            'StartRelayFailInOpenPosition'    : 0,
            'PressureSwitchFailInClosedPos'   : 0,
            'VictingUnitFailsToRaiseSignal'   : 0,
            'FusePlug1DoesNotRespond'         : 0,
            'FusePlug2DoesNotRespond'         : 0,
            'FusePlug3DoesNotRespond'         : 0,
            'FusePlug4DoesNotRespond'         : 0,
            'SmokeDetector1and2DoesntRespond' : 0,
            'SmokeDetector1and3DoesntRespond' : 0,
            'SmokeDetector2and3DoesntRespond' : 0,
            'ManualSwitchFallsToOpen'         : 0,
            'PressureSwitchFalls'             : 0,
            'OperatorFailsToTakeAction'       : 0
    }
#setting modulation cases
map = {
            0  : 'NoCurrentFromDCCurrentSource',                      
            1  : 'StartRelayFailInOpenPosition',                            
            2  : 'PressureSwitchFailInClosedPos', 
            3  : 'VictingUnitFailsToRaiseSignal',                      
            4  : 'FusePlug1DoesNotRespond',                 
            5  : 'FusePlug2DoesNotRespond',                 
            6  : 'FusePlug3DoesNotRespond',                
            7  : 'FusePlug4DoesNotRespond',                                                   
            8  : 'SmokeDetector1and2DoesntRespond',             
            9  : 'SmokeDetector1and3DoesntRespond',             
            10 : 'SmokeDetector2and3DoesntRespond',                             
            11 : 'ManualSwitchFallsToOpen', 
            12 : 'PressureSwitchFalls',             
            13 : 'OperatorFailsToTakeAction'                   
      }
#list of possible states of machine
states = {
          'NoCurrentFromDCCurrentSource'   : False,
          'PressureSwitchFailInClosedPos'  : False,
          'VictingUnitFailsToRaiseSignal'  : False,
          'FusePlug1DoesNotRespond'        : False,
          'FusePlug2DoesNotRespond'        : False,
          'FusePlug3DoesNotRespond'        : False,
          'FusePlug4DoesNotRespond'        : False,
          'SmokeDetector1and2DoesntRespond': False,
          'SmokeDetector1and3DoesntRespond': False,
          'SmokeDetector2and3DoesntRespond': False,
          'ManualSwitchFallsToOpen'        : False,
          'PressureSwitchFalls'            : False,
          'OperatorFailsToTakeAction'      : False
         }

def getSignal():
    f = open('fsmConfig.txt')
    global currentSignal
    currentSignal = f.readline(7)
    print(currentSignal)
    return currentSignal

def FSM():
    global currentState 
    global currentSignal
    newState = FSMTable[(currentState,currentSignal)]
    currentState = newState;
    print(currentState)

#find a solution for the chosen problem
def findInFaultTree(currentNode):
    global findCheck
    global currentState 
    global currentSignal
    for i in range(len(currentNode)):
         if(len(currentNode[i]) == 0 and currentNode[i].text != treeFaultSignals[currentNode[i].tag]):
             print('\nEmergncy', currentNode[i].tag, 'default signal',currentNode[i].text,'mutable signal',treeFaultSignals[currentNode[i].tag],'\n')
             states[currentNode[i].tag] = True
         elif(len(currentNode[i]) == 0 and currentNode[i].text == treeFaultSignals[currentNode[i].tag]):
             print(currentNode[i].tag, 'default signal',currentNode[i].text,'mutable signal',treeFaultSignals[currentNode[i].tag])
             time.sleep(1)
         elif(len(currentNode[i]) > 1):
             time.sleep(1)
             print(currentNode[i])
             findInFaultTree(currentNode[i])
            
def switchState(state):
    exitFromLastState()
    states[state] = True
                        
def exitFromLastState():
    for state in states.keys():
        if states[state] == True:
            states[state] = False                  
    
#main function
def main(argv = sys.argv):
     global tree
     global node
     global findCheck
     try:
        tree = ET.parse('faultTree.xml')
     except IOError as e:
        print ('\nERROR - cant find file: %s\n') % e 
     node = tree.getroot()     
     f = open('fsmConfig.txt','r')
     for idx,line in enumerate(f):
        treeFaultSignals[map[idx]] = line[3:5]
     sorted(treeFaultSignals)

if __name__ == "__main__":
   main()
   findInFaultTree(node[0])
   state = Char()
   state.FSM.states["Initial"] = Initial()
   state.FSM.states["Emergency"] = Emergency()
   state.FSM.transitions["toInitial"] = Transition("Initial")
   state.FSM.transitions["toEmergency"] = Transition("Emergency")
   state.FSM.setState("Initial")

   for i in states.keys():      
       if(states[i]): 
           states[i] = False
           state.FSM.transition("toEmergency")
           state.Initial = False      
       else:
           state.FSM.transition("toInitial")
           state.Initial = True
       print(i)
       state.FSM.Execute()
       print('\n')
  
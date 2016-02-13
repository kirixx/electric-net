import os
import operator
import sys, time
import xml.etree.cElementTree as ET
from random import randint
from enum import Enum


#faultTree
tree = None
node = None
findCheck = False

signalsFSM = {
            -3: 'emergency',
            -2: 'off',
            -1: 'initial'
             }
 
treeFaultSignals ={
            'NoCurrentFromDCCurrentSource' : 0,
            'StartRelayFailInOpenPosition' : 0,
            'PressureSwitchFailInClosedPos' : 0,
            'VictingUnitFailsToRaiseSignal' : 0,
            'FusePlug1DoesNotRespond' : 0,
            'FusePlug2DoesNotRespond' : 0,
            'FusePlug3DoesNotRespond' : 0,
            'FusePlug4DoesNotRespond' : 0,
            'SmokeDetector1and2DoesntRespond' : 0,
            'SmokeDetector1and3DoesntRespond' : 0,
            'SmokeDetector2and3DoesntRespond': 0,
            'ManualSwitchFallsToOpen': 0,
            'PressureSwitchFalls': 0,
            'OperatorFailsToTakeAction': 0
    }
FSMStates =['initial','off','emergency']
FSMTable = {
            #initial
            (FSMStates[0],signalsFSM[-3]) : FSMStates[2], #emergency
            (FSMStates[0],signalsFSM[-2]) : FSMStates[1], #off
            (FSMStates[0],signalsFSM[-1]) : FSMStates[0], #initial
            #off
            (FSMStates[1],signalsFSM[-3]) : FSMStates[2], #emergency
            (FSMStates[1],signalsFSM[-2]) : FSMStates[1], #off
            (FSMStates[1],signalsFSM[-1]) : FSMStates[0], #initial
            #emergency
            (FSMStates[2],signalsFSM[-3]) : FSMStates[2], #emergency
            (FSMStates[2],signalsFSM[-2]) : FSMStates[1], #off
            (FSMStates[2],signalsFSM[-1]) : FSMStates[0]  #initial
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
          'DEFAULT'   : False,
          'DC'        : False,
          'SR'        : False,
          'PS'        : False,
          'VU'        : False,
          'MS'        : False,
          'PF'        : False,
          'OP'        : False,
          'FP1'       : False,
          'FP2'       : False,
          'FP3'       : False,
          'FP4'       : False,
          'SD1andSD2' : False,
          'SD1andSD3' : False,
          'SD2andSD3' : False
         }
#current state of state-machine
currentState = FSMStates[0]
currentSignal = signalsFSM[-1]
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
    #print(currentState, currentSignal, newState)
    currentState = newState;
    print(currentState)

#find a solution for the chosen problem
def findInFaultTree(currentNode):
    global findCheck
    global currentState 
    global currentSignal
    for i in range(len(currentNode)):
         if(len(currentNode[i]) == 0 and currentNode[i].text != treeFaultSignals[currentNode[i].tag]):
             findCheck = True
             currentState = FSMStates[2]
             currentSignal = signalsFSM[-3]
             print(currentNode[i].tag)
             FSM()      
         elif(len(currentNode[i]) == 0 and currentNode[i].text == treeFaultSignals[currentNode[i].tag]):
             currentState = FSMStates[0]
             currentSignal = signalsFSM[-1]
             print(currentNode[i].tag)
             FSM()
         elif(len(currentNode[i]) > 1):
             if findCheck == False:
                 time.sleep(2)
                 print(currentNode[i])
                 findInFaultTree(currentNode[i])
            
def switchState(state):
    exitFromLastState()
    print('***SYSTEM SET', state, 'STATE***\n')
    states[state] = True
                        
def exitFromLastState():
    for state in states.keys():
        if states[state] == True:
            states[state] = False
        else:
            print(state, states[state])                    
    
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
     while True:
          print('Do you want start the system(y/n):\n')
          a = input()
          if a == 'y' or a =='Y':
              findCheck = False
              #print('***ALL IS FINE, SYSTEM WORK IN DEFAULT = ',states['DEFAULT'],' STATE***\n')
              time.sleep(5)
              #numberOfCase = randint(0,13)
              #print('***SOME KIND OF TROUBLE***', map[numberOfCase])

              findInFaultTree(node[0])
          else:
              sys.exit()          


if __name__ == "__main__":     
   
   f = open('fsmConfig.txt','r')
   for idx,line in enumerate(f):
        treeFaultSignals[map[idx]] = line[3:5]
   sorted(treeFaultSignals)
   main()
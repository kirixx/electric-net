import os
import operator
import sys, time
import xml.etree.cElementTree as ET
from random import randint
from enum import Enum

#current state of state-machine
currentState = None
#faultTree
tree = None
node = None
findCheck = False
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
            12 : 'OperatorFailsToTakeAction'                   
      }
#list of possible states of machine
states = {
          'DEFAULT'   : False,
          'DC'        : False,
          'SR'        : False,
          'PS'        : False,
          'VU'        : False,
          'MS'        : False,
          'OP'        : False,
          'FP1'       : False,
          'FP2'       : False,
          'FP3'       : False,
          'FP4'       : False,
          'SD1andSD2' : False,
          'SD1andSD3' : False,
          'SD2andSD3' : False
         }

#find a solution for the chosen problem
def findInFaultTree(caseNum,currentNode):
    global findCheck
    for i in range(len(currentNode)):
        if(currentNode[i].tag == map[caseNum]):
            print(currentNode[i])
            switchState(currentNode[i].attrib['stateId'])
            findCheck = True
            break
        elif(currentNode[i].tag != map[caseNum] and len(currentNode[i]) > 1):
            if findCheck == False:
                time.sleep(2)
                print(currentNode[i])
                findInFaultTree(caseNum, currentNode[i])
        else:
            findCheck = False 
            
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
     try:
        tree = ET.parse('faultTree.xml')
     except IOError as e:
        print ('\nERROR - cant find file: %s\n') % e 
     node = tree.getroot()
     while True:
          print('Do you want start the system(y/n):\n')
          a = input()
          if a == 'y' or a =='Y':
              states['DEFAULT'] = True
              print('***ALL IS FINE, SYSTEM WORK IN DEFAULT = ',states['DEFAULT'],' STATE***\n')
              time.sleep(5)
              numberOfCase = randint(0,12)
              print('***SOME KIND OF TROUBLE***', map[numberOfCase])

              findInFaultTree(numberOfCase,node[0])
          else:
              sys.exit()          

if __name__ == "__main__":     
    main()
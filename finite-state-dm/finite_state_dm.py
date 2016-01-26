import os
import operator
import sys
import xml.etree.cElementTree as ET
from enum import Enum

#current state of state-machine
currentState = None
#faultTree
tree = None
node = None
findCheck = False
#node from which we start
rootOfCases = None
#setting modulation cases
settings = {            
            'NoCurrentFromDCCurrentSource'            : None,
            'StartRelayFailInOpenPosition'            : None,
            'PressureSwitchFailInClosedPos'           : None,
            'VictingUnitFailsToRaiseSignal'           : None,
            'FusePlug1DoesNotRespond'                 : None,
            'FusePlug2DoesNotRespond'                 : None,
            'FusePlug3DoesNotRespond'                 : None,
            'FusePlug4DoesNotRespond'                 : None,
            'SmokeDetector1DoesntRespond'             : None,
            'SmokeDetector2DoesntRespond'             : None,
            'SmokeDetector3DoesntRespond'             : None,
            'ManualSwitchFallsToOpen'                 : None
           }
map = {
            0  : 'NoCurrentFromDCCurrentSource',                      
            1  : 'StartRelayFailInOpenPosition',                            
            2  : 'PressureSwitchFailInClosedPos', 
            3  : 'VictingUnitFailsToRaiseSignal',                      
            4  : 'FusePlug1DoesNotRespond',                 
            5  : 'FusePlug2DoesNotRespond',                 
            6  : 'FusePlug3DoesNotRespond',                
            7  : 'FusePlug4DoesNotRespond',                                                   
            8  : 'SmokeDetector1DoesntRespond',             
            9  : 'SmokeDetector2DoesntRespond',             
            10  : 'SmokeDetector3DoesntRespond',                             
            11 : 'ManualSwitchFallsToOpen',                 
            12 : 'OperatorFailsToTakeAction'                   
      }
#list of possible states of machine
states = {
          'DC'  : False,
          'SR'  : False,
          'PS'  : False,
          'VU'  : False,
          'MS'  : False,
          'OP'  : False,
          'FP1' : False,
          'FP2' : False,
          'FP3' : False,
          'FP4' : False,
          'SD1' : False,
          'SD2' : False,
          'SD3' : False
         }

#configure settings
def setSettings(caseNum,currentNode):
    global findCheck
    for i in range(len(currentNode)):
        if(currentNode[i].tag == map[caseNum]):     
            print(currentNode[i].attrib['stateId'])
            states[currentNode[i].attrib['stateId']] = True
            findCheck = True
            break
        elif(currentNode[i].tag != map[caseNum] and len(currentNode[i]) > 1):

            print(len(currentNode[i]))
            print(True)
            settings[map[caseNum]] = True
            currentNode = currentNode[i]
            setSettings(caseNum,currentNode[i+1])
            print(currentNode[i-1])
       # if findCheck == False:   
            
                    
                    
    
#main function
def main(argv = sys.argv):
     global tree
     global rootOfCases
     global node
     try:
        tree = ET.parse('faultTree.xml')
     except IOError as e:
        print ('\nERROR - cant find file: %s\n') % e
     if len(argv) > 1 and argv[1] == 'NoSignalFromTheStartRelay':
         rootOfCases = argv[1]
         node = tree.getroot().find(rootOfCases)
         while True:
             print('Choose case of modulation:\n')
             for idx, case in enumerate(map.values()):
                 print(idx,case)
             a = int(input())
             setSettings(a,node)
             if a > len(map)-1:
                 print('incorrect number')             
     else:
         print('try again with \'NoSignalFromTheStartRelay\'')  

if __name__ == "__main__":     
    main()
import os
import operator
import sys
import xml.etree.cElementTree as ET
from enum import Enum

#current state of state-machine
currentState = None

#setting modulation cases
settings = {
            'NoCurrentFromDCCurrentSource'            : None,
            'NoSignalFromHeatDetectionSys'            : None,
            'StartRelayFailInOpenPosition'            : None,
            'NoSignalFromDetectionSystem'             : None,
            'NoSignalFromHeatDetectionSys'            : None,
            'PressureSwitchFailInClosedPos'           : None,
            'FusePlugsAreNotActivated'                : None,
            'FusePlug1DoesNotRespond'                 : None,
            'FusePlug2DoesNotRespond'                 : None,
            'FusePlug3DoesNotRespond'                 : None,
            'FusePlug4DoesNotRespond'                 : None,
            'NoSignalFromSmokeDetectionSys'           : None,
            'AtLeast2OfThe3SmokeDetectorsDontRespond' : None,
            'Combination1Fails'                       : None,
            'Combination2Fails'                       : None,
            'Combination3Fails'                       : None,
            'SmokeDetector1DoesntRespond'             : None,
            'SmokeDetector2DoesntRespond'             : None,
            'SmokeDetector3DoesntRespond'             : None,
            'NoSignalFromManualActSys'                : None,
            'ManualSwitchFallsToOpen'                 : None,
            'OperatorFailsToTakeAction'               : None    
           }
map = {
            0  : 'NoCurrentFromDCCurrentSource',           
            1  : 'NoSignalFromHeatDetectionSys',           
            2  : 'StartRelayFailInOpenPosition',           
            3  : 'NoSignalFromDetectionSystem',           
            4  : 'NoSignalFromHeatDetectionSys',          
            5  : 'PressureSwitchFailInClosedPos',          
            6  : 'FusePlugsAreNotActivated',                
            7  : 'FusePlug1DoesNotRespond',                 
            8  : 'FusePlug2DoesNotRespond',                 
            9 : 'FusePlug3DoesNotRespond',                
            10 : 'FusePlug4DoesNotRespond',                 
            11 : 'NoSignalFromSmokeDetectionSys',           
            12 : 'AtLeast2OfThe3SmokeDetectorsDontRespond', 
            13 : 'Combination1Fails',                       
            14 : 'Combination2Fails',                      
            15 : 'Combination3Fails',                       
            16 : 'SmokeDetector1DoesntRespond',             
            17 : 'SmokeDetector2DoesntRespond',             
            18 : 'SmokeDetector3DoesntRespond',             
            19 : 'NoSignalFromManualActSys',                
            20 : 'ManualSwitchFallsToOpen',                 
            21 : 'OperatorFailsToTakeAction'                   
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

def exitState(state):
    print()

try:
     tree = ET.parse('faultTree.xml')
     root = tree.getroot().find('NoSignalFromTheStartRelay')
     signal = root.find("NoCurrentFromDCCurrentSource")
     states['DC'] = True
     print(states['DC'])
except IOError as e:
    print ('\nERROR - cant find file: %s\n') % e	

#main function
def main(argv =sys.argv):
     if len(argv) > 1 and argv[1] == 'NoSignalFromTheStartRelay':
         while True:
             print('Choose case of modulation:\n')
             for idx, case in enumerate(map.values()):
                 print(idx,case)
             a = int(input())
             if a > len(map)-1:
                 print('incorrect number')             
     else:
         print('try again with \'NoSignalFromTheStartRelay\'')  

if __name__ == "__main__":
    main()
import os
import sys
import xml.etree.cElementTree as ET
from enum import Enum

currentState = None
states = {'DC' : False,
          'SR' : False,
          'PS' : False,
          'VU' : False,
          'MS' : False,
          'OP' : False,
          'FP1' : False,
          'FP2' : False,
          'FP3' : False,
          'FP4' : False,
          'SD1' : False,
          'SD2' : False,
          'SD3' : False}

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

def main(argv =sys.argv):
     if len(argv) > 1 and argv[1] == 'NoSignalFromTheStartRelay':
         print('FUCK')
     else:
         print('try again with \'NoSignalFromTheStartRelay\'')  

if __name__ == "__main__":
    main()
"""
MicroNFCBoard Python API

Copyright (c) 2014-2015 AppNearMe Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from time import sleep
from micronfcboard.board import MicroNFCBoard
from micronfcboard.transport import Transport
t = Transport()

board = MicroNFCBoard.getBoard()

if( board == None ):
    print("Board not found")
    exit()


t.open(board)

version, revision, boardId = t.info()
print("Connected to board id %s (version %d.%d)" % (boardId, version, revision) )

print("Blinking LEDs")
b = True
for i in range(0, 10): 
    t.leds( b, not b )
    b = not b
    sleep(0.2)
t.leds( False, False )

t.close()

exit()

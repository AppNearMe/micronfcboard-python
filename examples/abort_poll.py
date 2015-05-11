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

board = MicroNFCBoard.getBoard()

if( board == None ):
    print("Board not found")
    exit()

board.open()

print("Connected to board id %s (version %d.%d)" % (board.id, board.version[0], board.version[1]) )



for i in range(1,10):
    if not board.connected:
        print("Start polling")
        board.startPolling(True, False, False)
    j = 0
    while not board.polling:
        print("Wait")
    while board.polling:
        print(j)
        sleep(0.1)
        j+=1
        if j == 50:
            print("Stop polling")
            board.stopPolling()

print("Disconnnected")

board.close()

exit()

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

print("Start polling")
t.nfcPoll(True)

polling = False
connected = False
ndefPresent = False

while True:
    polling, connected, ndefPresent = t.status()
    if not polling:
        break
    sleep(0.1)

if connected:
    uid = t.nfcGetInfo()
    print("ISO A tag detected: UID %s" % (uid,))
    
if ndefPresent:
    url = t.nfcGetRecordData()
    print("URL: %s" % (url,))

print("End")
#t.reset(True)

t.close()

exit()

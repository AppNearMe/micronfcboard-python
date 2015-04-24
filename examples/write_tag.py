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
from micronfcboard.nfc.ndef import URIRecord, TextRecord, SmartPosterRecord, MIMERecord


board = MicroNFCBoard.getBoard()

if( board == None ):
    print("Board not found")
    exit()

board.open()

print("Connected to board id %s (version %d.%d)" % (board.id, board.version[0], board.version[1]) )

if not board.connected:
    print("Start polling")
    board.startPolling()

while board.polling:
    sleep(0.1)

if board.connected:
    if board.type2:
        atqa, sak, uid = board.getNfcInfo()
        print("ISO A tag detected: ATQS: %s, SAK: %s, UID %s" % (atqa, sak, uid,))
    elif board.p2p:
        print("P2P mode")   

ndefMessageWritten = False
ndefWritingStarted = False
while board.connected:
    if not ndefWritingStarted and board.ndefWriteable:
        print("Writing tag / SNEP Push")
        ndefWritingStarted = True
        board.ndefRecords = [SmartPosterRecord([URIRecord("http://www.appnearme.com/"), TextRecord("AppNearMe", "en")])]
        board.ndefWrite()
    if ndefWritingStarted and (not ndefMessageWritten) and (not board.ndefBusy):
        ndefMessageWritten = True
        if board.ndefSuccess:
            print("Tag write successful")
        else:
            print("Tag write failed")
    sleep(0.1)

print("Disconnnected")

board.close()

exit()

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
from array import array

from interface import INTERFACE, usb_backend
from transport import Transport

from nfc.ndef import URIRecord, TextRecord, SmartPosterRecord, MIMERecord

VID = 0x1FC9 #NXP VID
PID = 0x8039 #Attributed to AppNearMe

TARGET_FIRMWARE = (1,2)

STATUS_POLLING        = (1 << 0)
STATUS_CONNECTED      = (1 << 1)
STATUS_NDEF_PRESENT   = (1 << 2)

STATUS_TYPE1          = (1 << 8)
STATUS_TYPE2          = (2 << 8)
STATUS_TYPE3          = (3 << 8)
STATUS_TYPE4          = (4 << 8)

STATUS_INITIATOR      = (1 << 16)
STATUS_TARGET         = (0 << 16)

CHUNK_SIZE = 40

TEXT_ENCODING = {0: "utf-8", 1: "utf-16"}

class MicroNFCBoard(object):
    @staticmethod
    def getBoard(number = 0):
        a = INTERFACE[usb_backend].getAllConnectedInterface(VID, PID)
        if((a != None) and (len(a) > number)):
            return MicroNFCBoard(a[number])
        return None
    
    @staticmethod
    def getAllBoards():
        return [MicroNFCBoard(i) for i in INTERFACE[usb_backend].getAllConnectedInterface(VID, PID)]
    
    def __init__(self, intf):
        self._intf = intf
        self._transport = Transport()
        self._id = None
        self._version = None
        self._polling = False
        self._connected = False
        self._ndefMessagePresent = False
        self._ndefRecords = None
        self._ndefRead = False
        
    def open(self):
        self._transport.open(self._intf)
        version, revision, self._id = self._transport.info()
        self._version = (version, revision)
        
    def close(self):
        self._transport.close()
        
    @property
    def id(self):
        return self._id
    
    @property
    def connected(self):
        self._updateStatus()
        return self._connected
    
    @property
    def polling(self):
        self._updateStatus()
        return self._polling
    
    @property
    def ndefMessagePresent(self):
        self._updateStatus()
        return self._ndefMessagePresent
    
    @property
    def ndefRecords(self):
        self._updateStatus()
        if self._ndefMessagePresent and not self._ndefRead:
            self._ndefRecords = self._getNdefMessageRecords()
            self._ndefRecordsRead = True
        return self._ndefRecords
    
    @property
    def version(self):
        return self._version
    
    def getNfcInfo(self):
        return self._transport.nfcGetInfo()
    
    def reset(self):
        self._transport.reset(False)
        
    def startPolling(self):
        self._transport.nfcPoll(True)
        
    def stopPolling(self):
        self._transport.nfcPoll(True)
        
    def setLeds(self, led1, led2):
        self._transport.leds(led1, led2)
        
    def _updateStatus(self):
        status = self._transport.status()
        self._polling = (status & STATUS_POLLING) != 0
        self._connected = (status & STATUS_CONNECTED) != 0
        self._ndefMessagePresent = (status & STATUS_NDEF_PRESENT) != 0
        if not self._ndefMessagePresent:
            self._ndefRecordsRead = False
        
    def _getNdefRecords(self, start, count):
        records = []
        for recordNumber in range(start, start+count):
            #Get records info
            recordType, recordInfo = self._transport.nfcGetRecordInfo(recordNumber)
            funcs = {   0 : self._parseUnknownRecord,
                        1 : self._parseURIRecord,
                        2 : self._parseTextRecord,
                        3 : self._parseSmartPosterRecord,
                        4 : self._parseMIMERecord,
                    }
            record = funcs[recordType](recordNumber, recordInfo)
            if record != None:
                records += [record]
        return records
    
    def _getNdefMessageRecords(self):    
        #Get message count
        recordsCount = self._transport.nfcGetMessageInfo()
        return self._getNdefRecords(0, recordsCount)
    
    def _parseUnknownRecord(self, recordNumber, recordInfo):
        return None
    
    def _parseURIRecord(self, recordNumber, recordInfo):
        uriLength = recordInfo[0]
        uri = unicode(self._getRecordData(recordNumber, 0, uriLength).tostring(), "utf-8")
        return URIRecord(uri)
    
    def _parseTextRecord(self, recordNumber, recordInfo):
        encoding = TEXT_ENCODING[recordInfo[0]]
        languageCodeLength = recordInfo[1]
        textLength = recordInfo[2]
        languageCode = unicode(self._getRecordData(recordNumber, 0, languageCodeLength).tostring(), "utf-8")
        text = unicode(self._getRecordData(recordNumber, 1, textLength).tostring(), encoding)
        return TextRecord(text, languageCode)
    
    def _parseSmartPosterRecord(self, recordNumber, recordInfo):
        recordsStart = recordInfo[0]
        recordsCount = recordInfo[1]
        records = self._getNdefRecords(recordsStart, recordsCount)
        return SmartPosterRecord(records)
    
    def _parseMIMERecord(self, recordNumber, recordInfo):
        mimeTypeLength = recordInfo[0]
        dataLength = recordInfo[1]
        mimeType = unicode(self._getRecordData(recordNumber, 0, mimeTypeLength).tostring(), "utf-8")
        data = self._getRecordData(recordNumber, 1, dataLength)
        return MIMERecord(mimeType, data)
    
    def _getRecordData(self, recordNumber, item, itemLength):
        buf = array("B")
        while len(buf) < itemLength:
            chunkLength = min(CHUNK_SIZE, itemLength - len(buf))
            buf += self._transport.nfcGetRecordData(recordNumber, item, len(buf), chunkLength)
        return buf
            
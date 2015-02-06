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

from struct import pack, unpack
from array import array

COMMAND_ID = { 'GET_STATUS': 0x00, 'INFO': 0x01, 'RESET': 0x02, 'LEDS': 0x03,
                'NFC_POLL': 0x04, 'NFC_GET_INFO': 0x05, 'NFC_GET_MESSAGE_INFO': 0x06,
                'NFC_GET_RECORD_INFO': 0x07, 'NFC_GET_RECORD_DATA': 0x08,
               }

    
class BoardError(ValueError):
    pass

class Transport(object):
    def __init__(self):
        self.interface = None

    def open(self, interface):
        self.interface = interface
        self.interface.init()

    def close(self):
        self.interface.close()
        
    def reset(self, isp=False):
        cmd = [ COMMAND_ID['RESET'] ]
        if(isp):
            cmd.append(1)
        else:
            cmd.append(0)
        self.interface.write(cmd)
         
    def status(self):
        cmd = [ COMMAND_ID['GET_STATUS'] ]
        self.interface.write(cmd)
        resp = array('B', self.interface.read())
        if (resp[0] != COMMAND_ID['GET_STATUS']):
            raise BoardError('Device returned invalid command code %d' % resp[0])
        if resp[1] != 0:
            raise BoardError('Device returned %d' % resp[1])
        return unpack(">I", resp[2:6])[0]
         
    def nfcPoll(self, enable):
        cmd = [ COMMAND_ID['NFC_POLL'] ]
        if(enable):
            cmd.append(1)
        else:
            cmd.append(0)
        self.interface.write(cmd)
        resp = array('B', self.interface.read())
        if (resp[0] != COMMAND_ID['NFC_POLL']):
            raise BoardError('Device returned invalid command code %d' % resp[0])
        if resp[1] != 0:
            raise BoardError('Device returned %d' % resp[1])

    def nfcGetInfo(self):
        cmd = [ COMMAND_ID['NFC_GET_INFO'] ]
        self.interface.write(cmd)
        resp = array('B', self.interface.read())
        if (resp[0] != COMMAND_ID['NFC_GET_INFO']):
            raise BoardError('Device returned invalid command code %d' % resp[0])
        if resp[1] != 0:
            raise BoardError('Device returned %d' % resp[1])
        uidLength = resp[2]
        return "".join([ "%02X" % b for b in resp[3:3+uidLength]] )
        
    def nfcGetMessageInfo(self):
        cmd = [ COMMAND_ID['NFC_GET_MESSAGE_INFO'] ]
        self.interface.write(cmd)
        resp = array('B', self.interface.read())
        if (resp[0] != COMMAND_ID['NFC_GET_MESSAGE_INFO']):
            raise BoardError('Device returned invalid command code %d' % resp[0])
        if resp[1] != 0:
            raise BoardError('Device returned %d' % resp[1])
        return unpack(">H", resp[2:4])[0]
    
    def nfcGetRecordInfo(self, recordNumber):
        cmd = [ COMMAND_ID['NFC_GET_RECORD_INFO'] ]
        cmd += array('B', pack(">H", recordNumber))
        self.interface.write(cmd)
        resp = array('B', self.interface.read())
        if (resp[0] != COMMAND_ID['NFC_GET_RECORD_INFO']):
            raise BoardError('Device returned invalid command code %d' % resp[0])
        if resp[1] != 0:
            raise BoardError('Device returned %d' % resp[1])
        recordType = unpack(">H", resp[2:4])[0]
        recordInfo = [unpack(">H", resp[x:x+2])[0] for x in range(4,len(resp),2)]
        return recordType, recordInfo
        
    def nfcGetRecordData(self, recordNumber, item, offset, length):
        cmd = [ COMMAND_ID['NFC_GET_RECORD_DATA'] ]
        cmd += array('B', pack(">HBHH", recordNumber, item, offset, length))
        self.interface.write(cmd)
        resp = array('B', self.interface.read())
        if (resp[0] != COMMAND_ID['NFC_GET_RECORD_DATA']):
            raise BoardError('Device returned invalid command code %d' % resp[0])
        if resp[1] != 0:
            raise BoardError('Device returned %d' % resp[1])
        return resp[2:2+length]
        
    def info(self):
        cmd = [ COMMAND_ID['INFO'] ]
        self.interface.write(cmd)
        resp = array('B', self.interface.read())
        if (resp[0] != COMMAND_ID['INFO']):
            raise BoardError('Device returned invalid command code %d' % resp[0])
        if resp[1] != 0:
            raise BoardError('Device returned %d' % resp[1])
        version, revision = unpack(">HH", resp[2:6])
        return version, revision, "".join([ "%02X" % b for b in resp[6:6+5*4]] )
            
    def leds(self, led1, led2):
        cmd = [ COMMAND_ID['LEDS'] ]
        cmd += [ 1 if led1 == True else 0, 1 if led2 == True else 0 ]
        self.interface.write(cmd)
        resp = array('B', self.interface.read())
        if (resp[0] != COMMAND_ID['LEDS']):
            raise BoardError('Device returned invalid command code %d' % resp[0])
        if resp[1] != 0:
            raise BoardError('Device returned %d' % resp[1])

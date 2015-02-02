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

import logging
import array

COMMAND_ID = { 'GET_STATUS': 0x00, 'INFO': 0x01, 'RESET': 0x02, 'LEDS': 0x03,
                'NFC_POLL': 0x04, 'NFC_GET_INFO': 0x05, 'NFC_GET_RECORD': 0x06,
               }

def arrToBit32BE(arr):
    bytesArr=[0]*4
    for byte in range(0, 4):
        for bit in range(0, 8):
            if( (len(arr) > 8*byte+bit) and (arr[8*byte+bit] != 0) ):
              bytesArr[3-byte] |= 1 << bit
    return bytesArr

def bit32BEToArr(bytesArr):
    arr=[0]*32
    for byte in range(0, 4):
        for bit in range(0, 8):
            if( (bytesArr[3-byte] >> bit) & 1 != 0 ):
              arr[8*byte+bit] = 1
    return arr

def u32TobytesArr(u):
    return [(u >> 24) & 0xFF, (u >> 16) & 0xFF, (u >> 8) & 0xFF, (u >> 0) & 0xFF]

def bytesArrToU32(b):
    return (b[0] << 24) | (b[1] << 16) | (b[2] << 8) | (b[3] << 0)
    
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
        resp = self.interface.read()
        if (resp[0] != COMMAND_ID['GET_STATUS']):
            raise BoardError('Device returned invalid command code %d' % resp[0])
        if resp[1] != 0:
            raise BoardError('Device returned %d' % resp[1])
        polling = resp[2] & 1
        connected = resp[2] & 2
        ndefValid = resp[2] & 4
        return polling, connected, ndefValid
         
    def nfcPoll(self, enable):
        cmd = [ COMMAND_ID['NFC_POLL'] ]
        if(enable):
            cmd.append(1)
        else:
            cmd.append(0)
        self.interface.write(cmd)
        resp = self.interface.read()
        if (resp[0] != COMMAND_ID['NFC_POLL']):
            raise BoardError('Device returned invalid command code %d' % resp[0])
        if resp[1] != 0:
            raise BoardError('Device returned %d' % resp[1])

    def nfcGetInfo(self):
        cmd = [ COMMAND_ID['NFC_GET_INFO'] ]
        self.interface.write(cmd)
        resp = self.interface.read()
        if (resp[0] != COMMAND_ID['NFC_GET_INFO']):
            raise BoardError('Device returned invalid command code %d' % resp[0])
        if resp[1] != 0:
            raise BoardError('Device returned %d' % resp[1])
        uidLength = resp[2]
        return "".join([ "%02X" % b for b in resp[3:3+uidLength]] )
        
    def nfcGetRecordData(self):
        cmd = [ COMMAND_ID['NFC_GET_RECORD'] ]
        self.interface.write(cmd)
        resp = self.interface.read()
        if (resp[0] != COMMAND_ID['NFC_GET_RECORD']):
            raise BoardError('Device returned invalid command code %d' % resp[0])
        if resp[1] != 0:
            raise BoardError('Device returned %d' % resp[1])
        length = resp[2]
        if length == 0:
            return ""
        return "".join(map(chr,resp[3:3+length]) )
        
    def info(self):
        cmd = [ COMMAND_ID['INFO'] ]
        self.interface.write(cmd)
        resp = self.interface.read()
        if (resp[0] != COMMAND_ID['INFO']):
            raise BoardError('Device returned invalid command code %d' % resp[0])
        if resp[1] != 0:
            raise BoardError('Device returned %d' % resp[1])
        version = resp[2]
        revision = resp[3]
        return version, revision, "".join([ "%02X" % b for b in resp[4:4+5*4]] )
            
    def leds(self, led1, led2):
        cmd = [ COMMAND_ID['LEDS'] ]
        cmd += [ 1 if led1 == True else 0, 1 if led2 == True else 0 ]
        self.interface.write(cmd)
        resp = self.interface.read()
        if (resp[0] != COMMAND_ID['LEDS']):
            raise BoardError('Device returned invalid command code %d' % resp[0])
        if resp[1] != 0:
            raise BoardError('Device returned %d' % resp[1])
     
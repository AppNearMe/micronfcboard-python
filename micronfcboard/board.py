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
from interface import INTERFACE, usb_backend

VID = 0x1FC9 #NXP VID
PID = 0x8039 #Attributed to AppNearMe

class MicroNFCBoard(object):
    @staticmethod
    def getBoard(number = 0):
        a = INTERFACE[usb_backend].getAllConnectedInterface(VID, PID)
        if((a != None) and (len(a) > number)):
            return a[number]
        return None
    
    @staticmethod
    def getAllBoards():
        return INTERFACE[usb_backend].getAllConnectedInterface(VID, PID)
        
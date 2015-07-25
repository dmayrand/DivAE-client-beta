import json
import configparser
import socket
import threading
import os
import sys
import traceback
sys.path.append( "../lib" )
from iseclogger import Logger
from rpiinfo import get_temperature
import pdb


class PeripheralObject:
    serialid = None
    devid = None
    name = None
    description = None
    ptype = None
    

class LocalPeripherals:

    CFG_PERI_SECTION_MAIN="main"
    CFG_PERI_SECTION_PERI="peri_{0}"
    CFG_PERI_ID = "id"
    CFG_PERI_ID_SERIAL = "id_serial"
    CFG_PERI_NAME = "name"
    CFG_PERI_DESCRIPTION = "description"
    CFG_PERI_TYPE="type"
    CFG_PERI_COUNT="count"

    ST_DEV_NAME = "device_name"
    ST_DEV_ID = "device_id"
    ST_PERIPHERAL_ID = "peripheral_id"
    ST_DEV_SERIAL_ID = "device_serial_id"
    ST_DEV_TYPE = "device_type"
    ST_DEV_DESC = "device_desc"

    filename = "cfg/peripherals.cfg";
    
    log = None
    _peripherals = []
    
    def __init__(self, logger):
        self.log = logger
        
    def load(self):
        self._peripherals = []
        
        peri_config = configparser.ConfigParser()
        peri_config.read(self.filename)
        sectionmain = dict(peri_config.items(self.CFG_PERI_SECTION_MAIN))
 #       sectionmain[self.CFG_PERI_COUNT]
        pericount = int(sectionmain[self.CFG_PERI_COUNT]);
        for x in range(0,pericount):
            sectionkey = self.CFG_PERI_SECTION_PERI.format(x+1);
            sectionperi = dict(peri_config.items(sectionkey))
            pid = sectionperi[self.CFG_PERI_ID]
            pids = sectionperi[self.CFG_PERI_ID_SERIAL]
            pname = sectionperi[self.CFG_PERI_NAME]
            pdesc = sectionperi[self.CFG_PERI_DESCRIPTION]
            ptype = sectionperi[self.CFG_PERI_TYPE]
            self.addDevice(pid, pids, pname,pdesc,ptype);
        
        
        
 #       self.addDevice("00001","0","Blue Valve", "Relay 1 connected to blue valve","1")
#        self.addDevice("00002","1","Red Valve", "Relay 2 connected to red valve","1")

    PERI_TYPE_RELAY = "1";
    PERI_TYPE_TEMPERATURE = "204";
    STATUS = "status";

    def getPeripheralsStatus(self,peripheralcontroller):
        retval = [];
        for po in self._peripherals:
            if(po.ptype == self.PERI_TYPE_RELAY):
                status = peripheralcontroller.getPeripheralStatus(po.serialid)
                stat = {''+self.ST_PERIPHERAL_ID + '':'' + po.devid
                + '',''+self.STATUS + '':'' + status+''}
                retval.append(stat)
                
            elif(po.ptype == self.PERI_TYPE_TEMPERATURE):
                tempc = get_temperature();
                stat = {''+self.ST_PERIPHERAL_ID + '':'' + po.devid
                + '',''+self.STATUS + '':'' + tempc+''}
                retval.append(stat)
                
                

        return retval;

    def findPeripheral(self, deviceid):
        retval = None
        
        for po in self._peripherals:
            if po.devid == deviceid:
                retval = po
                break
        return retval

    def getPeripherals(self):
        return self._peripherals
                

    def addDevice(self, deviceid, serialid, name, description, ptype):
        po = PeripheralObject()
        po.devid = deviceid
        po.serialid = serialid
        po.name = name
        po.description = description
        po.ptype = ptype
        self._peripherals.append(po)

    def toJSON(self):
        retval = [];
        for po in self._peripherals:
            #po = self._peripherals[i]
            #self.log.write("locperi", po.name + po.devid)
            onePeri = { ''+self.ST_DEV_NAME+'':'' + po.name
                        + '',''+self.ST_DEV_ID + '':'' + po.devid+''
                        + '',''+self.ST_DEV_SERIAL_ID + '':'' + po.serialid+''
                        + '',''+self.ST_DEV_TYPE + '':'' + po.ptype+''
                        + '',''+self.ST_DEV_DESC + '':'' + po.description+''}
 #           self.log.write("locperi", json.dumps(onePeri))
            retval.append(onePeri)
        return retval #json.dumps(retval)
  


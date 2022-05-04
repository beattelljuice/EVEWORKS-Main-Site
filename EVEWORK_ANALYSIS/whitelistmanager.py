import time
from datetime import datetime
import json
from SCRIPTLIBRARIES.ESI4Py import esiobject_base_noauth as AUTHLESSESI




class WhiteListManager:
    def __init__(self):
        self.isbrandnewfile = False
        self.istooold = False
        self.dat=""
        self.checkspeed=30 #how frequently to check for a date change (in secconds)
        self.updatespeed=1 #0.00001157407 #how frequently to update the data (in days)
    def updatewhitelist(self):
        whitelisted_objects = {
                'Command Ship': 540, 
                'Combat Battlecruiser': 419, 
                'Attack Battecruiser': 0, 
                'Black Ops': 898, 
                'Marauder': 900, 
                'Battleship': 27, 
                'Capital Industrial Ship': 883, 
                'Supercarrier': 659, 
                'Carrier': 547, 
                'Dreadnought': 485, 
                'Force Auxiliary': 1538, 
                'Freighter': 513, 
                'Jump Freighter': 902, 
                'Titan': 30, 
                'Corvette': 237, 
                'Flag Cruiser': 1972, 
                'Heavy Assault Cruiser': 358,
                'Heavy Interdiction Cruiser': 894, 
                'Logistics': 832, 
                'Combat Recon Ship': 906, 
                'Force Recon Ship': 833, 
                'Strategic Cruiser': 963, 
                'Cruiser': 26, 
                'Command Destroyer': 1534, 
                'Interdictor': 541, 
                'Tactical Destroyer': 1305, 
                'Destroyer': 420, 
                'Assult Frigate': 0, 
                'Covert Ops': 830, 
                'Electronic Attack Ship': 893, 
                'Expedition Frigate': 1283, 
                'Interceptor': 831, 
                'Logistics Frigate': 1527, 
                'Frigate': 25, 
                'Deep Space Transport': 380, 
                'Blockade Runner': 1202, 
                'Industrial Command Ship': 941, 
                'Hauler': 28, 
                'Exhumer': 543, 
                'Mining Barge': 463, 
                'Shuttle': 31
        }
        whitelistedIDs = []
        for i in whitelisted_objects:
            whitelistedIDs += AUTHLESSESI.universe_groups_GROUPID(whitelisted_objects[i])["types"]
            #print(rawdata)
        #print(whitelistedIDs)
        f = open("whitelist.json", "r")
        self.dat = f.read()
        f.close()
        jsondat = json.loads(self.dat)
        jsondat["IDs"] = whitelistedIDs
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        jsondat["updated-time"] = date_time
        f = open("whitelist.json", "w")
        f.write(json.dumps(jsondat))
        f.close()


    def start(self):
        try:
            f = open("whitelist.json", "r")
            self.dat = f.read()
            f.close()
        except FileNotFoundError:
            self.isbrandnewfile = True
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            defaultform = {"updated-time":date_time,"IDs":[]}
            defaultJSONform = json.dumps(defaultform, indent = 4)
            #print(defaultJSONform)
            f = open("whitelist.json", "w")
            f.write(defaultJSONform)
            f.close()
        while True:
            print("Update Whitelist started")
            self.updatewhitelist()
            print(datetime.now().strftime("[%d/%m/%Y:%H:%M:%S] ")+"Whitelist updated")
            time.sleep(86400*self.updatespeed)
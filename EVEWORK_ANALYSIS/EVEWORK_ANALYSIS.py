#from whitelistmanager import WhiteListManager as WLM
from SCRIPTLIBRARIES.templatemanager import template_manager as TM
from SCRIPTLIBRARIES.ESI4Py import esiobject_base_noauth as AUTHLESSESI

import json
from datetime import datetime

def search_list(list,tosearchfor):
    found = False
    i = 0
    while found == False and i < len(list):
        if list[i] == tosearchfor:
            found = True
        i += 1
    return found


class EVEWORK_ANALYSIS:

    def __init__(self, DEBUG="",URI="", SCANCODE="", DSCAN="", LOCAL="", useDSCAN="", useLOCAL=""):
        self.DEBUG = DEBUG
        self.SCANCODE =SCANCODE
        self.DSCAN =DSCAN
        self.LOCAL =LOCAL
        self.useDSCAN =useDSCAN
        self.useLOCAL =useLOCAL
        self.URI=URI
        pass

    def DEBUG_print(self,toDEBUG_print):
        if self.DEBUG:
            print(toDEBUG_print)
            
    def DSCANAnalyse(self):
         self.DSCANAnalysePage = TM()

         # Format Variables to avoid throwing errors for being null
         if self.LOCAL == "":
             self.LOCAL = " "
         if self.DSCAN == "":
             self.DSCAN = " "

         # Format Checkbox Values
         if self.useDSCAN == "":
             self.useDSCAN = False
         if self.useDSCAN == "on":
             self.useDSCAN = True
         if self.useLOCAL == "":
             self.useLOCAL = False
         if self.useLOCAL == "on":
             self.useLOCAL = True

         self.DEBUG_print(self.useDSCAN)
         # Determine if user is creating a new scan or reading an existing scan
         if self.SCANCODE == "":



             # If scan type is selected and no scan data was provided 
             if self.DSCAN==" " and self.useDSCAN:
                 return "<meta http-equiv=\"Refresh\" content=\"0; url=\'http://"+self.URI+"/self.DSCAN\'\" />" 
             if self.LOCAL==" " and self.useLOCAL:
                 return "<meta http-equiv=\"Refresh\" content=\"0; url=\'http://"+self.URI+"/self.DSCAN\'\" />"
             # ----------- self.LOCAL SCAN DATA RELATED LOGIC -------------
             if self.useLOCAL:
                 # Do some formatting
                 self.LOCAL = self.LOCAL.replace("\r","")
                 self.LOCAL = self.LOCAL.split("\n")

                 # convert the list of self.LOCAL to ids and names 
                 self.LOCALLIST = AUTHLESSESI.bulk_names_to_ids(self.LOCAL)
                 self.DEBUG_print(self.LOCALLIST)

                 # Append all ids together on their own as a list
                 self.LOCAL_ID_LIST = []
                 for i in self.LOCALLIST:
                     self.LOCAL_ID_LIST += [i]

                 # Get list of corporations and alliance related to the people in self.LOCAL
                 self.LOCAL_ID_AFFILIATIONS = AUTHLESSESI.bulk_ids_to_affiliations(self.LOCAL_ID_LIST)

                 # Make a dictionary with the character names and their affiliations as ids
                 self.DEBUG_print(self.LOCAL_ID_AFFILIATIONS)
                 self.LOCAL_FULLY_LINKED_DATA = {}
                 for i in self.LOCALLIST:
                     current_affiliation_data = {}
                     for a in self.LOCAL_ID_AFFILIATIONS:
                         if i == a['character_id']:
                             current_affiliation_data = a
                     self.DEBUG_print(current_affiliation_data)
                     #self.DEBUG_print(self.LOCALLIST[2117617141])# += {}
                     self.DEBUG_print(current_affiliation_data)
                     try:
                         self.LOCAL_FULLY_LINKED_DATA[self.LOCALLIST[i]] = {"NAME":self.LOCALLIST[i],"CORPORATION":current_affiliation_data["corporation_id"],"ALLIANCE":current_affiliation_data["alliance_id"]}
                     except KeyError:
                         try:
                             self.LOCAL_FULLY_LINKED_DATA[self.LOCALLIST[i]] = {"NAME":self.LOCALLIST[i],"CORPORATION":current_affiliation_data["corporation_id"],"ALLIANCE":"NONE"}
                         except KeyError:
                             self.LOCAL_FULLY_LINKED_DATA["INVALID NAME"] = {"NAME": "INVALID NAME",
                                                                      "CORPORATION": "NONE", "ALLIANCE": "NONE"}

                 self.DEBUG_print(self.LOCAL_FULLY_LINKED_DATA)
                 # Make list of all the corporation and alliance ids for a reference dictionary, sort it into a list with no duplicates and retreive all their corresponding names
                 CORP_AND_ALLIANCE_ID_LIST = []
                 for i in self.LOCAL_FULLY_LINKED_DATA:
                     self.DEBUG_print(self.LOCAL_FULLY_LINKED_DATA[i])
                     self.DEBUG_print(i)
                     i_corp_data = self.LOCAL_FULLY_LINKED_DATA[i]["CORPORATION"]
                     if i_corp_data != "NONE":
                         CORP_AND_ALLIANCE_ID_LIST += [self.LOCAL_FULLY_LINKED_DATA[i]["CORPORATION"]]
                         i_alliance_data = self.LOCAL_FULLY_LINKED_DATA[i]["ALLIANCE"]
                         if i_alliance_data != "NONE":
                            CORP_AND_ALLIANCE_ID_LIST += [i_alliance_data]
                 CORP_AND_ALLIANCE_ID_LIST_SORTED = []
                 for i in CORP_AND_ALLIANCE_ID_LIST:
                     isfound = False
                     count = 0
                     maxcount = len(CORP_AND_ALLIANCE_ID_LIST_SORTED)
                     while isfound != True and count < maxcount:
                         if i == CORP_AND_ALLIANCE_ID_LIST_SORTED[count]:
                             isfound = True
                         count += 1
                     if isfound == False:
                         CORP_AND_ALLIANCE_ID_LIST_SORTED += [i]
                 self.DEBUG_print(CORP_AND_ALLIANCE_ID_LIST_SORTED)
                 unformated_corp_and_alliance_names =[]
                 if len(CORP_AND_ALLIANCE_ID_LIST_SORTED) > 0:
                     unformated_corp_and_alliance_names = (AUTHLESSESI.bulk_ids_to_names(CORP_AND_ALLIANCE_ID_LIST_SORTED))
                 FORMATTED_CORP_AND_ALLIANCE_NAMES = {"NONE":"NONE"}
                 for i in unformated_corp_and_alliance_names:
                     FORMATTED_CORP_AND_ALLIANCE_NAMES[i["id"]] = i["name"]
                 self.DEBUG_print(FORMATTED_CORP_AND_ALLIANCE_NAMES)
                 self.DEBUG_print(self.LOCAL_FULLY_LINKED_DATA)

                 # Apply id and name dictionary to update the main dictionary for presentation
                 for i in self.LOCAL_FULLY_LINKED_DATA:
                     self.LOCAL_FULLY_LINKED_DATA[i]['CORPORATION'] = FORMATTED_CORP_AND_ALLIANCE_NAMES[self.LOCAL_FULLY_LINKED_DATA[i]['CORPORATION']]
                     self.LOCAL_FULLY_LINKED_DATA[i]['ALLIANCE'] = FORMATTED_CORP_AND_ALLIANCE_NAMES[self.LOCAL_FULLY_LINKED_DATA[i]['ALLIANCE']]
                 self.DEBUG_print(self.LOCAL_FULLY_LINKED_DATA)
             else:
                 self.LOCAL_FULLY_LINKED_DATA = {}
             # ----------- DIRECTIONAL SCAN DATA RELATED LOGIC -------------
             filtered_ship_dictionary = {}
             if self.useDSCAN:
                 # Load up the ship id whitelist
                 f = open("EVEWORK_ANALYSIS/whitelist.json", "r")
                 whitelistIDs = json.loads(f.read())["IDs"]
                 f.close()
                 self.DEBUG_print(whitelistIDs)

                 # Parse Raw self.DSCAN data and put them into lists
                 self.DSCANparsed = self.DSCAN.split("\r\n")
                 shipnames = []
                 ids = []
                 for i in self.DSCANparsed:
                     thesplit = i.split("\t")
                     shipnames += [thesplit[2]]
                     ids += [thesplit[0]]

                 # Tally up items that have been self.DSCANned
                 shipdictionary = {}
                 for i in range(len(shipnames)):
                     try:
                         # Add to dictionary position if position exist
                         shipdictionary[shipnames[i]]["Quantity"] += 1
                     except KeyError:
                         # Position doesnt exist; lets create it
                         shipdictionary[shipnames[i]] = {"ID": ids[i], "Quantity":1}


                 # Filter out non whitelisted items
                 filtered_ship_dictionary = {}
                 for i in shipdictionary:
                     if search_list(whitelistIDs,int(shipdictionary[i]["ID"])) == True:
                         filtered_ship_dictionary[i] = {"ID":int(shipdictionary[i]["ID"]),"QUANTITY":shipdictionary[i]["Quantity"]}
             else:
                 filtered_ship_dictionary = {}

             finaldict = {"TIME":datetime.now().strftime("%d/%m/%Y @ %H:%M:%S"),"SCANDATA":filtered_ship_dictionary,"self.LOCALDATA":self.LOCAL_FULLY_LINKED_DATA}
             finaldict = json.dumps(finaldict)

             f = open("EVEWORK_ANALYSIS/dscans/count.dat", "r")
             currentcount = int(f.read())
             f.close()

             f = open("EVEWORK_ANALYSIS/dscans/count.dat", "w")
             f.write(str(currentcount+1))
             f.close()

             f = open("EVEWORK_ANALYSIS/dscans/"+str(currentcount)+".scan","w")
             f.write(finaldict)
             f.close()

             self.DSCANAnalysePage.load_html_template("EVEWORK_ANALYSIS/TEMPLATES/DSCAN-analysis-function-template.html")
             self.DSCANAnalysePage.format_html(["http://"+self.URI+"/dscanAnalyse?SCANCODE="+str(currentcount)])
             return self.DSCANAnalysePage.get_parsed_html()
         else:
             self.DSCAN_table =""
             f=open("EVEWORK_ANALYSIS/dscans/"+self.SCANCODE+".scan")
             scan_dictionary = json.loads(f.read())
             f.close()
             #self.DEBUG_print(filtered_ship_dictionary)
             for i in scan_dictionary["SCANDATA"]:
                 #self.DEBUG_print(filtered_ship_dictionary["SCANDATA"][i]["QUANTITY"])
                 self.DSCAN_table += ("<tr>")
                 self.DSCAN_table += ("<td>"+i+"</td>")
                 self.DSCAN_table += ("<td>"+str(scan_dictionary["SCANDATA"][i]["QUANTITY"])+"</td>")
                 self.DSCAN_table += ("</tr>")
             self.DSCANAnalysePage.load_html_template("EVEWORK_ANALYSIS/TEMPLATES/DSCAN-analysis-template.html")
             time_taken =scan_dictionary["TIME"]
             self.LOCAL_table = ""
             for i in scan_dictionary["self.LOCALDATA"]:
                 self.LOCAL_table += ("<tr>")
                 self.LOCAL_table += ("<td>"+i+"</td>")
                 self.LOCAL_table += ("<td>"+str(scan_dictionary["self.LOCALDATA"][i]["CORPORATION"])+"</td>")
                 self.LOCAL_table += ("<td>"+str(scan_dictionary["self.LOCALDATA"][i]["ALLIANCE"])+"</td>")
                 self.DSCAN_table += ("</tr>")
             self.DSCANAnalysePage.format_html([("http://"+self.URI+"/self.DSCANAnalyse?SCANCODE="+self.SCANCODE),time_taken,self.DSCAN_table,time_taken,self.LOCAL_table])
             return self.DSCANAnalysePage.get_parsed_html()
         #resultstable =""
         self.DEBUG_print(whitelistIDs[0])
         #filtered_ship_dictionary = {}
         #for i in shipdictionary:
         #    self.DEBUG_print(search_list(whitelistIDs,shipdictionary[i]["ID"]))
         #    if search_list(whitelistIDs,int(shipdictionary[i]["ID"])) == True:
         #        filtered_ship_dictionary[i] = {"ID":int(shipdictionary[i]["ID"]),"QUANTITY":shipdictionary[i]["Quantity"]}
         #        resultstable += ("<tr>")
         #        #resultstable += ("<td>"+"</td>")
         #        #resultstable += ("<td>"+shipdictionary[i]["ID"]+"</td>")
         #        resultstable += ("<td>"+i+"</td>")
         #        resultstable += ("<td>"+str(shipdictionary[i]["Quantity"])+"</td>")
         #        resultstable += ("</tr>")
         #self.DSCANAnalysePage.format_html([resultstable])
         self.DEBUG_print(filtered_ship_dictionary)
         #return self.DSCANAnalysePage.get_parsed_html()
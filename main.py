from SCRIPTLIBRARIES.ESI4Py import esiobject_base_noauth as AUTHLESSESI
from SCRIPTLIBRARIES.templatemanager import template_manager as TM
from EVEWORK_ANALYSIS.EVEWORK_ANALYSIS import EVEWORK_ANALYSIS as EA
from EVEWORK_ANALYSIS.whitelistmanager import WhiteListManager as WLM


import threading
import cherrypy

def whitelistholderfunc():
    Whitelist = WLM()
    Whitelist.start()


import os.path
from datetime import datetime
import json

def DEBUG_print(toDEBUG_print):
    if DEBUG:
        print(toDEBUG_print)

#def search_list(list,tosearchfor):
#    found = False
#    i = 0
#    while found == False and i < len(list):
#        if list[i] == tosearchfor:
#            found = True
#        i += 1
#    return found

class Mainsite(object):
    @cherrypy.expose
    def default(self, attr='abc'):
        return "<meta http-equiv=\"Refresh\" content=\"0; url=\'http://"+URI+"\'\" />"
    @cherrypy.expose
    def index(self):
        indexPage = TM()
        indexPage.load_html_template("TEMPLATES/index.html")
        return indexPage.get_parsed_html()
    @cherrypy.expose
    def dscan(self):
        dscanPage = TM()
        dscanPage.load_html_template("EVEWORK_ANALYSIS/TEMPLATES/dscan-template.html")
        #dscanPage.format_html(["yes","why"])
        return dscanPage.get_parsed_html()
    
    @cherrypy.expose
    def dscanAnalyse(self,SCANCODE="",DSCAN="",LOCAL="",useDSCAN="",useLOCAL=""):
        EAvar= EA(DEBUG,URI,SCANCODE,DSCAN,LOCAL,useDSCAN,useLOCAL)
        return EAvar.DSCANAnalyse()
        """""""""# Prepare Template Class
        dscanAnalysePage = TM()

        # Format Variables to avoid throwing errors for being null
        if LOCAL == "":
            LOCAL = " "
        if DSCAN == "":
            DSCAN = " "

        # Format Checkbox Values
        if useDSCAN == "":
            useDSCAN = False
        if useDSCAN == "on":
            useDSCAN = True
        if useLOCAL == "":
            useLOCAL = False
        if useLOCAL == "on":
            useLOCAL = True

        DEBUG_print(useDSCAN)
        # Determine if user is creating a new scan or reading an existing scan
        if SCANCODE == "":
            
            

            # If scan type is selected and no scan data was provided 
            if DSCAN==" " and useDSCAN:
                return "<meta http-equiv=\"Refresh\" content=\"0; url=\'http://"+URI+"/dscan\'\" />" 
            if LOCAL==" " and useLOCAL:
                return "<meta http-equiv=\"Refresh\" content=\"0; url=\'http://"+URI+"/dscan\'\" />"
            # ----------- LOCAL SCAN DATA RELATED LOGIC -------------
            if useLOCAL:
                # Do some formatting
                LOCAL = LOCAL.replace("\r","")
                LOCAL = LOCAL.split("\n")

                # convert the list of local to ids and names 
                LOCALLIST = AUTHLESSESI.bulk_names_to_ids(LOCAL)
                DEBUG_print(LOCALLIST)

                # Append all ids together on their own as a list
                LOCAL_ID_LIST = []
                for i in LOCALLIST:
                    LOCAL_ID_LIST += [i]
            
                # Get list of corporations and alliance related to the people in local
                LOCAL_ID_AFFILIATIONS = AUTHLESSESI.bulk_ids_to_affiliations(LOCAL_ID_LIST)

                # Make a dictionary with the character names and their affiliations as ids
                DEBUG_print(LOCAL_ID_AFFILIATIONS)
                LOCAL_FULLY_LINKED_DATA = {}
                for i in LOCALLIST:
                    current_affiliation_data = {}
                    for a in LOCAL_ID_AFFILIATIONS:
                        if i == a['character_id']:
                            current_affiliation_data = a
                    DEBUG_print(current_affiliation_data)
                    #DEBUG_print(LOCALLIST[2117617141])# += {}
                    DEBUG_print(current_affiliation_data)
                    try:
                        LOCAL_FULLY_LINKED_DATA[LOCALLIST[i]] = {"NAME":LOCALLIST[i],"CORPORATION":current_affiliation_data["corporation_id"],"ALLIANCE":current_affiliation_data["alliance_id"]}
                    except KeyError:
                        try:
                            LOCAL_FULLY_LINKED_DATA[LOCALLIST[i]] = {"NAME":LOCALLIST[i],"CORPORATION":current_affiliation_data["corporation_id"],"ALLIANCE":"NONE"}
                        except KeyError:
                            LOCAL_FULLY_LINKED_DATA["INVALID NAME"] = {"NAME": "INVALID NAME",
                                                                     "CORPORATION": "NONE", "ALLIANCE": "NONE"}
                
                DEBUG_print(LOCAL_FULLY_LINKED_DATA)
                # Make list of all the corporation and alliance ids for a reference dictionary, sort it into a list with no duplicates and retreive all their corresponding names
                CORP_AND_ALLIANCE_ID_LIST = []
                for i in LOCAL_FULLY_LINKED_DATA:
                    DEBUG_print(LOCAL_FULLY_LINKED_DATA[i])
                    DEBUG_print(i)
                    i_corp_data = LOCAL_FULLY_LINKED_DATA[i]["CORPORATION"]
                    if i_corp_data != "NONE":
                        CORP_AND_ALLIANCE_ID_LIST += [LOCAL_FULLY_LINKED_DATA[i]["CORPORATION"]]
                        i_alliance_data = LOCAL_FULLY_LINKED_DATA[i]["ALLIANCE"]
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
                DEBUG_print(CORP_AND_ALLIANCE_ID_LIST_SORTED)
                unformated_corp_and_alliance_names =[]
                if len(CORP_AND_ALLIANCE_ID_LIST_SORTED) > 0:
                    unformated_corp_and_alliance_names = (AUTHLESSESI.bulk_ids_to_names(CORP_AND_ALLIANCE_ID_LIST_SORTED))
                FORMATTED_CORP_AND_ALLIANCE_NAMES = {"NONE":"NONE"}
                for i in unformated_corp_and_alliance_names:
                    FORMATTED_CORP_AND_ALLIANCE_NAMES[i["id"]] = i["name"]
                DEBUG_print(FORMATTED_CORP_AND_ALLIANCE_NAMES)
                DEBUG_print(LOCAL_FULLY_LINKED_DATA)

                # Apply id and name dictionary to update the main dictionary for presentation
                for i in LOCAL_FULLY_LINKED_DATA:
                    LOCAL_FULLY_LINKED_DATA[i]['CORPORATION'] = FORMATTED_CORP_AND_ALLIANCE_NAMES[LOCAL_FULLY_LINKED_DATA[i]['CORPORATION']]
                    LOCAL_FULLY_LINKED_DATA[i]['ALLIANCE'] = FORMATTED_CORP_AND_ALLIANCE_NAMES[LOCAL_FULLY_LINKED_DATA[i]['ALLIANCE']]
                DEBUG_print(LOCAL_FULLY_LINKED_DATA)
            else:
                LOCAL_FULLY_LINKED_DATA = {}
            # ----------- DIRECTIONAL SCAN DATA RELATED LOGIC -------------
            filtered_ship_dictionary = {}
            if useDSCAN:
                # Load up the ship id whitelist
                f = open("EVEWORK-ANALYSIS/whitelist.json", "r")
                whitelistIDs = json.loads(f.read())["IDs"]
                f.close()
                DEBUG_print(whitelistIDs)
            
                # Parse Raw dscan data and put them into lists
                dscanparsed = DSCAN.split("\r\n")
                shipnames = []
                ids = []
                for i in dscanparsed:
                    thesplit = i.split("\t")
                    shipnames += [thesplit[2]]
                    ids += [thesplit[0]]
            
                # Tally up items that have been dscanned
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

            finaldict = {"TIME":datetime.now().strftime("%d/%m/%Y @ %H:%M:%S"),"SCANDATA":filtered_ship_dictionary,"LOCALDATA":LOCAL_FULLY_LINKED_DATA}
            finaldict = json.dumps(finaldict)

            f = open("EVEWORK-ANALYSIS/dscans/count.dat", "r")
            currentcount = int(f.read())
            f.close()

            f = open("EVEWORK-ANALYSIS/dscans/count.dat", "w")
            f.write(str(currentcount+1))
            f.close()

            f = open("dscans/"+str(currentcount)+".scan","w")
            f.write(finaldict)
            f.close()
            
            dscanAnalysePage.load_html_template("TEMPLATES/dscan-analysis-function-template.html")
            dscanAnalysePage.format_html(["http://"+URI+"/dscanAnalyse?SCANCODE="+str(currentcount)])
            return dscanAnalysePage.get_parsed_html()
        else:
            dscan_table =""
            f=open("dscans/"+SCANCODE+".scan")
            scan_dictionary = json.loads(f.read())
            f.close()
            #DEBUG_print(filtered_ship_dictionary)
            for i in scan_dictionary["SCANDATA"]:
                #DEBUG_print(filtered_ship_dictionary["SCANDATA"][i]["QUANTITY"])
                dscan_table += ("<tr>")
                dscan_table += ("<td>"+i+"</td>")
                dscan_table += ("<td>"+str(scan_dictionary["SCANDATA"][i]["QUANTITY"])+"</td>")
                dscan_table += ("</tr>")
            dscanAnalysePage.load_html_template("TEMPLATES/dscan-analysis-template.html")
            time_taken =scan_dictionary["TIME"]
            local_table = ""
            for i in scan_dictionary["LOCALDATA"]:
                local_table += ("<tr>")
                local_table += ("<td>"+i+"</td>")
                local_table += ("<td>"+str(scan_dictionary["LOCALDATA"][i]["CORPORATION"])+"</td>")
                local_table += ("<td>"+str(scan_dictionary["LOCALDATA"][i]["ALLIANCE"])+"</td>")
                dscan_table += ("</tr>")
            dscanAnalysePage.format_html([("http://"+URI+"/dscanAnalyse?SCANCODE="+SCANCODE),time_taken,dscan_table,time_taken,local_table])
            return dscanAnalysePage.get_parsed_html()
        #resultstable =""
        DEBUG_print(whitelistIDs[0])
        #filtered_ship_dictionary = {}
        #for i in shipdictionary:
        #    DEBUG_print(search_list(whitelistIDs,shipdictionary[i]["ID"]))
        #    if search_list(whitelistIDs,int(shipdictionary[i]["ID"])) == True:
        #        filtered_ship_dictionary[i] = {"ID":int(shipdictionary[i]["ID"]),"QUANTITY":shipdictionary[i]["Quantity"]}
        #        resultstable += ("<tr>")
        #        #resultstable += ("<td>"+"</td>")
        #        #resultstable += ("<td>"+shipdictionary[i]["ID"]+"</td>")
        #        resultstable += ("<td>"+i+"</td>")
        #        resultstable += ("<td>"+str(shipdictionary[i]["Quantity"])+"</td>")
        #        resultstable += ("</tr>")
        #dscanAnalysePage.format_html([resultstable])
        DEBUG_print(filtered_ship_dictionary)
        #return dscanAnalysePage.get_parsed_html()"""""



if __name__ == '__main__':
    # Load config
    URI = None
    DEBUG = None
    USE_ID_WHITELIST_UPDATER = None
    f = open("config.json", "r")
    config_data = json.loads(f.read())
    f.close()
    URI = config_data["URI"]
    DEBUG = config_data["DEBUG"]
    USE_ID_WHITELIST_UPDATER = config_data["USE ID WHITELIST UPDATER"]
    if (USE_ID_WHITELIST_UPDATER):
        WhitelistmanagerThread = threading.Thread(target=whitelistholderfunc)
        WhitelistmanagerThread.start()

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.config.update({'server.socket_port': 80})
    cherrypy.config.update({'server.socket_host': URI})
    cherrypy.quickstart(Mainsite(),'/',conf)

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

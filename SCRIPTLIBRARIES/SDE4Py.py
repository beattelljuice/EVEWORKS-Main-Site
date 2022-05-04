from typing import Type
import yaml
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
class SDE_Base:
    def __init__(self,sde_root_path):
        self.rootpath = "./"+sde_root_path
        self.hasloadedTypeIDs = False
        self.typeIDdata = ""

    def load_typeIDs(self,typeIDpath = "/fsd/typeIDs.yaml"):
        print("Opening "+self.rootpath+typeIDpath)
        f = open(self.rootpath+typeIDpath,"r")
        print("Saving Data")
        self.typeIDdata = f.read()
        print("File Closed")
        f.close()
        print("Parsing")
        self.typeIDdata = yaml.safe_load(self.typeIDdata)
        print("Loaded Successfully")

    def return_typeID_data(self,typeID):
        return self.typeIDdata[typeID]


#a = SDE_Base("sde/sde")
#a.load_typeIDs()
#print(a.typeIDdata)

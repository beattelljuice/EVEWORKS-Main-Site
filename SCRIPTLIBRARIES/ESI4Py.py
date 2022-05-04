import base64
from urllib import request, parse
import json
import datetime
import jwt

class esiobject_base:
    def urlencode(self,stringtoencode):
        #assess validity of inputs
        if not isinstance(stringtoencode,str):
            raise TypeError("Encoding string must be a STRING")

        #URL encode script to make it url friendly
        stringtoencode = stringtoencode.replace(" ","%20")
        stringtoencode = stringtoencode.replace("/","%2F")
        stringtoencode = stringtoencode.replace(":","%3A")
        return stringtoencode

    def __init__(self, ClientID, SecretKey,CallbackURL,Scopes,ValidationState,baseUrl = "https://login.eveonline.com/v2/oauth/authorize/?response_type=code&redirect_uri="):
        # assess validity of inputs
        if not isinstance(ClientID,str):
            raise TypeError("ClientID must be a STRING")
        if not isinstance(SecretKey,str):
            raise TypeError("SecretKey must be a STRING")
        if not isinstance(CallbackURL,str):
            raise TypeError("CallbackURL must be a STRING")
        if not isinstance(Scopes,str):
            raise TypeError("Scopes must be a STRING")
        if not isinstance(ValidationState,str):
            raise TypeError("ValidationState must be a STRING")
        if not isinstance(baseUrl,str):
            raise TypeError("baseUrl must be a STRING")

        #Define Handy Variables; set class wide standard variables
        self.baseUrl = baseUrl
        self.ValidationState = ValidationState
        self.ClientID = ClientID
        self.SecretKey = SecretKey
        self.CallbackURL = self.urlencode(CallbackURL)
        self.Scopes = self.urlencode(Scopes)
        self.expiry_time_error_margin = 10
        #Construct the redriect url so a function doesnt have to be called to "start the process"
        self.redirectURL = self.baseUrl+self.CallbackURL+"&client_id="+self.ClientID+"&scope="+self.Scopes+"&state="+self.ValidationState
        self.authcode = None
        self.refresh_token = None

        #ensure the datetime access token expiry variable is set properly
        self.access_token_expiry_datetime = datetime.datetime.now() - datetime.timedelta(seconds=10)

        #define variable in case it gets called later on
        self.jwt_token_data = None

    # -------------------------- Print Redirect URL for the inital part of the process getting the 'auth code' from esi (This is the player login redirect link) -------------------------- #
    def returnRedirectURL(self):
        return self.redirectURL

    # -------------------------- Generic Base64 Encoding Function -------------------------- #
    def base64encode(self,toencode):
        # assess validity of inputs
        if not isinstance(toencode,str):
            pass

        toencode_bytes = toencode.encode("ascii")
        toencode_bytes64 = base64.b64encode(toencode_bytes)
        toencode_bytes64_string = toencode_bytes64.decode("ascii")
        return toencode_bytes64_string

    # -------------------------- Retreive Refresh Token using auth code-------------------------- #
    def analyse_auth_code(self,authcode,base_url = "https://login.eveonline.com/v2/oauth/token"):
        # assess validity of inputs
        if not isinstance(authcode,str):
            raise TypeError("authcode must be a STRING")

        # construct the user pass key as per developer documentation
        user_pass = self.ClientID+":"+self.SecretKey
        self.encoded_user_pass = self.base64encode(user_pass)

        #contstruct auth header
        auth_header = "Basic " + str(self.encoded_user_pass)

        # construct headers
        form_headers = {
            "Authorization": auth_header
        }

        # construct form payload data
        form_values = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "login.eveonline.com",
            'grant_type': 'authorization_code',
            'code': authcode
        }

        #encode form values
        form_values = parse.urlencode(form_values).encode()
        #make request to esi and read data
        req = request.Request(base_url,data=form_values,headers=form_headers,method='POST')
        resp = request.urlopen(req)
        result = resp.read().decode('utf-8')
        result = json.loads(result)

        #Extract Refresh token and set it class wide
        self.refresh_token = result["refresh_token"]
        return self.refresh_token

    # -------------------------- Reset expiry time of access token; used mostly for debugging but also could come in handy for unexpected input issues. Can Also be called to force an access token reset -------------------------- #
    def manual_reset_access_token_expiry_time(self):
        self.access_token_expiry_datetime = datetime.datetime.now() - datetime.timedelta(seconds=10)

    # -------------------------- Decode the Access Token and store the retreived data -------------------------- #
    def decode_jwt(self,JWT=None,requesturl = "https://login.eveonline.com/oauth/jwks"):
        #validate data input
        if not self.is_access_token_valid():
            self.retreive_access_token()
        used_JWT = JWT
        if used_JWT==None:
            used_JWT = self.access_token
        token = used_JWT

        # Decode Token and parse the data we actually could potentially want (scopes and player name)
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        decoded_useful_token_data = {'scp':decoded_token['scp'],'name':decoded_token['name']}

        # store the wanted data
        self.jwt_token_data = decoded_useful_token_data
        return decoded_useful_token_data

    def retreive_access_token(self,refresh_token=None,ClientID=None,SecretKey=None,RequestUrl="https://login.eveonline.com/v2/oauth/token"):
        # check to see if access token is still valid; why get a new one when the current one works. Saves resources and network requests
        if (self.is_access_token_valid()):
            toreturn = self.access_token
        else:
            # assess validity of inputs regadrless if they were specified in the function or not
            used_refresh_token = refresh_token
            if refresh_token == None:
                used_refresh_token = self.refresh_token
            if self.refresh_token == None:
                raise TypeError("Refresh Token Not Set, Did you forget to set it with analyse_auth_code()?")
            if not isinstance(used_refresh_token, str):
                raise TypeError("refresh_token must be a STRING")

            used_ClientID = ClientID
            if ClientID == None:
                used_ClientID = self.ClientID
            if not isinstance(used_ClientID, str):
                raise TypeError("ClientID must be a STRING")

            used_SecretKey = SecretKey
            if SecretKey == None:
                used_SecretKey = self.SecretKey
            if not isinstance(used_SecretKey, str):
                raise TypeError("SecretKey must be a STRING")

            used_RequestUrl = RequestUrl
            if not isinstance(used_RequestUrl, str):
                raise TypeError("RequestURL must be a STRING")

            # Create user pass key as per documentation; base64 encode it
            user_pass = used_ClientID + ":" + used_SecretKey
            encoded_user_pass = self.base64encode(user_pass)
            auth_header = "Basic " + str(encoded_user_pass)

            # define the headers
            form_headers = {
                "Authorization": auth_header
            }

            # define the payload and encode it
            form_values = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "login.eveonline.com",
                'grant_type': "refresh_token",
                "refresh_token": used_refresh_token
            }
            form_values = parse.urlencode(form_values).encode()

            # Make Request to ESI
            req = request.Request(used_RequestUrl, data=form_values, headers=form_headers, method='POST')
            resp = request.urlopen(req)

            # Decode and store incoming data parsed into a dictionary from json
            result = resp.read().decode('utf-8')
            result = json.loads(result)

            # store access token class wide
            self.access_token = result["access_token"]

            # Calculate token expiry time and store it
            self.access_token_expiry_datetime = datetime.datetime.now() + datetime.timedelta(seconds=(int(result["expires_in"]) - self.expiry_time_error_margin))

            # Return the access token
            toreturn = result["access_token"]
        return toreturn
    # -------------------------- Import Refresh token into the class; so you dont have to get your users to reauth each time you need to get the refresh token -------------------------- #
    def LOADRefreshToken(self,Refresh_Token):
        # Validate Input
        if not isinstance(Refresh_Token,str):
            raise TypeError("Refresh_Token must be a STRING")

        # Set the refresh token globally and return it (cause why not)
        self.refresh_token=Refresh_Token
        return Refresh_Token

    # -------------------------- Determine if the access token has expired yet -------------------------- #
    def is_access_token_valid(self):
        # Validate if the expiry date time has been set properly
        if not isinstance(self.access_token_expiry_datetime,datetime.datetime):
            raise TypeError("Access Token Expiry Date Not Set Properly")

        # Calculate remaining time
        remaining_time = self.access_token_expiry_datetime-datetime.datetime.now()

        # Detect if the time remaining is above 0 (meaning there is still time left)
        isvalid = (remaining_time>datetime.timedelta(seconds=0))
        return isvalid

    def universe_types_TYPEID(self,ID):
        req = request.Request("https://esi.evetech.net/latest/universe/types/"+str(ID)+"/?datasource=tranquility&language=en")
        resp = request.urlopen(req)
        # Decode and store incoming data parsed into a dictionary from json
        result = resp.read().decode('utf-8')
        result = json.loads(result)
        return result

class esiobject_base_noauth:
    def __init__(self):
        pass
    def universe_types_TYPEID(ID):
        req = request.Request("https://esi.evetech.net/latest/universe/types/"+str(ID)+"/?datasource=tranquility&language=en")
        resp = request.urlopen(req)
        # Decode and store incoming data parsed into a dictionary from json
        result = resp.read().decode('utf-8')
        result = json.loads(result)
        return result
    def universe_groups_GROUPID(groupID):
        req = request.Request("https://esi.evetech.net/latest/universe/groups/"+str(groupID)+"/?datasource=tranquility&language=en")
        resp = request.urlopen(req)
        # Decode and store incoming data parsed into a dictionary from json
        result = resp.read().decode('utf-8')
        result = json.loads(result)
        return result
    
    def bulk_names_to_ids(name_list = []):
        payload = json.dumps(name_list)
        #print(payload)
        req = request.Request("https://esi.evetech.net/latest/universe/ids/?datasource=tranquility&language=en",data=payload.encode("ASCII"))
        resp = request.urlopen(req)
        result = resp.read().decode('utf-8')
        result = json.loads(result)
        try:
            result = result['characters']
        except KeyError:
            result = [{'id':0,'name':''}]
        toreturn = {}
        #print(result)
        for i in result:
            #print(i['name'])
            #print(i['id'])
            toreturn[i['id']] = i['name']
        return toreturn
    
    def bulk_ids_to_names(id_list=[]):
        payload = json.dumps(id_list)
        #print(payload)
        req = request.Request("https://esi.evetech.net/latest/universe/names/?datasource=tranquility",data=payload.encode("ASCII"))
        resp = request.urlopen(req)
        result = resp.read().decode('utf-8')
        result = json.loads(result)
        return result
        #result = result['characters']
        #toreturn = {}
        #print(result)
        #for i in result:
            #print(i['name'])
            #print(i['id'])
        #    toreturn[i['id']] = i['name']

    def bulk_ids_to_affiliations(ids = []):
        #print(ids[0])
        if (int(ids[0]) == 0):
            #print("Invalid Char ID")
            return [{'alliance_id': None, 'character_id': None, 'corporation_id': None}]
        else:
            #print("---")
            payload = json.dumps(ids)
            # print(payload)
            req = request.Request("https://esi.evetech.net/latest/characters/affiliation/?datasource=tranquility",
                                  data=payload.encode("ASCII"))
            resp = request.urlopen(req)
            result = resp.read().decode('utf-8')
            result = json.loads(result)
            #print(result)
            return result
            # result = result['characters']
            # toreturn = {}
            # print(result)
            # for i in result:
            #    #print(i['name'])
            #    #print(i['id'])
            #    toreturn[i['name']] = i['id']
            # return


    


#a = esiobject_base_noauth()
#print(a.universe_types_TYPEID(35835))
#print(esiobject_base_noauth.universe_groups_GROUPID(419))
#print(esiobject_base_noauth.bulk_names_to_ids(["aLagger Boi","Long Wiwi"]))
#print(esiobject_base_noauth.bulk_ids_to_affiliations([2114238787,2118047645]))
#esiobject_base_noauth.bulk_names_to_affiliations(["aLagger Boi","Long Wiwi"])
#print(esiobject_base_noauth.bulk_ids_to_names([98700935, 99011260, 98652614, 99010517, 98710824]))
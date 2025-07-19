
'''Info Header Start
Name : response
Author : Wieland@AMB-ZEPH15
Saveorigin : WebUtils.toe
Saveversion : 2022.32660
Info Header End'''

import json
from dataclasses import dataclass
from cookie import Cookie

@dataclass
class Response:
    statuscode      : int
    statusreason    : str
    header          : dict
    cookies         : list
    data            : any
    raw_data        : any

    def __init__(self, statuscode, statusreason, header_dict, raw_response):
        self.statuscode     = statuscode
        self.statusreason   = statusreason
        self.header         = { key.lower() : value for key, value in header_dict.items() }
        self.data			= Response._parse_response( raw_response )
        self.raw_data       = raw_response
        self.cookies        = [ Cookie( value ) for key,value in self.header.items() if key == "set-cookie" ]
    
    @staticmethod
    def _parse_response(raw_data):
        try:
            return json.loads( raw_data)
        except json.JSONDecodeError:
            pass
        return raw_data
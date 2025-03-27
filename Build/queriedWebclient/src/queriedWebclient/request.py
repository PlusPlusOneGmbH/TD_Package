
'''Info Header Start
Name : request
Author : Wieland@AMB-ZEPH15
Saveorigin : WebUtils.toe
Saveversion : 2022.32660
Info Header End'''

from dataclasses import dataclass
from urllib.parse import urlencode
import json
from cookie import Cookie
from typing import Callable, List

requestCallback = Callable[["Request", "Response", "extQueriedWebClient"],None]

@dataclass
class Request:
	method : str
	uri    : str
	header : dict
	query  : dict
	data   : any
	cookies : List[Cookie]
	#get generated dynamicly!
	#_td_request : any

	def __init__(self, server:str, method:str, uri:str = "/", query = {}, header = {}, cookies = [Cookie], data = None, callback = lambda request, response, server: None ):
		self.server  = server
		self.method  = method
		self.uri 	 = uri
		self.query 	 = query
		self.header  = { key.lower(): value for key,value in header.items() }
		self.cookies = cookies
		self.data    = data
		self.callback = callback
	
	def _get_content_type(self):
		if isinstance( self.data, (list, dict) ): return "application/json"
		elif isinstance(self.data, (bytes, bytearray)): return "application/octet-stream"
		elif isinstance(self.data, str): return "text/plain"
		return ""
	
	def _get_header(self):
		#first, lets add cookies!
		cleaned_header = {}
		cleaned_header.update( self.header )
		cleaned_header["cookie"] = "; ".join([f"{cookie.key}={cookie.value}" for cookie in self.cookies ])
		cleaned_header["content-type"] = self.header.get("content-type", self._get_content_type() )
		return cleaned_header

	def _get_data(self):
		try:
			return json.dumps( self.data )
		except (json.JSONDecodeError, TypeError):
			return self.data
		
	def _get_method(self):
		return self.method.upper()
	
	def _get_query(self):
		return self.query
	
	def _get_url(self):
		return f"{self.server.rstrip('/')}/{self.uri.lstrip('/')}" + f"?{urlencode(self.query)}"*bool(self.query)


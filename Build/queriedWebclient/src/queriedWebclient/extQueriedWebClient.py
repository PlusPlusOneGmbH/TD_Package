'''Info Header Start
Name : extQueriedWebClient
Author : Wieland@AMB-ZEPH15
Saveorigin : WebUtils.toe
Saveversion : 2022.32660
Info Header End'''

import json

from response import Response
from request import Request

import quriedwebclient_exceptions
from cookie import Cookie
from ambMultipart import Multipart
from typing import List, Callable, Dict, Union, Type

def default_callback(request:Request, response:Response, server:COMP):
	return None

requestData 	= Union[Dict, str, bytes]
requestCallback = Callable[[Request, Response, COMP],None]

class extQueriedWebClient:

	def __init__(self, ownerComp:COMP):
		# The component to which this extension is attached
		self.ownerComp:COMP			= ownerComp
		self.requests:list[Request]	= []
		self.active:bool			= False
		self.current_request:Request = None

		self.log = self.ownerComp.op("logger").Log

		self.Processing:bool						= tdu.Dependency( False )
		self.Exceptions 							= quriedwebclient_exceptions
		self.Cookie:Type[Cookie]					= Cookie
		self.Request_Class:Type[Request]			= Request
		self.Response_Class:Type[Response]			= Response
		self.Multipart:Type[Multipart]				= Multipart
	
	@property 
	def Server(self):
		return self.ownerComp.par.Server.eval()
	
	@property
	def _webclient(self) -> webclientDAT:
		return self.ownerComp.op("webclient")
	
	def Timeout(self):
		self._webclient.par.stop.pulse()
		self.log("Timeout", self.current_request._get_url() )
		self.ownerComp.op("callbackManager").Do_Callback("onTimeout", self.current_request, self.ownerComp)

		self.current_request = None
		self.active = False
		self._check_query()
	
	def _check_query(self):
		if self.active: return
		self.ownerComp.op("timeout").par.initialize.pulse()
		if not self.requests: 
			self.Processing.val = False
			return self.ownerComp.op("callbackManager").Do_Callback("onQueryEmpty", self.ownerComp)
		
		self.Processing.val = True
		self.active 		= True
		self.current_request = self.requests.pop(0)
		run( "me.ext.extQueriedWebClient._trigger_request()", fromOP=self.ownerComp, delayFrames = 1)
	
		
	def _parse_body(self, data):
		return json.dumps( data ) if type(data) is dict else data
	
	
	def _read_body(self, data):
		try:
			encoded_data = data.decode()
		except: 
			return data
		try:
			return json.loads(encoded_data)
		except:
			return encoded_data
		
	def _trigger_request(self):
		self.ownerComp.op("timeout").par.start.pulse()
		self.log("Running Request", self.current_request._get_url() )
		self.ownerComp.op("webclient").request(
					  self.current_request._get_url(),
					  self.current_request._get_method(),
			header 	= self.current_request._get_header(),
			data 	= self.current_request._get_data()
		)
	
	def _parse_response(self, status, headerDict, data):
		statusCode = status["code"]
		statusReason = status["message"]
		self.log("Getting Response", self.current_request, statusCode )
		#redirects and similiar should be ignored!
		if statusCode < 200 or 300 <= statusCode < 400: 
			self.log("Ignoring Response", statusReason)
			return

		current_request = self.current_request
		
		self.current_request = None
		
		response_item = Response(
			statusCode, statusReason, headerDict, data
		)

		if statusCode >= 400:
			exception = quriedwebclient_exceptions.get( statusCode )
			self.log("Failed Response!", statusCode, statusReason, current_request, response_item)
			self.ownerComp.op("callbackManager").Do_Callback("onError", current_request, 
																		response_item,
																		exception, 
																		self.ownerComp )
		else:
			self.ownerComp.op("callbackManager").Do_Callback("onResponse" , current_request,
																			response_item,
																			self.ownerComp )
			
			try:
				current_request.callback( current_request, response_item, self.ownerComp )
			except Exception as e:
				debug("Error in Request_Callback", e, current_request)
		
		#Set active AFTER callbacks, otherwise order of execution is borked!
		self.active = False
		self._check_query()
		return
	
	def _read_header(self):
		if self.ownerComp.par.Header.eval():
			return { row[0].val : row[1].val for row in self.ownerComp.par.Header.eval().rows() }
		return {}

	def QueryRequest(self, requestObject:Request):
		requestObject.header.update( self._read_header() )
		self.requests.append( requestObject )
		self._check_query()
		return requestObject

	
	def Get(self, 
		 endpoint:str, 
		 params:Dict[str,str] = {}, 
		 header:Dict[str,str] = {}, 
		 cookies:list[Cookie] = [], 
		 callback:requestCallback = default_callback) -> Request:
		return self.QueryRequest( 
			Request(
				self.Server,
				"GET",
				uri = endpoint,
				query = params,
				header = header,
				cookies = cookies,
				data = None,
				callback = callback
			)
		 )
			
	def Post(self, 
		  endpoint:str, 
		  params:Dict[str,str] = {}, 
		  header:Dict[str,str] = {}, 
		  cookies:list[Cookie] = [], 
		  data:requestData = None, 
		  callback:requestCallback = default_callback)-> Request:
		method = "POST"
		return self.QueryRequest( 
			Request(self.Server,method,uri = endpoint,query = params,header = header,cookies = cookies,data = data,callback = callback)
		 )
	
	def Put(self, 
		  endpoint:str, 
		  params:Dict[str,str] = {}, 
		  header:Dict[str,str] = {}, 
		  cookies:list[Cookie] = [], 
		  data:requestData = None, 
		  callback:requestCallback = default_callback)-> Request:
		method = "PUT"
		return self.QueryRequest( 
			Request(self.Server,method,uri = endpoint,query = params,header = header,cookies = cookies,data = data,callback = callback)
		 )
	
	def Patch(self, 
		  endpoint:str, 
		  params:Dict[str,str] = {}, 
		  header:Dict[str,str] = {}, 
		  cookies:list[Cookie] = [], 
		  data:requestData = None, 
		  callback:requestCallback = default_callback)-> Request:
		method = "PATCH"
		return self.QueryRequest( 
			Request(self.Server,method,uri = endpoint,query = params,header = header,cookies = cookies,data = data,callback = callback)
		 )
		
	def Delete(self, 
		  endpoint:str, 
		  params:Dict[str,str] = {}, 
		  header:Dict[str,str] = {}, 
		  cookies:list[Cookie] = [], 
		  data:requestData = None, 
		  callback:requestCallback = default_callback)-> Request:
		method = "DELETE"
		return self.QueryRequest( 
			Request(self.Server,method,uri = endpoint,query = params,header = header,cookies = cookies,data = data,callback = callback)
		 )
	
	def Search(self, 
		  endpoint:str, 
		  params:Dict[str,str] = {}, 
		  header:Dict[str,str] = {}, 
		  cookies:list[Cookie] = [], 
		  data:requestData = None, 
		  callback:requestCallback = default_callback)-> Request:
		method = "SEARCH"
		return self.QueryRequest( 
			Request(self.Server,method,uri = endpoint,query = params,header = header,cookies = cookies,data = data,callback = callback)
		 )

This component makes working with requests a little easier in introducing a somewhat async workflow by taking a request on  one after another with an extensive API. 
It makes life a little easier by autoparsing requests and responses to JSON.

## Parameters:

    Server : The base domain all requests will be appended to.
    Header: A TableDAT representing a Header that will be appended to every request where first col is the key, second col is the value.
    Timeout: How long to wait in seconds before closing the connection and executing the next request.
    Processing : A Toogle showing if the client is currently processing a request.


Attributes:

    Processing : Bool. Shows if the webclient is currently fetching data.
    Exceptions: A list of Exceptions.
    Request: The class-definition of the Request
    Response: The class-definition of the Response
    Cookie: The class-definition for a cookie.


    Multipart : ClassDefinition for multipart-formdata.

```python
multiPart = op("queriedWebclient").Multipart()
multiPart.AddField( "Key", "Value")
multiPart.AddFile( "Key", pathlib.Path( filepath ) )
content, header = multiPart.Parse()
op("queriedWebclient").Post( "endpoint", header = header, data = content)
```

Methods:
```python
Get( endpoint:str , params:dict = {}, header:dict = {}, cookies:list<Cookie> = [], callback:func<request, response, client_comp> = default_callback )
# Query a get request. Except endpoint everything else is optional.

Post/Put/Delete/Search( endpoint, params:dict = {} , header:dict = {}, cookies:list<Cookie> = [], data:any = None, callback:func<request, response, client_comp> = default_callback)
# Creates a Post/Put/Delete request. If the data is delivered as a dictionary, it will be converted to JSON and the apllicationtype Json will be applied to the header.

QueryRequest( request_object ) 
# Attaches a Request-Object and attaches it to the query. If no object is in the query it will start the request. Above functions are wrappers around this.

Request_Class( server:str, method:str, uri:str = "/", query:dict = {}, header:dict = {}, cookies:list<Cookie> = [], data:any = None, callback:func<lambda request, response, client_comp> = default_callback )
# Created a request-object that can be used in QueryRequest.

Cookie( cookie_str:str)
# Can be used to forge cookies, but you actually should just use the ones you already got in the response!
```

```python 
Class Members

class Request:
	method : str
	uri    : str
	header : dict
	query  : dict
	data   : any
	cookies : list

class Response:
    statuscode      : int
    statusreason    : str
    header          : dict
    cookies         : list
    data            : any
    raw_data        : any

class Cookie:
    key         : str
    value       : str 
    settings    : dict


```
For get one page of catbreeds from catfact.ninja and print it out call:

```python
op("queriedWebClient").Get("breeds", 
							params = {"limit" : 1},
							callback = lambda request, response, server: debug(response))
```

Callbacks:
```python
onResponse(request, response, client_comp): 
    """ Passes the request and the response on a good response. """
    pass

onError(request, response, client_comp ): 
    """ On error. Passes the request, response, an exception and the module with exceptions. """
    pass

onQueryEmpty(): 
    """Gets called when the last request in the current query resolved."""
    pass

onTimeout( request ): 
    """No response from the server during the timeout."""
    pass

```
Exceptions:
The onError-callbacks passes an exception-object that can be rissen and excepted to handle specific errors.
```python
try:
		raise error_exception( response["body"] )
	except exceptions.NotFound:
		#What happens when the endpoint cannot be found?
```

WebClientError : A general-purpose error.
UserError : The issues lies withing the request
ServerError : The issue comes from the server.

 - 400 : BadRequest,
 - 401 : Unauthorized,
 - 403 : Forbidden,
 - 404 : NotFound,
 - 405 : MethodNotAllowed,
 - 410 : Gone,
 - 500 : InternalServerError,
 - 501 : NotImplemented,
 - 502 : BadGateway,
 - 503 : ServiceUnavailable,
 - 504 : GatewayTimeout

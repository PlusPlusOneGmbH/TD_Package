
'''Info Header Start
Name : quriedwebclient_exceptions
Author : Wieland@AMB-ZEPH15
Saveorigin : WebUtils.toe
Saveversion : 2022.32660
Info Header End'''
class WebClientError(Exception):
    pass

class UserError(WebClientError):
    pass

#400
class BadRequest(UserError):
    pass

#401
class Unauthorized(UserError):
    pass

#403
class Forbidden(UserError):
    pass

#404
class NotFound(UserError):
    pass

#405 
class MethodNotAllowed(UserError):
    pass
    
class Timeout(UserError):
	pass
#410
class Gone(UserError):
    pass

###
class ServerError(WebClientError):
    pass

#500
class InternalServerError(ServerError):
    pass

#501
class NotImplemented(ServerError):
    pass

#502
class BadGateway(ServerError):
    pass

#503
class ServiceUnavailable(ServerError):
    pass

#504
class GatewayTimeout(ServerError):
    pass


exception_dict = {
    400 : BadRequest,
    401 : Unauthorized,
    403 : Forbidden,
    404 : NotFound,
    405 : MethodNotAllowed,
    410 : Gone,
    500 : InternalServerError,
    501 : NotImplemented,
    502 : BadGateway,
    503 : ServiceUnavailable,
    504 : GatewayTimeout
}
def get_default( code ):
    if 400 <= code <= 499: return UserError
    if 500 <= code <= 599: return ServerError
    return None

def get( code ):
    return exception_dict.get( code, get_default(code) )
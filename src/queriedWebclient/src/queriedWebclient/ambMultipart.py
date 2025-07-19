



'''Info Header Start
Name : ambMultipart
Author : Wieland@AMB-ZEPH15
Saveorigin : WebUtils.toe
Saveversion : 2022.32660
Info Header End'''

import mimetypes
from io import BytesIO
from pathlib import Path
strCodec = "ISO-8859-1"
class Multipart:
    def __init__(self) -> None:
        self.fields = []
        #self.boundary = f"---{str(uuid.uuid4()).replace('-', '')})"
        self.boundary = "nasudhUHBAKUDBdABHKJSDbvjajkdhasBD"
       

    def AddField(self, name:str, value:any):
        self.fields.append( {
            "header" : {
                "Content-Disposition": f'form-data; name="{name}"'
            },
            "content" : value
        } )

    def AddFile(self, name:str, filepath:Path):
        self.fields.append( {
            "header" : {
                "Content-Disposition": f'form-data; name="{name}"; filename="{filepath.name}"',
                "Content-Type" : mimetypes.guess_type( filepath )[0]
            },
            "content" : filepath.read_bytes()
        } )

    def boundaryPart(self, prefix = "", suffix = ""):
        return f"{prefix}{self.boundary}{suffix}\r\n".encode(strCodec)

    def Parse(self):
        body = BytesIO()

        for indQex, field in enumerate(self.fields):
            body.write( self.boundaryPart(prefix="--") )
            for key, value in field["header"].items():
                body.write( key.encode(strCodec) )
                body.write( ":".encode(strCodec) )
          
                body.write( value.encode(strCodec) )
                body.write( "\r\n".encode(strCodec) )
                
            body.write( "\r\n".encode(strCodec) )
            
            data = field["content"]
            if isinstance( data, int): data = str(data)
            if isinstance( data, str): data = data.encode( strCodec )
            body.write( data )
            body.write( "\r\n".encode(strCodec) )
            

        body.write( self.boundaryPart(prefix = "--", suffix="--") )
        return body.getvalue(), {
            "Content-Type" : f"multipart/form-data; boundary={self.boundary}"
        }
            
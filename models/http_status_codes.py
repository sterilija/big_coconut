from enum import Enum

class HTTPStatusCodes:
    Success = 200
    Created = 201
    WrongData = 400
    Unauthorized = 401
    NotFound = 404
    Conflict = 409
    ServerError = 500

print(HTTPStatusCodes.WrongData)
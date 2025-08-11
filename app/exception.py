from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    def __init__(self, detail="Not Found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ConflictException(HTTPException):
    def __init__(self, detail="Resource already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class BadRequestException(HTTPException):
    def __init__(self, detail="Bad Request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
class UnauthorizedException(HTTPException):
    def __init__(self, detail="Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenException(HTTPException):
    def __init__(self, detail="Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class InternalServerError(HTTPException):
    def __init__(self, detail="Server Error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

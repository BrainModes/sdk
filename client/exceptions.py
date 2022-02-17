class AuthenticationError(Exception):
    pass


class PayloadTypeError(Exception):
    pass


# Http Code Exception
# HTTP 400
class BadRequest(Exception):
    pass


# HTTP 401
class Unauthorized(Exception):
    pass


# HTTP 403
class Forbiden(Exception):
    pass


# HTTP 404
class NotFound(Exception):
    pass


# HTTP 409
class Conflict(Exception):
    pass


# HTTP 500
class InternalServerError(Exception):
    pass

class ApiError(Exception):
    pass

class MethodNotAllowed(Exception):
    pass


class HttpError(Exception):

    def __init__(self, response=None):
        if response is not None:
            self.response = response

    def __str__(self):
        try:
            return str(self.response.json()['errors'])
        except:
            return super(HttpError, self).__str__()


class HttpClientError(HttpError):
    pass

class HttpBadRequest(HttpClientError):
    pass

class HttpUnauthorized(HttpClientError):
    pass

class HttpForbidden(HttpClientError):
    pass

class HttpNotFound(HttpClientError):
    pass

class HttpMethodNotAllowed(HttpClientError):
    pass

class HttpServerError(HttpError):
    pass

class HttpInternalServerError(HttpServerError):
    pass

class HttpNotImplemented(HttpServerError):
    pass

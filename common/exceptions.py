class BadRequestException(Exception):
    def __init__(self, msg):
        self.msg = msg


class NotFoundException(Exception):
    def __init__(self, msg):
        self.msg = msg


class HTTPException(Exception):
    def __init__(self, msg):
        self.msg = msg


class ForbiddenException(Exception):
    def __init__(self, msg):
        self.msg = msg
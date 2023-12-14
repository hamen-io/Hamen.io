class HamenBaseException:
    """ Base class for all Hamen Build Errors """

class ReadOnlyError(HamenBaseException):
    """ Modified a read-only property """
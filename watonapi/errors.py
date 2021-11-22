class DisconnectedError(Exception):
    pass

class InvalidFormatError(Exception):
    pass

class CorruptedStreamError(Exception):
    pass

class AlreadyConnectedError(Exception):
    pass

class DispatcherIsStoppedError(Exception):
    pass

class UnknownAddressError(Exception):
    pass

class _NoSRVRecordError(Exception):
    pass

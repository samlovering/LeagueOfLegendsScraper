from threading import Lock

class AppState:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AppState, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.logger = None  # Will be set externally
        # Add other app state attributes here
        self._initialized = True

AppState = AppState()



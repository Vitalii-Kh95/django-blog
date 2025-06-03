from logging.handlers import RotatingFileHandler


class RequestCountRotatingHandler(RotatingFileHandler):
    def __init__(self, *args, max_requests=1000, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_requests = max_requests
        self._pair_state = 0
        self._request_count = 0

    def emit(self, record):
        msg = record.getMessage()
        if msg.startswith("Request:"):
            self._pair_state = 1
        elif msg.startswith("Response:") and self._pair_state == 1:
            self._pair_state = 0
            self._request_count += 1
            if self._request_count >= self.max_requests:
                self.doRollover()
                self._request_count = 0
        super().emit(record)

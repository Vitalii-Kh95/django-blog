import logging


class IgnoreStaticRequestsFilter(logging.Filter):
    def filter(self, record):
        try:
            msg = record.getMessage()
            return not any(
                [
                    "/static/" in msg,
                    "/media/" in msg,
                ]
            )
        except Exception:
            return True  # Don't block anything if something breaks

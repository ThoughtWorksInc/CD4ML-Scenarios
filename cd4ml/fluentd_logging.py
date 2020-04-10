import os
from fluent import sender

TENANT = os.getenv('TENANT', 'model')
FLUENTD_HOST = os.getenv('FLUENTD_HOST')
FLUENTD_PORT = os.getenv('FLUENTD_PORT')

print("FLUENTD_HOST="+FLUENTD_HOST)
print("FLUENTD_PORT="+FLUENTD_PORT)


class FluentdLogger:
    def __init__(self):
        self.logger = sender.FluentSender(TENANT, host=FLUENTD_HOST, port=int(FLUENTD_PORT))

    def log(self, event_label, event_payload):
        if FLUENTD_HOST is not None:
            if not self.logger.emit(event_label, event_payload):
                print("Could not log to Fluentd: {}".format(self.logger.last_error))
                self.logger.clear_last_error()

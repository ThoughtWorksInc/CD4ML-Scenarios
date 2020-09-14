import os
import logging
from fluent import sender


class FluentdLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        tenant = os.getenv('TENANT', 'model')
        fluentd_host = os.getenv('FLUENTD_HOST', '')
        fluentd_port = os.getenv('FLUENTD_PORT', '0')

        if fluentd_host == '' or fluentd_port == '0':
            self.logger.info("Fluentd logger is not configured, check your FLUENTD_HOST and FLUENTD_PORT environment "
                             "variables, not logging to fluentd")
            self.fluentd_logger = None
        else:
            self.fluentd_logger = sender.FluentSender(tenant, host=fluentd_host, port=int(fluentd_port))

    def log(self, event_label, event_payload):
        if self.fluentd_logger is None:
            return

        if not self.fluentd_logger.emit(event_label, event_payload):
            self.logger.warning("Could not log to Fluentd: {}".format(self.fluentd_logger.last_error))
            self.fluentd_logger.clear_last_error()

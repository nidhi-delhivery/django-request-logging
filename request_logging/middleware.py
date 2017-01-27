import logging
import re
from django.utils.termcolors import colorize

MAX_BODY_LENGTH = 50000  # log no more than 3k bytes of content
request_logger = logging.getLogger('django.request')


class LoggingMiddleware(object):

    def process_request(self, request):
        if (request.method == "POST"):
            request_logger.info(colorize("{} {}".format(request.method, request.get_full_path()), fg="cyan"))
            self.log_body(request.body)

    def process_response(self, request, response):
        return response

    def log_resp_body(self, response, level=logging.INFO):
        if (not re.match('^application/json', response.get('Content-Type', ''), re.I)):  # only log content type: 'application/xxx'
            return

        self.log_body(self.chunked_to_max(response.content), level)

    def log_body(self, msg, level=logging.INFO):
        request_logger.log(level, msg)

    def chunked_to_max(self, msg):
        if (len(msg) > MAX_BODY_LENGTH):
            return "{0}\n...\n".format(msg[0:MAX_BODY_LENGTH])
        else:
            return msg

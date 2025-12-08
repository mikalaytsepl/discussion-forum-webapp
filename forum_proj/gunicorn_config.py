import multiprocessing
import os
import logging
from gunicorn.glogging import Logger

bind = "0.0.0.0:8000"

# Run multiple workers to handle load and restart them if they freeze
workers = multiprocessing.cpu_count() * 2 + 1
# Use threads to handle concurrent requests (helpful for I/O bound Django apps)
threads = 2

# Restart workers after 1000 requests to prevent memory leaks from bloating the pod
max_requests = 1000
# Add jitter so all workers don't restart at the exact same time
max_requests_jitter = 50

# Limit the size of the HTTP request line (default is 4094, strict is safer)
limit_request_line = 4094
# Limit the number of headers (prevents header overflow attacks)
limit_request_fields = 100
# Limit the size of header fields
limit_request_field_size = 8190

# Workers silent for this long will be killed and restarted. #TODO On stage of architecture hardening
# timeout = 60 

# Keep-alive helps performance behind ALB.
keepalive = 5

# Ensure logs go to stdout/stderr so Kubernetes/CloudWatch collects them
accesslog = "-"
errorlog = "-"
loglevel = "info"
# Capture stdout/stderr from the application specifically
capture_output = True

class CustomLogger(Logger):
    def setup(self, cfg):
        super().setup(cfg)
        self.access_log.addFilter(StaticFilter())

class StaticFilter(logging.Filter):
    def filter(self, record):
        return '/static/' not in record.getMessage()

logger_class = CustomLogger
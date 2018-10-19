"""Django middleware for the prioritized batcher."""
from django.utils.deprecation import MiddlewareMixin

from .prioritized_batcher import PrioritizedBatcher


class Middleware(MiddlewareMixin):
    """Prioritized batcher middleware.

    Starts a batch before each request and commits the batch after each
    request.
    """

    def process_request(self, request):
        """Process a request."""
        PrioritizedBatcher.global_instance().start()

    def process_response(self, request, response):
        """Process a response."""
        batcher = PrioritizedBatcher.global_instance()
        if batcher.is_started:
            # May not be started due to strange middleware behavior on first request.
            batcher.commit()

        return response

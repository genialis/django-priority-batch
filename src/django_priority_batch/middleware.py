"""Django middleware for the prioritized batcher."""
import logging

from django.utils.deprecation import MiddlewareMixin

from .prioritized_batcher import PrioritizedBatcher

logger = logging.getLogger(__name__)


class Middleware(MiddlewareMixin):
    """Prioritized batcher middleware.

    Starts a batch before each request and commits the batch after each
    request.
    """

    def process_request(self, request):
        """Process a request."""
        batcher = PrioritizedBatcher.global_instance()
        if batcher.is_started:
            # This can happen in old-style middleware if consequent middleware
            # raises exception and thus `process_response` is not called.
            # Described under 3rd point of differences:
            # https://docs.djangoproject.com/en/1.11/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
            batcher.rollback()
            logger.warning(
                "Uncommited batcher transaction from previous request was rollbacked."
            )

        batcher.start()

    def process_response(self, request, response):
        """Process a response."""
        batcher = PrioritizedBatcher.global_instance()
        if batcher.is_started:
            # May not be started due to strange middleware behavior on first request.
            batcher.commit()

        return response

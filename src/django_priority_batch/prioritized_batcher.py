"""Prioritized batcher."""
import collections
import logging
import threading

from django.conf import settings

# Thread-local storage for the global batcher.
GLOBAL_BATCHER = threading.local()

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class PrioritizedBatcher:
    """Prioritized batcher."""

    def __init__(self, default_priority=1, priorities=None):
        """Construct a prioritized batcher."""
        self.default_priority = default_priority
        self.priorities = priorities or {}
        self.batch = None

    def __enter__(self):
        """Enter context manager."""
        self.start()
        return self

    def __exit__(self, *args):
        """Exit context manager."""
        self.commit()

    @classmethod
    def global_instance(cls):
        """Return a per-thread global batcher instance."""
        try:
            return GLOBAL_BATCHER.instance
        except AttributeError:

            instance = PrioritizedBatcher(
                **getattr(settings, 'PRIORITIZED_BATCHER', {})
            )
            GLOBAL_BATCHER.instance = instance
            return instance

    @property
    def is_started(self):
        """Whether a batch has been started."""
        return self.batch is not None

    def start(self):
        """Start a new batch."""
        assert (
            self.batch is None
        ), "Attempt to start() a batch before commit() of an open batch"
        self.batch = collections.OrderedDict()

    def commit(self):
        """Commit a batch."""
        assert self.batch is not None, "No active batch, call start() first"

        logger.debug("Comitting batch from %d sources...", len(self.batch))

        # Determine item priority.
        by_priority = []
        for name in self.batch.keys():
            priority = self.priorities.get(name, self.default_priority)
            by_priority.append((priority, name))

        for priority, name in sorted(by_priority, key=lambda key: key[0]):
            logger.debug("Processing items from '%s' (priority=%d)...", name, priority)
            items = self.batch[name]
            for handlers in items.values():
                for agg, handler in handlers:
                    try:
                        if agg is None:
                            handler()
                        else:
                            handler(agg)
                    except Exception as error:
                        # Log errors and proceed to evaluate the next handler.
                        logger.exception("Error while invoking handler.")

        self.batch = None

        logger.debug("Batch committed.")

    def rollback(self):
        """Rollback a batch."""
        assert self.batch is not None, "No active batch, call start() first"

        self.batch = None

    def add(self, name, handler, group_by=None, aggregator=None):
        """Add a new handler to the current batch."""
        assert self.batch is not None, "No active batch, call start() first"

        items = self.batch.setdefault(name, collections.OrderedDict())
        if group_by is None:
            # None is special as it means no grouping. In this case we must store all
            # the different handlers and call them all.
            items.setdefault(group_by, []).append((None, handler))
        elif aggregator is not None:
            agg = items.get(group_by, [(None, None)])[0][0]
            items[group_by] = [(aggregator(agg), handler)]
        else:
            items[group_by] = [(None, handler)]

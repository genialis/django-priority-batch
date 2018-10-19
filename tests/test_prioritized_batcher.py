from django_priority_batch import PrioritizedBatcher


def test_batch():
    results = []

    def simple_handler():
        results.append(1)

    batcher = PrioritizedBatcher()
    assert not batcher.is_started
    batcher.start()
    assert batcher.is_started
    batcher.add('test', simple_handler)
    batcher.add('test', simple_handler)
    batcher.add('test', simple_handler)
    batcher.commit()

    assert len(results) == 3
    assert not batcher.is_started


def test_simple_group_by():
    results = []

    def simple_handler():
        results.append(1)

    batcher = PrioritizedBatcher()
    batcher.start()
    batcher.add('test', simple_handler, group_by='group1')
    batcher.add('test', simple_handler, group_by='group2')
    batcher.add('test', simple_handler, group_by='group1')
    batcher.commit()

    assert len(results) == 2


def test_aggregation():
    results = []

    def simple_handler(agg):
        results.append(agg)

    def aggregate(value):
        def aggregator(state=None):
            if state is None:
                state = []

            state.append(value)
            return state

        return aggregator

    batcher = PrioritizedBatcher()
    batcher.start()
    batcher.add('test', simple_handler, group_by='group1', aggregator=aggregate(1))
    batcher.add('test', simple_handler, group_by='group2', aggregator=aggregate(2))
    batcher.add('test', simple_handler, group_by='group1', aggregator=aggregate(3))
    batcher.commit()

    assert results == [[1, 3], [2]]


def test_exception_in_handler():
    results = []

    def simple_handler():
        results.append(1)

    def exception_handler():
        raise Exception

    batcher = PrioritizedBatcher()
    batcher.start()
    batcher.add('test', simple_handler)
    batcher.add('test', exception_handler)
    batcher.add('test', simple_handler)
    batcher.commit()

    assert len(results) == 2


def test_priorities():
    results = []

    def simple_handler(value):
        def handler():
            results.append(value)

        return handler

    batcher = PrioritizedBatcher(priorities={'test1': 2, 'test2': 1})
    batcher.start()
    batcher.add('test1', simple_handler(1))
    batcher.add('test2', simple_handler(2))
    batcher.add('test1', simple_handler(3))
    batcher.commit()

    assert results == [2, 1, 3]


def test_context_manager():
    results = []

    def simple_handler():
        results.append(1)

    with PrioritizedBatcher() as batcher:
        batcher.add('test', simple_handler)

    assert len(results) == 1

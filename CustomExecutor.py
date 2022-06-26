from queue import Queue
from threading import Condition, Lock, Thread


class CustomExecutor:
    def __init__(self, max_workers: int):
        self.max_workers = max_workers
        self.workers = []
        self.threads = set()
        self.queue = Queue()
        self.lock = Lock()
        self.threads_queue = dict()

    def execute(self, func, *args, **kwargs):
        future = Future()
        work_item = WorkItem(future, func, args, kwargs)
        self.queue.put(work_item)
        threads_number = len(self.threads)
        if threads_number < self.max_workers:
            thread = Worker(queue=self.queue)
            thread.start()
            self.threads.add(thread)
            self.threads_queue[thread] = self.queue
        return future

    def map(self, func, *iterables):
        result = [self.execute(func, *args) for args in zip(*iterables)]
        if len(iterables) > 0:
            for i in range(len(iterables) - 1):
                result.pop()
        return result

    def shutdown(self):
        items = list(self.threads_queue.items())
        for thread, queue in items:
            queue.put(None)
            thread.join()


class Worker(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            work_item = self.queue.get(block=True)
            if work_item is None:
                return
            result = work_item.func(*work_item.args, **work_item.kwargs)
            work_item.future.set_result(result)


class WorkItem:
    def __init__(self, future, func, args, kwargs):
        self.future = future
        self.func = func
        self.args = args
        self.kwargs = kwargs


class Future(object):
    def __init__(self):
        self.condition = Condition()
        self.has_result = False
        self.result = None

    def get_result(self):
        self.condition.acquire()
        while not self.has_result:
            self.condition.wait(2)
        return self.result

    def set_result(self, result):
        self.condition.acquire()
        self.result = result
        self.has_result = True
        self.condition.notify_all()
        self.condition.release()

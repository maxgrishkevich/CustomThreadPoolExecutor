from queue import Queue
from threading import Thread
from time import sleep


class CustomExecutor:

    threads = []
    result = []
    queue = Queue()
    func = None

    def __init__(self, max_workers=None):
        for _ in range(max_workers):
            thread = Thread(target=self.run)
            thread.start()
            self.threads.append(thread)

    def shutdown(self):
        for _ in self.threads:
            self.queue.put(None)
        for thread in self.threads:
            thread.join()

    def execute(self, func, task):
        self.func = func
        self.queue.put(task)
        self.queue.join()

    def run(self):
        while True:
            task = self.queue.get()
            if task is None:
                break
            self.result.append(self.func(task))
            sleep(1)
            self.queue.task_done()

    def map(self, func, tasks):
        self.func = func
        for task in tasks:
            self.queue.put(task)
        self.queue.join()

    def get_results(self):
        return self.result

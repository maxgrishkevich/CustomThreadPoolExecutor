from threading import Thread


class CustomExecutor:

    threads = []
    is_running = True
    queue = []
    results = []

    def __init__(self, max_workers=None):
        for _ in range(max_workers):
            thread = Thread(target=Worker.run, args=[self], daemon=True)
            thread.start()
            self.threads.append(thread)

    def shutdown(self):
        while True:
            if False not in [item.future.hasResult for item in self.queue]:
                self.is_running = False
                [thread.join() for thread in self.threads]
                break

    def execute(self, func, task):
        item = WorkItem(func, task)
        self.queue.append(item)
        return item.future

    def map(self, func, tasks):
        results = []
        for task in tasks:
            item = WorkItem(func, task)
            self.queue.append(item)
            results.append(item.future)
        return results

    def get_item(self):
        for item in self.queue:
            if not item.is_running:
                item.is_running = True
                return item


class Worker(Thread):
    def run(self):
        while True:
            item = self.get_item()
            if item is not None:
                result = item.func(item.task)
                item.future.set_result(result)
            if not self.is_running:
                break


class WorkItem:
    def __init__(self, func, task):
        self.func = func
        self.task = task
        self.is_running = False
        self.future = Future()

    def __str__(self):
        return str(self.future.result)


class Future:
    def __init__(self):
        self.result = None
        self.hasResult = False

    def set_result(self, result):
        self.result = result
        self.hasResult = True

    def result(self):
        while self.hasResult is not True:
            pass
        return self.result

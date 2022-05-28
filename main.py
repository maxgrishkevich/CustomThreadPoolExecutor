from datetime import datetime
from time import sleep

from new import CustomExecutor


def func(task):
    sleep(1)
    return f'{datetime.now().strftime("%H:%M:%S")} - {task}'


tasks = [i for i in range(6)]
obj = CustomExecutor(max_workers=3)
results = obj.map(func, tasks)
for result in results:
    print(result.result())
obj.shutdown()

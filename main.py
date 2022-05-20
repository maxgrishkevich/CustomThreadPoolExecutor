from datetime import datetime
from CustomExecutor import CustomExecutor


def func(task):
    return f'{datetime.now().strftime("%H:%M:%S")} - {task}'


tasks = [i for i in range(12)]
obj = CustomExecutor(max_workers=4)
obj.map(func, tasks)
results = obj.get_results()
for result in results:
    print(result)
obj.shutdown()

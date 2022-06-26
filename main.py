from datetime import datetime
from time import sleep
from CustomExecutor import CustomExecutor


def func(task):
    sleep(1)
    return f'{datetime.now().strftime("%H:%M:%S")} - {task}'


def main():
    obj = CustomExecutor(max_workers=3)
    futures = obj.map(func, [i for i in range(6)])
    for f in futures:
        print(f.get_result())
    obj.shutdown()


if __name__ == '__main__':
    main()

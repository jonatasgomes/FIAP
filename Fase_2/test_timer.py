import time

def timer_n_recursive(n):
    for i in range(n, 0, -1):
        time.sleep(1)
        print(f'non recursive: {i}')

def timer_recursive(n):
    if n <= 0:
        return
    print(f'recursive: {n}')
    time.sleep(1)
    timer_recursive(n - 1)

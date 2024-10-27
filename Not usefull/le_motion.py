import time
import sys

print('\n')
RED = "\033[91m"
RESET = "\033[0m"


def ty(text, num, color):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(num)
    time.sleep(1 + num)


def loading(name):
    for _ in range(20):
        sys.stdout.write(f'\r{name}.')
        sys.stdout.flush()
        time.sleep(.1)
        sys.stdout.write(f'\r{name}..')
        sys.stdout.flush()
        time.sleep(.1)
        sys.stdout.write(f'\r{name}...')
        sys.stdout.flush()
        time.sleep(.1)
        sys.stdout.write('\r ')


# ty("Hello Nanao", .05, RED)
# sys.stdout.write('\r')
# ty("keidwrige?", 0, RESET)
# sys.stdout.write('\r')
# ty("Chak ka amta chadrabo?", .05, RED)
# sys.stdout.write('\r')
# ty("Hello Nanao", 0, RESET)
# sys.stdout.write('\r')
# ty("Hello Nanao", .05, RESET)


loading(RED + 'Loading')

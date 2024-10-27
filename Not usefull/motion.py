import sys
import time

for i in range(101):
    sys.stdout.write(f"\rProgress: {i}/100")
    # sys.stdout.flush()
    time.sleep(0.1)

print("\nDone!")

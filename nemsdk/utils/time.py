from datetime import datetime, timezone
import math

NEMESIS_EPOCH = int(datetime(2015, 3, 29, 0, 6, 25, tzinfo=timezone.utc).timestamp())


def get_current_nem_time():
    current_time = datetime.now().timestamp()
    return math.floor(current_time - NEMESIS_EPOCH)

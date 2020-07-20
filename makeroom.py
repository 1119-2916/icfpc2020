from util import (
    dem,
    to_list_rec,
)
from api import (
    send_message,
)

print(to_list_rec(send_message(dem("11011000011101000"))))

import os
import socket
from sys import platform
from dotenv import load_dotenv
load_dotenv()

PATH_DATA = os.environ["PATH_DATA"]

if platform == 'darwin':
    pass

if (socket.gethostname() == "macbook-pro-de-etienne.home"
   and os.environ["USERNAME_DESKTOP"] == "edmz"):
    pass

if __name__ == '__main__':
    print(PATH_DATA)

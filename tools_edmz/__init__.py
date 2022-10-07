import os
# import socket
# from sys import platform
from dotenv import load_dotenv
load_dotenv()
#
WHERE_WHO = os.environ["WHERE_WHO"]
if WHERE_WHO == "Workstation 10, Etienne":
    BASE_FOLDER_DATA = "/home/etienne.doumazane/data"
    BASE_FOLDER_FIGS = "/home/etienne.doumazane/figures"

elif WHERE_WHO == "Macbook, Etienne":
    BASE_FOLDER_DATA = "/Users/edmz/data/icm_data/"
    BASE_FOLDER_FIGS = "/Users/edmz/data/icm_data/"

else:
    BASE_FOLDER_DATA = ""
    BASE_FOLDER_FIGS = ""


# BASE_FOLDER_DATA = os.environ["BASE_FOLDER_DATA"]
# BASE_FOLDER_FIGS = os.environ["BASE_FOLDER_FIGS"]
#
# if platform == 'darwin':
#     pass
#
# if (socket.gethostname() == "macbook-pro-de-etienne.home"
#    and os.environ["USERNAME_DESKTOP"] == "edmz"):
#     pass
#
# if __name__ == '__main__':
#     print(PATH_DATA)



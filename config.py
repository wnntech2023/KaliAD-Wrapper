import os
from dotenv import load_dotenv
load_dotenv()

CONFIG = {
    "domain": os.getenv("DOMAIN"),
    "username": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD"),
    "dc_ip": os.getenv("DC_IP"),
}

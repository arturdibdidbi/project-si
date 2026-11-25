from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client["nha"]

usuarios = db["usuarios"]

bloqueio_config = db["bloqueio_config"]
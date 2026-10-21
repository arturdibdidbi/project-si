from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client["nha"]

usuarios = db["usuarios"]

usuarios = db["bloqueio_config"]
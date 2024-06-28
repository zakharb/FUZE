from motor.motor_asyncio import AsyncIOMotorClient
from app.config import DATABASE_URI

client = AsyncIOMotorClient(DATABASE_URI)
db = client['db']

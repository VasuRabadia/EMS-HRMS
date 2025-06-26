import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fd4c75b2aa0049c8b3faa225f752cdff')
    JWT_SECRET_KEY = os.getenv(
        'JWT_SECRET_KEY', 'f1a6ebddb5fd4c09b85c8696bfa7bb98')
    MONGO_URI = os.getenv(
        'MONGO_URI', 'mongodb://localhost:27017/Task-4')

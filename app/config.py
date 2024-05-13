# Base class for configuraton
class Config:
    SECRET_KEY = '9LDKjHtQCU-jUjvhMbNUXA'
    
    # DB settings
    SQLALCHEMY_DATABASE_URI = 'postgresql://chen0121:bleach54276@localhost/accessify_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MONGO_URI = 'mongodb://localhost:27017/yourmongodbname'
    
    PINECONE_API_KEY = 'your_pinecone_api_key_here'
    PINECONE_INDEX_URL = 'https://your-index-name.svc.your-region.pinecone.io'

class DevelopmentConfig(Config):
    DEBUG = True
  
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    keyspace: str = Field(..., env='ASTRADB_KEYSPACE')
    
    class Config:
        env_file = '.env'
    
    
def get_settings():
    return Settings()

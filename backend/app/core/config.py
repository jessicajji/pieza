from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Core application settings
    OPENAI_API_KEY: str

    # Qdrant settings
    QDRANT_URL: str
    QDRANT_API_KEY: str

    # eBay Compliance settings
    EBAY_VERIFICATION_TOKEN: str
    EBAY_COMPLIANCE_ENDPOINT_URL: str
    
    # eBay Environment
    EBAY_ENVIRONMENT: str = "sandbox"  # "sandbox" or "production"
    
    # eBay API credentials - Sandbox
    EBAY_CLIENT_ID_SANDBOX: str
    EBAY_CLIENT_SECRET_SANDBOX: str
    
    # eBay API credentials - Production
    EBAY_CLIENT_ID_PRODUCTION: str
    EBAY_CLIENT_SECRET_PRODUCTION: str
    
    # eBay API URLs - Sandbox
    EBAY_TOKEN_URL_SANDBOX: str
    EBAY_BASE_URL_SANDBOX: str
    
    # eBay API URLs - Production
    EBAY_TOKEN_URL_PRODUCTION: str
    EBAY_BASE_URL_PRODUCTION: str
    
    @property
    def ebay_client_id(self) -> str:
        """Get the appropriate client ID based on environment."""
        if self.EBAY_ENVIRONMENT == "production":
            return self.EBAY_CLIENT_ID_PRODUCTION
        else:
            return self.EBAY_CLIENT_ID_SANDBOX
    
    @property
    def ebay_client_secret(self) -> str:
        """Get the appropriate client secret based on environment."""
        if self.EBAY_ENVIRONMENT == "production":
            return self.EBAY_CLIENT_SECRET_PRODUCTION
        else:
            return self.EBAY_CLIENT_SECRET_SANDBOX
    
    @property
    def ebay_token_url(self) -> str:
        """Get the appropriate token URL based on environment."""
        if self.EBAY_ENVIRONMENT == "production":
            return self.EBAY_TOKEN_URL_PRODUCTION
        else:
            return self.EBAY_TOKEN_URL_SANDBOX
    
    @property
    def ebay_base_url(self) -> str:
        """Get the appropriate base URL based on environment."""
        if self.EBAY_ENVIRONMENT == "production":
            return self.EBAY_BASE_URL_PRODUCTION
        else:
            return self.EBAY_BASE_URL_SANDBOX
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 
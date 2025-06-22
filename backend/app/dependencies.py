from app.services.vector_db import VectorDBService

def get_vector_db_service() -> VectorDBService:
    """
    Dependency injector for the VectorDBService.
    Initializes the service with settings from the environment.
    """
    return VectorDBService() 
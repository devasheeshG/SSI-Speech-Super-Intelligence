# Path: ssi/types/new_client_connected.py
# Description: This module contains the NewClientConnected pydantic model, which represents a new client connection.

from pydantic import BaseModel

class NewClientConnected(BaseModel):
    client_id: str

import requests

from src.config.settings import AVIATIONSTACK_API_KEY


class AviationstackClient:

    BASE_URL = "https://api.aviationstack.com/v1"

    def __init__(self):
        self.api_key = AVIATIONSTACK_API_KEY

    def is_configured(self) -> bool:
        return bool(self.api_key)

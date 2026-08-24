import requests

from src.config.settings import AVIATIONSTACK_API_KEY


class AviationstackClient:

    BASE_URL = "https://api.aviationstack.com/v1"

    def __init__(self):
        self.api_key = AVIATIONSTACK_API_KEY

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def get_flights(self, flight_number: str) -> dict:
        response = requests.get(
            f"{self.BASE_URL}/flights",
            params={
                "access_key": self.api_key,
                "flight_iata": flight_number,
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

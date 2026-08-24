from src.integrations.aviationstack.client import AviationstackClient

client = AviationstackClient()

print("Aviationstack configured:", client.is_configured())
print("Aviationstack base URL:", client.BASE_URL)
print("\nCalling Aviationstack...")
result = client.get_flights("AI202")
print("\nAviationstack response:")
print(result)

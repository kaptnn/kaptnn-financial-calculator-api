import httpx
from app.core.config import configs

class AzureAuthService:
    @staticmethod
    async def get_access_token():
        token_url = f"https://login.microsoftonline.com/{configs.TENANT_ID}/oauth2/v2.0/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": configs.APPLICATION_ID,
            "client_secret": configs.CLIENT_SECRET,
            "scope": "https://graph.microsoft.com/.default"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            if response.status_code != 200:
                print(f"Token request failed: {response.text}")
                raise Exception("Failed to retrieve access token")
            token_data = response.json()
            return token_data.get("access_token")

    @staticmethod
    async def refresh_access_token(refresh_token: str):
        token_url = f"https://login.microsoftonline.com/{configs.TENANT_ID}/oauth2/v2.0/token"
        data = {
            "client_id": configs.APPLICATION_ID,
            "client_secret": configs.CLIENT_SECRET,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            response.raise_for_status()
            return response.json()

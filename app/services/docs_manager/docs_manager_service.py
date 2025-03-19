import httpx
from app.core.config import configs
from app.utils.msgraph import AzureAuthService

class OneDriveService:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        self.base_url = f"{configs.MS_GRAPH_BASE_URL}/me/drive"

    @classmethod
    async def init_service(cls):
        access_token = await AzureAuthService.get_access_token()
        return cls(access_token)

    async def list_root_folder(self):
        url = f"{self.base_url}/root/children"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json().get("value", [])

    async def upload_file(self, file_path: str, file_bytes: bytes):
        upload_url = f"{self.base_url}/root:/{file_path}:/content"
        async with httpx.AsyncClient() as client:
            response = await client.put(upload_url, headers=self.headers, content=file_bytes)
            response.raise_for_status()
            return response.json()

    async def get_files(self):
        url = f"{self.base_url}/root/children"
        print(f"Using access token: {self.access_token}")
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            print(response.text)
            response.raise_for_status()
            return response.json()

    async def delete_file(self, file_id: str):
        url = f"{self.base_url}/items/{file_id}"
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=self.headers)
            response.raise_for_status()
            return {"message": "File deleted successfully"}

from fastapi import APIRouter, UploadFile
from app.services.docs_manager.docs_manager_service import OneDriveService
from app.core.config import configs
from app.utils.msgraph import AzureAuthService

router = APIRouter(prefix="/document-managers", tags=["Document Manager"])

@router.get("/auth/login")
async def login():
    auth_url = f"https://login.microsoftonline.com/{configs.TENANT_ID}/oauth2/v2.0/authorize?" \
               f"client_id={configs.APPLICATION_ID}&response_type=code&redirect_uri={configs.REDIRECT_URI}&" \
               f"scope=Files.ReadWrite offline_access User.Read"
    return {"auth_url": auth_url}

@router.get("/auth/callback")
async def auth_callback():
    access_token = await AzureAuthService.get_access_token()
    return {"access_token": access_token}

@router.post("/upload")
async def upload_file(file: UploadFile):
    onedrive_service = await OneDriveService.init_service()
    file_bytes = await file.read()
    response = await onedrive_service.upload_file(file.filename, file_bytes)
    return response

@router.get("/files")
async def list_files():
    onedrive_service = await OneDriveService.init_service()
    response = await onedrive_service.get_files()
    return response

@router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    onedrive_service = await OneDriveService.init_service()
    response = await onedrive_service.delete_file(file_id)
    return response

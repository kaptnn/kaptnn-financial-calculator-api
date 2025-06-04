from msal import ConfidentialClientApplication
from app.core.config import configs
from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient

AUTHORITY = f"https://login.microsoftonline.com/{configs.TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]
MS_GRAPH_BASE_URL = configs.MS_GRAPH_BASE_URL

cred = ClientSecretCredential(
    client_id=configs.APPLICATION_ID,
    tenant_id=configs.TENANT_ID,
    client_secret=configs.CLIENT_SECRET
)

conf_app = ConfidentialClientApplication(
    client_id=configs.APPLICATION_ID,
    client_credential=configs.CLIENT_SECRET,
    authority=AUTHORITY
)
scope_msal = ["Files.Read"]

client = GraphServiceClient(credentials=cred, scopes=SCOPE)

def get_app_response() -> dict: 
    result = conf_app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" not in result:
        raise RuntimeError(f"MSAL error: {result.get('error_description')}")
    
    return result
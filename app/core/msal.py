from fastapi_msal import MSALAuthorization, MSALClientConfig, UserInfo
from msal import ConfidentialClientApplication, PublicClientApplication
from app.core.config import configs

AUTHORITY = f"https://login.microsoftonline.com/{configs.TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]
MS_GRAPH_BASE_URL = configs.MS_GRAPH_BASE_URL

conf_app = ConfidentialClientApplication(
    client_id=configs.APPLICATION_ID,
    client_credential=configs.CLIENT_SECRET,
    authority=AUTHORITY
)

fastapi_msal_conf = MSALClientConfig(
    client_id=configs.APPLICATION_ID,
    client_credential=configs.CLIENT_SECRET,
    tenant=configs.TENANT_ID,
)

fastapi_msal_auth = MSALAuthorization(client_config=fastapi_msal_conf)

def get_app_response() -> dict: 
    result = conf_app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" not in result:
        raise RuntimeError(f"MSAL error: {result.get('error_description')}")
    
    return result
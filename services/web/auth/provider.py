import logging

import requests
from msal import ConfidentialClientApplication
from project.config import settings

from .exceptions import (
    DiscoveryDocumentError,
    ProviderConnectionError,
    UnauthorizedUser,
)
from .model import ExternalAuthToken, ExternalUser
from .util import create_state_csrf_token

logger = logging.getLogger(__name__)


class AzureAuthProvider:
    """Azure authentication class for authenticating users and
    requesting user's information via and OpenIdConnect flow.
    """

    client_id = settings.AZURE_CLIENT_ID

    async def get_user(self, auth_token: ExternalAuthToken) -> ExternalUser:
        # Get Azure's endpoints from discovery document
        discovery_document = await self._get_discovery_document()
        try:
            token_endpoint = discovery_document["token_endpoint"]
            logger.info(f"end point token: {token_endpoint}")
            userinfo_endpoint = discovery_document["userinfo_endpoint"]
            logger.info(f"user info point: {userinfo_endpoint}")

        except KeyError as exc:
            raise DiscoveryDocumentError(f"Could not parse Azure's discovery document: {repr(exc)}")
        msal_client = ConfidentialClientApplication(
            settings.AZURE_CLIENT_ID,
            authority=settings.AZURE_AUTHORITY,
            client_credential=settings.AZURE_CLIENT_SECRET,
        )

        # Request access_token from Azure
        try:
            result = msal_client.acquire_token_by_authorization_code(
                auth_token.code,
                redirect_uri=settings.AZURE_REDIRECT_URL,
                scopes=["User.Read"],
            )
            access_token = result["access_token"]

        except Exception as exc:
            raise ProviderConnectionError(f"Could not get Azure's access token: {repr(exc)}")

        # Request user's information from Azure
        userinfo_response = requests.get(
            # Currently userinfo_endpoint only returns "sub". We need to use /v1.0/me for other info
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": "Bearer " + access_token},
        )

        response_data = userinfo_response.json()
        username = response_data.get("userPrincipalName")
        if not username:
            raise UnauthorizedUser("User account not verified by Azure.")

        email = response_data.get("mail")
        if not email:
            raise UnauthorizedUser("User account not verified by Azure.")

        sub_id = result["id_token_claims"]["sub"]

        external_user = ExternalUser(email=email, username=username, external_sub_id=sub_id)

        return external_user

    async def get_request_uri(self) -> str:
        msal_client = ConfidentialClientApplication(
            settings.AZURE_CLIENT_ID,
            authority=settings.AZURE_AUTHORITY,
            client_credential=settings.AZURE_CLIENT_SECRET,
        )

        state_csrf_token = await create_state_csrf_token()

        request_uri = msal_client.get_authorization_request_url(
            scopes=["User.Read"],
            state=state_csrf_token,
            redirect_uri=settings.AZURE_REDIRECT_URL,
        )

        return request_uri, state_csrf_token

    async def _get_discovery_document(self) -> dict:
        try:
            discovery_document = requests.get(settings.AZURE_DISCOVERY_URL).json()
        except Exception as exc:
            raise ProviderConnectionError(f"Could not get Azure's discovery document: {repr(exc)}")

        return discovery_document

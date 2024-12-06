#!/usr/bin/env python3
'''
conjur_client: This module contains functions and classes related to
               Conjur interactions to manage Corona secrets.cisco.com.
'''
__author__ = 'Ted Gauthier'
__email__ = 'tedg@cisco.com'
__version__ = '1.0.0'
import os
from urllib.parse import quote_plus
import logging
import requests

# Configure logging
logging.basicConfig()
logger = logging.getLogger('conjur_client ')
logger.setLevel(level=logging.INFO)


class ConjurError(Exception):
    """Custom Exception for Conjur-related errors."""
    pass


class ConjurConfig:
    '''Configuration handling for Conjur environment variables and defaults.'''

    @staticmethod
    def get_conjur_url():
        # return os.getenv("CONJUR_URL", "your_conjur_url.cisco.com")
        return os.getenv("CONJUR_URL", "https://conjur-nonprod-follower.cisco.com")

    @staticmethod
    def get_conjur_account():
        # return os.getenv("CONJUR_ACCT", "your_conjur_account")
        return os.getenv("CONJUR_ACCT", "cisco")

    @staticmethod
    def get_conjur_username():
        # return os.getenv('CONJUR_USERNAME', 'your_conjur_username')
        return os.getenv("CONJUR_USERNAME", "host/it/tedgcisco-gen_conjur_namespace/tutorial-tedgcisco-gen/webapp")

    @staticmethod
    def get_conjur_api_key():
        # return os.getenv('CONJUR_API_KEY', 'your_conjur_api_key')
        return os.getenv("CONJUR_API_KEY", "3098bvs1cj1792btg3p5vwh7hm30e96b9143tqxt232d0pxt0djr8")

    @staticmethod
    def get_conjur_app_username():
        # return os.getenv('CONJUR_APP_USERNAME', 'your_conjur_app_username')
        return os.getenv("CONJUR_APP_USERNAME", "it/tedgcisco-gen_conjur_namespace/tutorial-tedgcisco-gen/app-username")

    @staticmethod
    def get_conjur_app_password():
        # return os.getenv('CONJUR_APP_PASSWORD', 'your_conjur_app_password')
        return os.getenv("CONJUR_APP_PASSWORD", "it/tedgcisco-gen_conjur_namespace/tutorial-tedgcisco-gen/app-password")


class ConjurClient:
    def __init__(self, url: str, account: str, username: str, api_key: str):
        self.url = url.rstrip('/')
        self.account = quote_plus(account)
        self.token = None

        # Authenticate to Conjur and get a base64-encoded token.
        try:
            username_encoded = quote_plus(username)
            auth_url = f"{self.url}/authn/{self.account}/{username_encoded}/authenticate"
            headers = {"Accept-Encoding": "base64"}
            response = requests.post(auth_url, data=api_key, headers=headers)
            response.raise_for_status()
            self.token = response.text
            logger.debug("Successfully authenticated to Conjur.")

        except requests.exceptions.RequestException as e:
            logger.error("Error during Conjur authentication: %s", e)
            raise ConjurError("Authentication failed.") from e

    def get_secret(self, identifier: str) -> str:
        """
        Retrieve a single secret from Conjur.
        """
        if not self.token:
            raise ConjurError("Token is missing. Please authenticate first.")
        
        try:
            identifier_encoded = quote_plus(identifier)
            secret_url = f"{self.url}/secrets/{self.account}/variable/{identifier_encoded}"
            headers = {"Authorization": f'Token token="{self.token}"'}
            response = requests.get(secret_url, headers=headers)
            response.raise_for_status()
            logger.debug("Secret %s retrieved successfully.", identifier)
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error("Error retrieving secret '%s': %s", identifier, e)
            raise ConjurError(f"Failed to retrieve secret: {identifier}") from e


if __name__ == "__main__":

    # Initialize client
    client = ConjurClient(url=ConjurConfig.get_conjur_url(), 
                          account=ConjurConfig.get_conjur_account(), 
                          username=ConjurConfig.get_conjur_username(), 
                          api_key=ConjurConfig.get_conjur_api_key())

    try:
        # Authenticate and retrieve secrets
        # token = client.authenticate(username=conjur_username, api_key=conjur_api_key)
        app_username = client.get_secret(ConjurConfig.get_conjur_app_username())
        app_password = client.get_secret(ConjurConfig.get_conjur_app_password())

        # Output retrieved secrets
        logger.info("App Username: %s", app_username)
        logger.info("App Password: %s", app_password)
 
    except ConjurError as e:
        logger.error("Conjur operation failed: %s", e)

"""Core API client for Corona REST API interactions."""

import sys
import time
import logging
import requests

from .config import CoronaConfig
from .exceptions import CoronaError

# Configure logging
logging.basicConfig()
logger = logging.getLogger('upload_spdx')
logger.setLevel(level=logging.INFO)

MAX_REQ_TIMEOUT = 120  # requests default timeout = 120 seconds


class CoronaAPIClient:
    """Base client for authenticated Corona API requests."""

    def __init__(self, host, user_name):
        """
        Initialize Corona API client.

        Args:
            host: Corona API host
            user_name: Corona username for authentication
        """
        self.host = host
        self.user_name = user_name
        self.token = None
        self.pat = None

    def get_auth_token(self):
        """
        Get Bearer token using the PAT (Personal Access Token).

        Returns:
            str: Authentication token

        Raises:
            CoronaError: If token retrieval fails
        """
        if not self.token:
            try:
                # Corona PAT (Personal Access Token for self.user_name)
                self.pat = CoronaConfig.get_corona_pat()

                pat_header = {
                    'user': {
                        'username': self.user_name,
                        'pat': self.pat
                    }
                }
                msg = f'>>>TEST>>> sign_in, pat_header = {pat_header}/n'
                logger.debug(msg)

                sign_in_res = requests.post(
                    f'https://{self.host}/api/auth/sign_in',
                    json=pat_header
                )
                sign_in_res.raise_for_status()
                self.token = sign_in_res.json().get('token')

                msg = (f'>>>TEST>>> sign_in, pat_header = {pat_header}, '
                       f'API token = {self.token}/n')
                logger.debug(msg)

                if not self.token:
                    raise CoronaError(
                        'Failed to retrieve token from response.')
            except requests.exceptions.RequestException as e:
                raise CoronaError(
                    f'Error obtaining auth token: {e}') from e
            except Exception as e:
                raise CoronaError(f'Error: {e}') from e

        return self.token

    def make_authenticated_request(self, method, endpoint, data=None,
                                    files=None, retries=3):
        """
        Helper function to make authenticated API requests with retry.

        Args:
            method: API method (GET or POST)
            endpoint: API endpoint being invoked
            data: JSON data, defaults to None
            files: Files to upload, defaults to None
            retries: Number of retry attempts

        Returns:
            API request response converted to JSON

        Raises:
            CoronaError: If request fails after all retries
        """
        self.get_auth_token()
        headers = {'Authorization': f'Bearer {self.token}'}
        url = f'https://{self.host}/{endpoint}'

        for attempt in range(retries):
            try:
                msg = f'>>>TEST>>> headers = {headers}, url = {url}/n'
                logger.debug(msg)

                response = requests.request(
                    method,
                    url,
                    headers=headers,
                    json=data,
                    files=files,
                    timeout=MAX_REQ_TIMEOUT
                )
                response.raise_for_status()
                return response.json()

            except requests.exceptions.HTTPError as e:
                if response.status_code in [429, 500, 502, 503, 504]:
                    msg = (f'Temporary server error ({response.status_code})'
                           f'. Retrying... ({attempt + 1}/{retries})')
                    logger.warning(msg)
                    time.sleep(2 ** attempt)
                else:
                    self._handle_error(e, response, f'requesting {endpoint}')
                    break

            except requests.exceptions.RequestException as e:
                msg = (f'Network error: {e}. Retrying... '
                       f'({attempt + 1}/{retries})')
                logger.warning(msg)
                time.sleep(2 ** attempt)

        raise CoronaError(
            f'Failed to perform request to {endpoint} after '
            f'{retries} attempts'
        )

    def _handle_error(self, e, response, action):
        """
        Handle API errors for make_authenticated_request().

        Args:
            e: Exception that occurred
            response: HTTP response object
            action: Description of the action being performed
        """
        error_messages = {
            401: f'Unauthorized access while {action}. '
                 f'Invalid PAT or token.',
            422: f'Invalid request during {action}. '
                 f'Ensure that the name is unique.',
        }
        msg = (f">>_handle_error_TEST>> e = '{e}' \n"
               f"response = '{response.json()}'")
        logger.debug(msg)

        msg = error_messages.get(
            response.status_code,
            f'Error {action}: {response.status_code} ({response.text})'
        )
        logger.fatal(msg)
        sys.exit(response.status_code)

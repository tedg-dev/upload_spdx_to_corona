#!/usr/bin/env python3
'''
upload_spdx: This module contains functions and classes related to 
             Corona REST API interactions and
             uploading an SPDX document file to Corona.

NOTE: logger messaging is pre-formatted and confined to a single line, e.g., 
        msg = f"blah '{var1}' blah '{var2}'"; logger.info(msg)
'''
__author__ = 'Ted Gauthier'
__email__ = 'tedg@cisco.com'
__version__ = '1.0.0'
import os
import sys
import time
import argparse
import logging
import requests

# Configure logging
logging.basicConfig()
logger = logging.getLogger('upload_spdx ')
logger.setLevel(level=logging.INFO)

MAX_REQ_TIMEOUT = 120    # requests default timeout = 120 seconds


class CoronaConfig:
    '''Configuration for Corona-related environment variables and defaults.'''

    @staticmethod
    def get_corona_pat():
        # return os.getenv('CORONA_PAT', 'your_corona_pat_here')
        return os.getenv('CORONA_PAT', 'corona_eyJhbGciOiJIUzI1NiJ9_eyJuYmYiOjE3MzEwOTA5NDksImlhdCI6MTczMTA5MDk0OSwiZXhwIjoxNzM4ODY2OTQ5LCJwYXQiOnsibmFtZSI6InRlZGdjaXNjby5nZW5AY2lzY28uY29tIn0sImp0aSI6MTA1Nn0_9YIqxLblw1thQHKzR2S6gxysWLlNqC7K1BffLrPIQm8')
    
    @staticmethod
    def get_host():
        return os.getenv('CORONA_HOST', 'corona.cisco.com')

    @staticmethod
    def get_user_name():
        # return os.getenv('CORONA_USERNAME', 'your_generic_user_id_here.gen')
        return os.getenv('CORONA_USERNAME', 'tedgcisco.gen')

    @staticmethod
    def get_security_contact():
        # return os.getenv('CORONA_SECURITY_CONTACT', 'your_mailer_id_here')
        return os.getenv('CORONA_SECURITY_CONTACT', 'upload_spdx_mailer')

    @staticmethod
    def get_engineering_contact():
        # return os.getenv('CORONA_ENGINEERING_CONTACT', 'your_mailer_id_here')
        return os.getenv('CORONA_ENGINEERING_CONTACT', 'upload_spdx_mailer')

    # NOTE: The config items below are where in Corona the SPDX file is uploaded

    @staticmethod
    def get_product_name():
        # return os.getenv('CORONA_PRODUCT_NAME', 'your_corona_product_name_here')
        return os.getenv('CORONA_PRODUCT_NAME', 'tedg test 2024-11-20')

    @staticmethod
    def get_release_version():
        # return os.getenv('CORONA_RELEASE_VERSION', 'your_corona_release_version_here')
        return os.getenv('CORONA_RELEASE_VERSION', '1.0.20')

    @staticmethod
    def get_image_name():
        # return os.getenv('CORONA_IMAGE_NAME', 'your_corona_image_name_here')
        return os.getenv('CORONA_IMAGE_NAME', 'test imageViaApi.20')

    @staticmethod
    def get_spdx_file_path():
        # return os.getenv('CORONA_PRODUCT_NAME', 'your_spdx_file_path_here')
        return os.getenv('CORONA_PRODUCT_NAME', './bes-traceability-spdx.json')


class CoronaError(Exception):
    '''Custom Exception for handling Corona API related errors'''
    pass



class CoronaAPIClient:
    
    def __init__(self, host, user_name):
        self.host = host
        self.user_name = user_name
        self.token = None
        self.pat = None

    def get_auth_token(self):
        ''' Get Bearer token using the PAT (Personal Access Token) '''
        if not self.token:
            try:
                # Corona PAT (Personal Access Token for self.user_name)
                self.pat = CoronaConfig.get_corona_pat()
                # msg = (f"Corona PAT : {self.pat}"); logger.debug(msg)

                pat_header = {
                    'user': {
                        'username': self.user_name,
                        'pat': self.pat
                    }
                }
                msg = (f'>>>TEST>>> sign_in, pat_header = {pat_header}/n')
                logger.debug(msg)
                sign_in_res = requests.post(f'https://{self.host}/api/auth/sign_in', json=pat_header)
                sign_in_res.raise_for_status()
                self.token = sign_in_res.json().get('token')
                msg = (f'>>>TEST>>> sign_in, pat_header = {pat_header}, API token = {self.token}/n')
                logger.debug(msg)
                if not self.token:
                    raise CoronaError('Failed to retrieve token from response.')
            except requests.exceptions.RequestException as e:
                raise CoronaError(f'Error obtaining auth token: {e}') from e
            except Exception as e:
                raise CoronaError(f'Error: {e}') from e
                
        return self.token

    def make_authenticated_request(self, method, endpoint, data=None, files=None, retries=3):
        '''
            Helper function to make authenticated API requests with retry on failure.

            Args:
                self: the instance of the class.
                method: API method (GET or POST)
                endpoint: API endpoint being invoked
                data: JSON data, defaults to None

            Returns:
                API request response converted to JSON
        '''
        self.get_auth_token()
        headers = {'Authorization': f'Bearer {self.token}'}
        url = f'https://{self.host}/{endpoint}'

        for attempt in range(retries):
            try:
                msg = (f'>>>TEST>>> headers = {headers}, url = {url}/n')
                logger.debug(msg)
                response = requests.request(method, 
                                            url, 
                                            headers=headers, 
                                            json=data, 
                                            files=files,
                                            timeout=MAX_REQ_TIMEOUT)
                response.raise_for_status()
                return response.json()

            except requests.exceptions.HTTPError as e:
                if response.status_code in [429, 500, 502, 503, 504]:
                    msg = (f'Temporary server error ({response.status_code}).  ' \
                            'Retrying... ({attempt + 1}/{retries})')
                    logger.warning(msg)
                    time.sleep(2 ** attempt)
                else:
                    self._handle_error(e, response, f'requesting {endpoint}')
                    break

            except requests.exceptions.RequestException as e:
                msg = (f'Network error: {e}. Retrying... ({attempt + 1}/{retries})')
                logger.warning(msg)
                time.sleep(2 ** attempt)

        raise CoronaError(f'Failed to perform request to {endpoint} after {retries} attempts')


    def _handle_error(self, e, response, action):
        ''' Handle API errors for make_authenticated_request() '''
        error_messages = {
            401: f'Unauthorized access while {action}. Invalid PAT or token.',
            422: f'Invalid request during {action}. Ensure that the name is unique.',
        }
        msg = (f">>_handle_error_TEST>> e = '{e}' \nresponse = '{response.json()}'")
        logger.debug(msg)
        msg = error_messages.get(response.status_code, 
                                 f'Error {action}: {response.status_code} ({response.text})')
        logger.fatal(msg)
        sys.exit(response.status_code)


class ProductManager(CoronaAPIClient):
    '''Handle product-related operations.'''

    def get_or_create_product(self, product_name):
        ''' Retrieve or create a product for a given product_name '''
        try:
            res_json = self.make_authenticated_request('GET', f'api/v2/products?name={product_name}')
            if not res_json['data']:
                return self._create_product(product_name)

            msg = f"Product '{product_name}' product_id {res_json['data'][0]['id']} found"
            logger.info(msg)
            return res_json['data'][0]['id']

        except KeyError as e:
            raise CoronaError(f"Unexpected response structure while fetching product '{product_name}'") from e

    def _create_product(self, product_name):
        ''' Create a product for a given product_name '''
        # Note: For Production, change or remove 'cvr_product_name'
        data = {
            'name': product_name,
            'cvr_product_name': 'Test scan – not for production use',
            'enable_certificate_notifications': True
        }
        res_json = self.make_authenticated_request('POST', 'api/v2/products', data)
        msg = f"Product '{product_name}' product_id {res_json['id']} created"
        logger.info(msg)

        return res_json['id']


class ReleaseManager(CoronaAPIClient):
    '''Handle release-related operations.'''

    def get_or_create_release(self, product_id, release_version):
        ''' Retrieve or create a release for a given release_version '''
        try:
            res_json = self.make_authenticated_request('GET', f'api/v2/releases?product_id={product_id}')
            release = next((release for release in res_json['data'] if release['version'] == release_version), None)
            if not release:
                return self._create_release(product_id, release_version)

            msg = f"Release '{release_version}' ({release['id']}) found"
            logger.info(msg)
            return release['id']

        except KeyError:
            raise CoronaError(f"Unexpected response structure while fetching release '{release_version}'")

    def _create_release(self, product_id, release_version):
        ''' Create a release for a given release_version '''
        data = {
            'release': {
                'product_id': product_id,
                'version': release_version,
                'security_contact': CoronaConfig.get_security_contact(),
                'engineering_contact': CoronaConfig.get_engineering_contact(),
                'csdl_identifier': '',
                'release_note': ''
            }
        }
        res_json = self.make_authenticated_request('POST', 'api/v1/releases', data)
        msg = f"Release '{release_version}' release_id {res_json['id']} created"
        logger.info(msg)
        return res_json['id']


class ImageManager(CoronaAPIClient):
    '''Handle image-related operations.'''

    def get_or_create_image(self, product_id, release_id, image_name):
        ''' Retrieve or create an image for a given product_id, release_id, image_name '''
        try:
            res_json = self.make_authenticated_request('GET', f'api/v2/images?release_id={release_id}')
            image_id = next((image['id'] for image in res_json['data'] if image['name'] == image_name), None)
            if not image_id:
                return self._create_image(product_id, release_id, image_name)

            msg = f"Image '{image_name}' image_id {image_id} found"
            logger.info(msg)
            return image_id

        except KeyError as e:
            raise CoronaError(f"Unexpected response structure while fetching image '{image_name}'") from e

    def _create_image(self, product_id, release_id, image_name):
        ''' Create an image for a given product_id, release_id, image_name '''
        try:
            data = {
                'image': {
                    'name': image_name,
                    'release_id': release_id,
                    'product_id': product_id,
                    'security_contact': CoronaConfig.get_security_contact(),
                    'engineering_contact': CoronaConfig.get_engineering_contact(),
                    'location_attributes': {},
                    'tags_attributes': [],
                    'scan_jobs_to_skip': []
                }
            }
            res_json = self.make_authenticated_request('POST', 
                                                       'api/v2/images', 
                                                       data)
            msg = f"Image '{image_name}' image_id {res_json['id']} created"
            logger.info(msg)
            return res_json['id']

        except KeyError:
            raise CoronaError(f"Unexpected response structure while fetching image '{image_name}'")


class SpdxManager(CoronaAPIClient):
    '''Handle spdx-related operations.'''

    def update_or_add_spdx(self, image_id, spdx_file_path):
        '''  Update or add the contents of the spdx_file_path to Corona image_id

        spdx_data:
        - ignore_relationships, boolean - default false; It is common for SPDX files to use relationships to describe the packages. By default only the packages contained in the described packages will be imported. When relationships are ignored (true) all packages will be imported.
            - "ignore_relationships": "false",  # gets rid of main package as a Corona component DOESN"T SEEM TO BE TRUE ANYMORE - JG fixed my complaint!
        - ignore_eo_compliant, boolean - default true; The Executive Order (EO) for SBOMs requires fields that SPDX-2.3 does not. By default these fields will not be required for ingestion. When false, the EO required fields will be required.
        - ignore_validation, boolean - default false; By ignoring validation, Corona will return a warning if the SPDX file doesnt meet the SPDX documentation rather then raising an error. This could result in unexpected/missing data so it should be used with caution.
        - append, boolean - default false; By default old components with the same discovery_tool will be overwritten.
        - discovery_tool, string - default known creator tool or manifest; If discovery_tool is empty the SPDX "creators" field will be checked for the first known tool (current tools are "syft"), if none are found manifest is used.
            - Corona already knows SPDX is from Syft.  It reads "Tool" param from JSON:
            "discovery_tool": "Syft"
        '''
        spdx_data = {
            'ignore_relationships': 'true',
            'ignore_eo_compliant': 'true',
            'ignore_validation': 'true',
        }
        try:
            with open(spdx_file_path, 'r') as f:
                spdx_data['data'] = f.read()
        except FileNotFoundError:
            raise CoronaError(f"SPDX file '{spdx_file_path}' not found.")

        # First request to add JSON content
        res_json = self.make_authenticated_request('POST', 
                                                   f'api/v2/images/{image_id}/spdx.json', 
                                                   data=spdx_data)

        # Upload file in the second request
        with open(spdx_file_path, 'rb') as f:
            res_json = self.make_authenticated_request('POST', 
                                                       f'api/v2/images/{image_id}/spdx.json', 
                                                       files={'data': f})

        return res_json


def main():
    try:
        # Configurations 
        host = CoronaConfig.get_host()
        user_name = CoronaConfig.get_user_name()

        # Initialize managers
        product_manager = ProductManager(host, user_name)
        release_manager = ReleaseManager(host, user_name)
        image_manager = ImageManager(host, user_name)
        spdx_manager = SpdxManager(host, user_name)

        msg = f"Adding SPDX '{CoronaConfig.get_spdx_file_path()}' to" \
               " '{CoronaConfig.get_product_name()}'" \
               " v'{CoronaConfig.get_release_version()}'," \
               " image '{CoronaConfig.get_image_name()}')\n"
        logger.info(msg)

        # Operations
        product_id = product_manager.get_or_create_product(CoronaConfig.get_product_name())
        release_id = release_manager.get_or_create_release(product_id, CoronaConfig.get_release_version())
        image_id = image_manager.get_or_create_image(product_id, release_id, CoronaConfig.get_image_name())
        spdx_response = spdx_manager.update_or_add_spdx(image_id, CoronaConfig.get_spdx_file_path())

        msg = f"SPDX added to '{CoronaConfig.get_product_name()}' " \
               "v'{CoronaConfig.get_release_version()}', " \
               "image '{CoronaConfig.get_image_name()}' ({image_id}) successfully.\n"
        logger.info(msg)

    except CoronaError as e:
        msg = {e}
        logger.fatal(msg)
        sys.exit(1)

if __name__ == '__main__':
    main()

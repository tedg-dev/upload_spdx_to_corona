'''
test_upload_spdx: Unit test (Pytest) for upload_spdx module.
'''
__author__ = 'Ted Gauthier'
__email__ = 'tedg@cisco.com'
__version__ = '1.0.0'
import pytest
import os
import requests
from unittest import mock
from unittest.mock import mock_open
from requests.exceptions import RequestException, HTTPError
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from upload_spdx import (
    CoronaError,
    CoronaConfig,
    CoronaAPIClient,
    ProductManager,
    ReleaseManager,
    ImageManager,
    SpdxManager,
)

# Constants for testing
HOST = "testhost.com"
PAT = "test_pat"
USERNAME = "test_user"
SECURITY_CONTACT = "security_contact@example.com"
ENG_CONTACT = "engineering_contact@example.com"
PRODUCT_NAME = "test_product"
PRODUCT_ID = 123
RELEASE_VERSION = "1.0.0"
RELEASE_ID = 456
IMAGE_NAME = "test_image"
IMAGE_ID = 123
SPDX_FILE_PATH = "test_spdx.spdx"


@pytest.fixture
def mock_env_vars():
    '''Fixture to mock environment variables.'''
    with mock.patch.dict(os.environ, {
        'CORONA_HOST': HOST,
        'CORONA_PAT': PAT,
        'CORONA_USERNAME': USERNAME,
        'CORONA_SECURITY_CONTACT': SECURITY_CONTACT,
        'CORONA_ENGINEERING_CONTACT': ENG_CONTACT
    }):
        yield


# Test the CoronaConfig class
def test_corona_config(mock_env_vars):
    assert CoronaConfig.get_host() == HOST
    assert CoronaConfig.get_user_name() == USERNAME
    assert CoronaConfig.get_security_contact() == SECURITY_CONTACT
    assert CoronaConfig.get_engineering_contact() == ENG_CONTACT


# Test the CoronaAPIClient class
class TestCoronaAPIClient:
    @pytest.fixture
    def api_client(self):
        return CoronaAPIClient(host=HOST, user_name=USERNAME)

    # !!! NEED TO REDO auth_token tests TEST NOW THAT CONJURCLIENT IS INVOKED !!!
    # @mock.patch('requests.post')
    # def test_get_auth_token_success(self, mock_post, api_client):
    #     '''Test get_auth_token with a successful token retrieval.'''
    #     # Mock the response of the requests.post call
    #     mock_post.return_value = mock.Mock(status_code=200, json=lambda: {'token': 'test_token'})

    #     # Call get_auth_token
    #     token = api_client.get_auth_token()

    #     # Verify that the token was correctly set and returned
    #     assert token == 'test_token'
    #     assert api_client.token == 'test_token'

    # @mock.patch('requests.post')
    # def test_get_auth_token_failure(self, mock_post, api_client):
    #     '''Test get_auth_token when the API returns an error.'''
    #     # Mock an error response from requests.post
    #     mock_post.return_value = mock.Mock(status_code=401, json=lambda: {'message': 'Unauthorized'})
    #     mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()

    #     # Ensure the method raises a CoronaError
    #     with pytest.raises(CoronaError, match='Error obtaining auth token'):
    #         api_client.get_auth_token()

    # @mock.patch('requests.post')
    # def test_get_auth_token_no_token_in_response(self, mock_post, api_client):
    #     '''Test get_auth_token when the API does not return a token in the response.'''
    #     # Mock response without token field
    #     mock_post.return_value = mock.Mock(status_code=200, json=lambda: {})

    #     # Ensure the method raises a CoronaError due to missing token
    #     with pytest.raises(CoronaError, match='Failed to retrieve token from response'):
    #         api_client.get_auth_token()


    # Test for make_authenticated_request
    @mock.patch.object(CoronaAPIClient, 'get_auth_token', return_value='test_token')
    @mock.patch('requests.request')
    def test_make_authenticated_request_success(self, mock_request, mock_get_auth_token, api_client):
        '''Test make_authenticated_request with successful API call.'''
        # Mock successful request response
        mock_request.return_value = mock.Mock(status_code=200, json=lambda: {'data': 'response_data'})

        # Call the method
        response = api_client.make_authenticated_request('GET', 'endpoint')

        # Check if the response is as expected
        assert response == {'data': 'response_data'}

    @mock.patch.object(CoronaAPIClient, 'get_auth_token', return_value='test_token')
    @mock.patch('requests.request')
    def test_make_authenticated_request_retries_on_server_error(self, mock_request, mock_get_auth_token, api_client):
        '''Test make_authenticated_request with a server error that retries.'''
        # Simulate server error responses followed by a success
        mock_request.side_effect = [
            mock.Mock(status_code=503, raise_for_status=mock.Mock(side_effect=requests.exceptions.HTTPError())),
            mock.Mock(status_code=503, raise_for_status=mock.Mock(side_effect=requests.exceptions.HTTPError())),
            mock.Mock(status_code=200, json=lambda: {'data': 'response_data'})
        ]

        # Call the method and check if it eventually succeeds
        response = api_client.make_authenticated_request('GET', 'endpoint')
        assert response == {'data': 'response_data'}
        assert mock_request.call_count == 3  # Should be retried 2 times before success


    @mock.patch.object(CoronaAPIClient, 'get_auth_token', return_value='test_token')
    @mock.patch('requests.request')
    def test_make_authenticated_request_network_error_retries(self, mock_request, mock_get_auth_token, api_client):
        '''Test make_authenticated_request handles network errors and retries.'''
        mock_request.side_effect = [
            requests.exceptions.ConnectionError,
            mock.Mock(status_code=200, json=lambda: {'data': 'response_data'})
        ]

        response = api_client.make_authenticated_request('GET', 'endpoint')
        assert response == {'data': 'response_data'}
        assert mock_request.call_count == 2


    @mock.patch.object(CoronaAPIClient, 'get_auth_token', return_value='test_token')
    @mock.patch('requests.request')
    def test_make_authenticated_request_fail_after_retries(self, mock_request, mock_get_auth_token, api_client):
        '''Test make_authenticated_request fails after max retries on server errors.'''
        mock_request.return_value = mock.Mock(status_code=503, raise_for_status=mock.Mock(side_effect=requests.exceptions.HTTPError()))

        with pytest.raises(CoronaError, match='Failed to perform request'):
            api_client.make_authenticated_request('GET', 'endpoint', retries=3)


    # Test for _handle_error
    @mock.patch('sys.exit')
    def test_handle_error_unauthorized(self, mock_exit, api_client):
        '''Test _handle_error handles a 401 unauthorized error.'''
        response = mock.Mock(status_code=401, text='Unauthorized error')
        error = requests.exceptions.HTTPError()

        api_client._handle_error(error, response, 'authenticating')

        # Check the error message and that sys.exit was called with 401
        mock_exit.assert_called_once_with(401)

    @mock.patch('sys.exit')
    def test_handle_error_unprocessable_entity(self, mock_exit, api_client):
        '''Test _handle_error handles a 422 unprocessable entity error.'''
        response = mock.Mock(status_code=422, text='Invalid request')
        error = requests.exceptions.HTTPError()

        api_client._handle_error(error, response, 'creating product')

        # Check the error message and that sys.exit was called with 422
        mock_exit.assert_called_once_with(422)

    @mock.patch('sys.exit')
    def test_handle_error_generic_error(self, mock_exit, api_client):
        '''Test _handle_error handles an unknown error status code.'''
        response = mock.Mock(status_code=500, text='Internal Server Error')
        error = requests.exceptions.HTTPError()

        api_client._handle_error(error, response, 'unknown action')

        # Check that sys.exit was called with the response's status code
        mock_exit.assert_called_once_with(500)


# Test ProductManager
class TestProductManager:
    @pytest.fixture
    def product_manager(self):
        return ProductManager(HOST, USERNAME)

    # Test for get_or_create_product
    @mock.patch.object(ProductManager, 'make_authenticated_request')
    def test_get_or_create_product_found(self, mock_make_authenticated_request, product_manager):
        '''Test get_or_create_product when the product already exists.'''
        mock_make_authenticated_request.return_value = {
            "data": [{"id": 123, "name": PRODUCT_NAME}]
        }
        product_id = product_manager.get_or_create_product(PRODUCT_NAME)
        # Verify the product ID is returned and no creation is attempted
        assert product_id == 123
        mock_make_authenticated_request.assert_called_once_with('GET', f'api/v2/products?name={PRODUCT_NAME}')

    @mock.patch.object(ProductManager, 'make_authenticated_request')
    @mock.patch.object(ProductManager, '_create_product')
    def test_get_or_create_product_not_found(self, mock_create_product, mock_make_authenticated_request, product_manager):
        '''Test get_or_create_product when the product does not exist and is created.'''
        # Simulate no product found in GET request
        mock_make_authenticated_request.return_value = {"data": []}
        # Simulate creation response
        mock_create_product.return_value = 456

        product_id = product_manager.get_or_create_product(PRODUCT_NAME)

        # Ensure the product creation method was called and returned ID is from _create_product
        assert product_id == 456
        mock_make_authenticated_request.assert_called_once_with('GET', f'api/v2/products?name={PRODUCT_NAME}')
        mock_create_product.assert_called_once_with(PRODUCT_NAME)

    @mock.patch.object(ProductManager, 'make_authenticated_request')
    def test_get_or_create_product_key_error(self, mock_make_authenticated_request, product_manager):
        '''Test get_or_create_product when a KeyError occurs due to an unexpected response structure.'''
        # Simulate a malformed response without 'data' key
        mock_make_authenticated_request.return_value = {"unexpected_key": "unexpected_value"}

        with pytest.raises(CoronaError, match="Unexpected response structure"):
            product_manager.get_or_create_product(PRODUCT_NAME)


    # Test for _create_product
    @mock.patch.object(ProductManager, 'make_authenticated_request')
    def test_create_product_success(self, mock_make_authenticated_request, product_manager):
        '''Test _create_product for successful product creation.'''
        # Mock the POST response with a product ID
        mock_make_authenticated_request.return_value = {"id": 456}

        product_id = product_manager._create_product(PRODUCT_NAME)

        # Verify that the product creation ID is returned
        assert product_id == 456
        mock_make_authenticated_request.assert_called_once_with(
            'POST', 
            'api/v2/products', 
            {
                'name': PRODUCT_NAME,
                'cvr_product_name': 'Test scan – not for production use',
                'enable_certificate_notifications': True
            }
        )

    @mock.patch.object(ProductManager, 'make_authenticated_request')
    def test_create_product_request_failure(self, mock_make_authenticated_request, product_manager):
        '''Test _create_product when make_authenticated_request raises a CoronaError.'''
        # Mock make_authenticated_request to raise an exception
        mock_make_authenticated_request.side_effect = CoronaError("Request failed")

        with pytest.raises(CoronaError, match="Request failed"):
            product_manager._create_product(PRODUCT_NAME)


# Test ReleaseManager
class TestReleaseManager:
    @pytest.fixture
    def release_manager(self):
        '''Fixture to create a ReleaseManager instance.'''
        return ReleaseManager(HOST, USERNAME)

    # Test for get_or_create_release
    @mock.patch.object(ReleaseManager, 'make_authenticated_request')
    def test_get_or_create_release_found(self, mock_make_authenticated_request, release_manager):
        '''Test get_or_create_release when the release already exists.'''
        # Mocking a response with a matching release version
        mock_make_authenticated_request.return_value = {
            "data": [{"id": 789, "version": RELEASE_VERSION}]
        }

        release_id = release_manager.get_or_create_release(PRODUCT_ID, RELEASE_VERSION)

        # Verify the release ID is returned without creating a new release
        assert release_id == 789
        mock_make_authenticated_request.assert_called_once_with('GET', f'api/v2/releases?product_id={PRODUCT_ID}')


    @mock.patch.object(ReleaseManager, 'make_authenticated_request')
    @mock.patch.object(ReleaseManager, '_create_release')
    def test_get_or_create_release_not_found(self, mock_create_release, mock_make_authenticated_request, release_manager):
        '''Test get_or_create_release when the release does not exist and needs to be created.'''
        # Simulate no matching release version found in GET response
        mock_make_authenticated_request.return_value = {"data": [{"id": 111, "version": "0.9.0"}]}
        # Simulate creation response for the new release
        mock_create_release.return_value = 456

        release_id = release_manager.get_or_create_release(PRODUCT_ID, RELEASE_VERSION)

        # Verify the release creation method was called and returned ID is from _create_release
        assert release_id == 456
        mock_make_authenticated_request.assert_called_once_with('GET', f'api/v2/releases?product_id={PRODUCT_ID}')
        mock_create_release.assert_called_once_with(PRODUCT_ID, RELEASE_VERSION)


    @mock.patch.object(ReleaseManager, 'make_authenticated_request')
    def test_get_or_create_release_key_error(self, mock_make_authenticated_request, release_manager):
        '''Test get_or_create_release when a KeyError occurs due to an unexpected response structure.'''
        # Mock a malformed response missing 'data' key
        mock_make_authenticated_request.return_value = {"unexpected_key": "unexpected_value"}

        with pytest.raises(CoronaError, match="Unexpected response structure while fetching release"):
            release_manager.get_or_create_release(PRODUCT_ID, RELEASE_VERSION)


# Test ImageManager
class TestImageManager:
    @pytest.fixture
    def image_manager(self):
        return ImageManager(HOST, USERNAME)

     # Test for get_or_create_image
    @mock.patch.object(ImageManager, 'make_authenticated_request')
    def test_get_or_create_image_found(self, mock_make_authenticated_request, image_manager):
        '''Test get_or_create_image when the image already exists.'''
        # Mock a response with a matching image name
        mock_make_authenticated_request.return_value = {
            "data": [{"id": IMAGE_ID, "name": IMAGE_NAME}]
        }
        image_id = image_manager.get_or_create_image(PRODUCT_ID, RELEASE_ID, IMAGE_NAME)
        # Verify the image ID is returned without creating a new image
        assert image_id == IMAGE_ID
        mock_make_authenticated_request.assert_called_once_with('GET', f'api/v2/images?release_id={RELEASE_ID}')


    @mock.patch.object(ImageManager, 'make_authenticated_request')
    @mock.patch.object(ImageManager, '_create_image')
    def test_get_or_create_image_not_found(self, mock_create_image, mock_make_authenticated_request, image_manager):
        '''Test get_or_create_image when the image does not exist and needs to be created.'''
        # Simulate no matching image found in GET response
        mock_make_authenticated_request.return_value = {"data": [{"id": 111, "name": "different_image"}]}
        # Simulate creation response for the new image
        mock_create_image.return_value = IMAGE_ID

        image_id = image_manager.get_or_create_image(PRODUCT_ID, RELEASE_ID, IMAGE_NAME)

        # Verify the image creation method was called and returned ID is from _create_image
        assert image_id == IMAGE_ID
        mock_make_authenticated_request.assert_called_once_with('GET', f'api/v2/images?release_id={RELEASE_ID}')
        mock_create_image.assert_called_once_with(PRODUCT_ID, RELEASE_ID, IMAGE_NAME)


    @mock.patch.object(ImageManager, 'make_authenticated_request')
    def test_get_or_create_image_key_error(self, mock_make_authenticated_request, image_manager):
        '''Test get_or_create_image when a KeyError occurs due to an unexpected response structure.'''
        # Mock a malformed response missing 'data' key
        mock_make_authenticated_request.return_value = {"unexpected_key": "unexpected_value"}

        with pytest.raises(CoronaError, match=f"Unexpected response structure while fetching image '{IMAGE_NAME}'"):
            image_manager.get_or_create_image(PRODUCT_ID, RELEASE_ID, IMAGE_NAME)


    # Test get_or_create_image - Image does not exist, creates a new image
    @mock.patch.object(ImageManager, '_create_image')
    @mock.patch.object(ImageManager, 'make_authenticated_request')
    def test_get_or_create_image_creates_new(self, mock_request, mock_create_image, image_manager):
        """Test that get_or_create_image creates a new image if it does not exist."""
        mock_request.return_value = {'data': []}
        mock_create_image.return_value = IMAGE_ID

        result = image_manager.get_or_create_image(PRODUCT_ID, RELEASE_ID, IMAGE_NAME)

        mock_request.assert_called_once_with('GET', f'api/v2/images?release_id={RELEASE_ID}')
        mock_create_image.assert_called_once_with(PRODUCT_ID, RELEASE_ID, IMAGE_NAME)
        assert result == IMAGE_ID

    # Test for _create_image
    @mock.patch.object(ImageManager, 'make_authenticated_request')
    @mock.patch('upload_spdx.CoronaConfig.get_security_contact', return_value="security_contact@example.com")
    @mock.patch('upload_spdx.CoronaConfig.get_engineering_contact', return_value="engineering_contact@example.com")
    def test_create_image_success(self, mock_engineering_contact, mock_security_contact, mock_make_authenticated_request, image_manager):
        '''Test _create_image for successful image creation.'''
        # Mocking a successful response with a new image ID
        mock_make_authenticated_request.return_value = {"id": IMAGE_ID}

        image_id = image_manager._create_image(PRODUCT_ID, RELEASE_ID, IMAGE_NAME)

        # Verify that the image creation ID is returned
        assert image_id == IMAGE_ID
        mock_make_authenticated_request.assert_called_once_with(
            'POST',
            'api/v2/images',
            {
                'image': {
                    'name': IMAGE_NAME,
                    'release_id': RELEASE_ID,
                    'product_id': PRODUCT_ID,
                    'security_contact': "security_contact@example.com",
                    'engineering_contact': "engineering_contact@example.com",
                    'location_attributes': {},
                    'tags_attributes': [],
                    'scan_jobs_to_skip': []
                }
            }
        )


    @mock.patch.object(ImageManager, 'make_authenticated_request')
    @mock.patch('upload_spdx.CoronaConfig.get_security_contact', return_value="security_contact@example.com")
    @mock.patch('upload_spdx.CoronaConfig.get_engineering_contact', return_value="engineering_contact@example.com")
    def test_create_image_missing_id(self, mock_engineering_contact, mock_security_contact, mock_make_authenticated_request, image_manager):
        '''Test _create_image when the response does not include an image ID.'''
        # Mocking response missing 'id' field
        mock_make_authenticated_request.return_value = {}

        with pytest.raises(CoronaError, match=f"Unexpected response structure while fetching image '{IMAGE_NAME}'"):
            image_manager._create_image(PRODUCT_ID, RELEASE_ID, IMAGE_NAME)


    @mock.patch.object(ImageManager, 'make_authenticated_request')
    def test_create_image_request_failure(self, mock_make_authenticated_request, image_manager):
        '''Test _create_image when make_authenticated_request raises a CoronaError.'''
        # Simulate a network request error
        mock_make_authenticated_request.side_effect = CoronaError("Request failed")

        with pytest.raises(CoronaError, match="Request failed"):
            image_manager._create_image(PRODUCT_ID, RELEASE_ID, IMAGE_NAME)


# Test SpdxManager
class TestSpdxManager:
    @pytest.fixture
    def spdx_manager(self):
        return SpdxManager(HOST, USERNAME)

    @mock.patch.object(CoronaAPIClient, 'make_authenticated_request')
    def test_update_or_add_spdx(self, mock_make_authenticated_request, spdx_manager, tmp_path):
        spdx_file = tmp_path / 'test.spdx'
        spdx_file.write_text('SPDX file content')

        mock_make_authenticated_request.side_effect = [{'id': 'mocked_image_id'}, {}]
        spdx_manager.update_or_add_spdx('mocked_image_id', str(spdx_file))
        assert mock_make_authenticated_request.call_count == 2

    # Test for update_or_add_spdx - Successful case
    @mock.patch("builtins.open", new_callable=mock_open, read_data="mock_spdx_data")
    @mock.patch.object(SpdxManager, 'make_authenticated_request')
    def test_update_or_add_spdx_success(self, mock_make_authenticated_request, mock_open_file, spdx_manager):
        '''Test update_or_add_spdx successfully posts data and file.'''
        # Mock first response to POST request
        mock_make_authenticated_request.return_value = {"status": "success"}

        response = spdx_manager.update_or_add_spdx(IMAGE_ID, SPDX_FILE_PATH)

        # Check if open was called twice: once for reading, once for binary reading
        assert mock_open_file.call_count == 2

        # Verify first request data for JSON content
        mock_make_authenticated_request.assert_any_call(
            'POST',
            f'api/v2/images/{IMAGE_ID}/spdx.json',
            data={
                'ignore_relationships': 'true',
                'ignore_eo_compliant': 'true',
                'ignore_validation': 'true',
                'data': 'mock_spdx_data'
            }
        )

        # Verify second request with file upload
        mock_make_authenticated_request.assert_any_call(
            'POST',
            f'api/v2/images/{IMAGE_ID}/spdx.json',
            files={'data': mock_open_file.return_value}
        )

        # Assert response is as expected
        assert response == {"status": "success"}


    # Test for update_or_add_spdx - File not found
    @mock.patch("builtins.open", side_effect=FileNotFoundError)
    def test_update_or_add_spdx_file_not_found(self, mock_open_file, spdx_manager):
        '''Test update_or_add_spdx when the SPDX file is not found.'''
        with pytest.raises(CoronaError, match=f"SPDX file '{SPDX_FILE_PATH}' not found."):
            spdx_manager.update_or_add_spdx(IMAGE_ID, SPDX_FILE_PATH)

        # Verify that file open was attempted
        mock_open_file.assert_called_once_with(SPDX_FILE_PATH, 'r')


    # Test for update_or_add_spdx - Network request failure on JSON POST
    @mock.patch("builtins.open", new_callable=mock_open, read_data="mock_spdx_data")
    @mock.patch.object(SpdxManager, 'make_authenticated_request')
    def test_update_or_add_spdx_request_failure_json(self, mock_make_authenticated_request, mock_open_file, spdx_manager):
        '''Test update_or_add_spdx when the first POST request raises an error.'''
        # Simulate an error on the first request
        mock_make_authenticated_request.side_effect = [CoronaError("Request failed")]

        with pytest.raises(CoronaError, match="Request failed"):
            spdx_manager.update_or_add_spdx(IMAGE_ID, SPDX_FILE_PATH)

        # Check that open was called only once (for the JSON data)
        mock_open_file.assert_called_once_with(SPDX_FILE_PATH, 'r')
        mock_make_authenticated_request.assert_called_once()


    # Test for update_or_add_spdx - Network request failure on file POST
    @mock.patch("builtins.open", new_callable=mock_open, read_data="mock_spdx_data")
    @mock.patch.object(SpdxManager, 'make_authenticated_request')
    def test_update_or_add_spdx_request_failure_file(self, mock_make_authenticated_request, mock_open_file, spdx_manager):
        '''Test update_or_add_spdx when the second POST request (file) raises an error.'''
        # Successful JSON data upload but file upload fails
        mock_make_authenticated_request.side_effect = [
            {"status": "success"},  # First request succeeds
            CoronaError("File upload failed")  # Second request fails
        ]

        with pytest.raises(CoronaError, match="File upload failed"):
            spdx_manager.update_or_add_spdx(IMAGE_ID, SPDX_FILE_PATH)

        # Check that open was called twice: once for reading and once for binary read
        assert mock_open_file.call_count == 2
        # Verify the requests made in sequence
        assert mock_make_authenticated_request.call_count == 2


    # Test for update_or_add_spdx - Unexpected API response structure
    @mock.patch("builtins.open", new_callable=mock_open, read_data="mock_spdx_data")
    @mock.patch.object(SpdxManager, 'make_authenticated_request')
    def test_update_or_add_spdx_unexpected_response(self, mock_make_authenticated_request, mock_open_file, spdx_manager):
        '''Test update_or_add_spdx when the response structure is unexpected.'''
        # Simulate an unexpected response structure for the first request
        mock_make_authenticated_request.return_value = {"unexpected_key": "unexpected_value"}

        # with pytest.raises(CoronaError, match="Unexpected response structure while adding SPDX"):
        response = spdx_manager.update_or_add_spdx(IMAGE_ID, SPDX_FILE_PATH)

        # Assert response is as expected
        assert response == {"unexpected_key": "unexpected_value"}

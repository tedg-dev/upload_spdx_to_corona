"""
Shared pytest fixtures and constants for all tests.
"""
import pytest
import os
from unittest import mock

# Test constants
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
    """Fixture to mock environment variables."""
    with mock.patch.dict(os.environ, {
        'CORONA_HOST': HOST,
        'CORONA_PAT': PAT,
        'CORONA_USERNAME': USERNAME,
        'CORONA_SECURITY_CONTACT': SECURITY_CONTACT,
        'CORONA_ENGINEERING_CONTACT': ENG_CONTACT
    }):
        yield

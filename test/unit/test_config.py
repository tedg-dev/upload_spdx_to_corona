"""Tests for CoronaConfig module."""

import os
import pytest
from unittest import mock
from upload_spdx.config import CoronaConfig


def test_get_corona_pat_from_env():
    """Test CoronaConfig.get_corona_pat() with env var set."""
    with mock.patch.dict(os.environ, {'CORONA_PAT': 'test_pat'}):
        assert CoronaConfig.get_corona_pat() == 'test_pat'


def test_get_corona_pat_default():
    """Test CoronaConfig.get_corona_pat() with default value."""
    with mock.patch.dict(os.environ, {}, clear=True):
        pat = CoronaConfig.get_corona_pat()
        assert pat.startswith('corona_eyJ')


def test_get_host_from_env():
    """Test CoronaConfig.get_host() with env var set."""
    with mock.patch.dict(os.environ, {'CORONA_HOST': 'test.host.com'}):
        assert CoronaConfig.get_host() == 'test.host.com'


def test_get_host_default():
    """Test CoronaConfig.get_host() with default value."""
    with mock.patch.dict(os.environ, {}, clear=True):
        assert CoronaConfig.get_host() == 'corona.cisco.com'


def test_get_user_name_from_env():
    """Test CoronaConfig.get_user_name() with env var set."""
    with mock.patch.dict(os.environ, {'CORONA_USERNAME': 'testuser'}):
        assert CoronaConfig.get_user_name() == 'testuser'


def test_get_user_name_default():
    """Test CoronaConfig.get_user_name() with default value."""
    with mock.patch.dict(os.environ, {}, clear=True):
        assert CoronaConfig.get_user_name() == 'tedgcisco.gen'


def test_get_security_contact_from_env():
    """Test CoronaConfig.get_security_contact() with env var set."""
    with mock.patch.dict(os.environ,
                         {'CORONA_SECURITY_CONTACT': 'security@test.com'}):
        assert CoronaConfig.get_security_contact() == 'security@test.com'


def test_get_security_contact_default():
    """Test CoronaConfig.get_security_contact() with default value."""
    with mock.patch.dict(os.environ, {}, clear=True):
        assert CoronaConfig.get_security_contact() == 'upload_spdx_mailer'


def test_get_engineering_contact_from_env():
    """Test CoronaConfig.get_engineering_contact() with env var set."""
    contact = 'eng@test.com'
    with mock.patch.dict(os.environ,
                         {'CORONA_ENGINEERING_CONTACT': contact}):
        assert CoronaConfig.get_engineering_contact() == contact


def test_get_engineering_contact_default():
    """Test CoronaConfig.get_engineering_contact() with default value."""
    with mock.patch.dict(os.environ, {}, clear=True):
        assert CoronaConfig.get_engineering_contact() == 'upload_spdx_mailer'


def test_get_product_name_from_env():
    """Test CoronaConfig.get_product_name() with env var set."""
    with mock.patch.dict(os.environ,
                         {'CORONA_PRODUCT_NAME': 'Test Product'}):
        assert CoronaConfig.get_product_name() == 'Test Product'


def test_get_product_name_default():
    """Test CoronaConfig.get_product_name() with default value."""
    with mock.patch.dict(os.environ, {}, clear=True):
        assert CoronaConfig.get_product_name() == 'tedg test 2024-11-20'


def test_get_release_version_from_env():
    """Test CoronaConfig.get_release_version() with env var set."""
    with mock.patch.dict(os.environ,
                         {'CORONA_RELEASE_VERSION': '2.0.0'}):
        assert CoronaConfig.get_release_version() == '2.0.0'


def test_get_release_version_default():
    """Test CoronaConfig.get_release_version() with default value."""
    with mock.patch.dict(os.environ, {}, clear=True):
        assert CoronaConfig.get_release_version() == '1.0.20'


def test_get_image_name_from_env():
    """Test CoronaConfig.get_image_name() with env var set."""
    with mock.patch.dict(os.environ,
                         {'CORONA_IMAGE_NAME': 'Test Image'}):
        assert CoronaConfig.get_image_name() == 'Test Image'


def test_get_image_name_default():
    """Test CoronaConfig.get_image_name() with default value."""
    with mock.patch.dict(os.environ, {}, clear=True):
        assert CoronaConfig.get_image_name() == 'test imageViaApi.20'


def test_get_spdx_file_path_from_env():
    """Test CoronaConfig.get_spdx_file_path() with env var set."""
    with mock.patch.dict(os.environ,
                         {'CORONA_SPDX_FILE_PATH': '/path/to/spdx.json'}):
        assert CoronaConfig.get_spdx_file_path() == '/path/to/spdx.json'


def test_get_spdx_file_path_default():
    """Test CoronaConfig.get_spdx_file_path() with default value."""
    with mock.patch.dict(os.environ, {}, clear=True):
        assert CoronaConfig.get_spdx_file_path() == (
            './bes-traceability-spdx.json'
        )

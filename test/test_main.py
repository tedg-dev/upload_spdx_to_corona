"""
Test cases for upload_spdx.__main__ module.
"""
import pytest
import os
import sys
from unittest import mock
from upload_spdx.__main__ import parse_args, main
from upload_spdx.exceptions import CoronaError


class TestParseArgs:
    """Test argument parsing."""
    
    def test_parse_args_defaults(self):
        """Test parse_args with no arguments."""
        with mock.patch('sys.argv', ['upload_spdx']):
            args = parse_args()
            assert args.pat is None
            assert args.host is None
            assert args.username is None
            assert args.product is None
            assert args.release is None
            assert args.image is None
            assert args.spdx_file is None
            assert args.verbose is False
    
    def test_parse_args_with_auth(self):
        """Test parse_args with authentication arguments."""
        with mock.patch('sys.argv', [
            'upload_spdx',
            '--pat', 'test_pat',
            '--host', 'test.corona.com',
            '--username', 'testuser'
        ]):
            args = parse_args()
            assert args.pat == 'test_pat'
            assert args.host == 'test.corona.com'
            assert args.username == 'testuser'
    
    def test_parse_args_with_product_info(self):
        """Test parse_args with product information."""
        with mock.patch('sys.argv', [
            'upload_spdx',
            '--product', 'TestProduct',
            '--release', '1.0.0',
            '--image', 'test-image'
        ]):
            args = parse_args()
            assert args.product == 'TestProduct'
            assert args.release == '1.0.0'
            assert args.image == 'test-image'
    
    def test_parse_args_with_contacts(self):
        """Test parse_args with contact information."""
        with mock.patch('sys.argv', [
            'upload_spdx',
            '--security-contact', 'security@test.com',
            '--engineering-contact', 'eng@test.com'
        ]):
            args = parse_args()
            assert args.security_contact == 'security@test.com'
            assert args.engineering_contact == 'eng@test.com'
    
    def test_parse_args_with_verbose(self):
        """Test parse_args with verbose flag."""
        with mock.patch('sys.argv', ['upload_spdx', '-v']):
            args = parse_args()
            assert args.verbose is True
        
        with mock.patch('sys.argv', ['upload_spdx', '--verbose']):
            args = parse_args()
            assert args.verbose is True


class TestMain:
    """Test main function."""
    
    @mock.patch('upload_spdx.__main__.SpdxManager')
    @mock.patch('upload_spdx.__main__.ImageManager')
    @mock.patch('upload_spdx.__main__.ReleaseManager')
    @mock.patch('upload_spdx.__main__.ProductManager')
    @mock.patch('upload_spdx.__main__.CoronaConfig')
    def test_main_success(self, mock_config, mock_product_mgr,
                         mock_release_mgr, mock_image_mgr, mock_spdx_mgr):
        """Test successful main execution."""
        # Setup mocks
        mock_config.get_host.return_value = 'test.corona.com'
        mock_config.get_user_name.return_value = 'testuser'
        mock_config.get_product_name.return_value = 'TestProduct'
        mock_config.get_release_version.return_value = '1.0.0'
        mock_config.get_image_name.return_value = 'test-image'
        mock_config.get_spdx_file_path.return_value = 'test.spdx'
        
        mock_product_instance = mock_product_mgr.return_value
        mock_product_instance.get_or_create_product.return_value = 123
        
        mock_release_instance = mock_release_mgr.return_value
        mock_release_instance.get_or_create_release.return_value = 456
        
        mock_image_instance = mock_image_mgr.return_value
        mock_image_instance.get_or_create_image.return_value = 789
        
        mock_spdx_instance = mock_spdx_mgr.return_value
        mock_spdx_instance.update_or_add_spdx.return_value = {'success': True}
        
        with mock.patch('sys.argv', ['upload_spdx']):
            main()
        
        # Verify managers were called
        mock_product_instance.get_or_create_product.assert_called_once_with(
            'TestProduct')
        mock_release_instance.get_or_create_release.assert_called_once_with(
            123, '1.0.0')
        mock_image_instance.get_or_create_image.assert_called_once_with(
            123, 456, 'test-image')
        mock_spdx_instance.update_or_add_spdx.assert_called_once_with(
            789, 'test.spdx')
    
    @mock.patch('upload_spdx.__main__.SpdxManager')
    @mock.patch('upload_spdx.__main__.ImageManager')
    @mock.patch('upload_spdx.__main__.ReleaseManager')
    @mock.patch('upload_spdx.__main__.ProductManager')
    @mock.patch('upload_spdx.__main__.CoronaConfig')
    def test_main_with_cli_args(self, mock_config, mock_product_mgr,
                                mock_release_mgr, mock_image_mgr,
                                mock_spdx_mgr):
        """Test main with CLI arguments overriding env vars."""
        # Setup config defaults
        mock_config.get_host.return_value = 'default.corona.com'
        mock_config.get_user_name.return_value = 'defaultuser'
        
        # Setup manager mocks
        mock_product_instance = mock_product_mgr.return_value
        mock_product_instance.get_or_create_product.return_value = 123
        mock_release_instance = mock_release_mgr.return_value
        mock_release_instance.get_or_create_release.return_value = 456
        mock_image_instance = mock_image_mgr.return_value
        mock_image_instance.get_or_create_image.return_value = 789
        mock_spdx_instance = mock_spdx_mgr.return_value
        
        with mock.patch('sys.argv', [
            'upload_spdx',
            '--product', 'CLI-Product',
            '--release', '2.0.0',
            '--image', 'cli-image',
            '--spdx-file', 'cli.spdx'
        ]):
            main()
        
        # Verify CLI args were used
        mock_product_instance.get_or_create_product.assert_called_once_with(
            'CLI-Product')
        mock_release_instance.get_or_create_release.assert_called_once_with(
            123, '2.0.0')
        mock_image_instance.get_or_create_image.assert_called_once_with(
            123, 456, 'cli-image')
        mock_spdx_instance.update_or_add_spdx.assert_called_once_with(
            789, 'cli.spdx')
    
    @mock.patch('upload_spdx.__main__.ProductManager')
    @mock.patch('upload_spdx.__main__.CoronaConfig')
    def test_main_handles_corona_error(self, mock_config, mock_product_mgr):
        """Test main handles CoronaError correctly."""
        mock_config.get_host.return_value = 'test.corona.com'
        mock_config.get_user_name.return_value = 'testuser'
        mock_config.get_product_name.return_value = 'TestProduct'
        mock_config.get_release_version.return_value = '1.0.0'
        mock_config.get_image_name.return_value = 'test-image'
        mock_config.get_spdx_file_path.return_value = 'test.spdx'
        
        mock_product_instance = mock_product_mgr.return_value
        mock_product_instance.get_or_create_product.side_effect = \
            CoronaError("Test error")
        
        with mock.patch('sys.argv', ['upload_spdx']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
    
    @mock.patch('upload_spdx.__main__.SpdxManager')
    @mock.patch('upload_spdx.__main__.ImageManager')
    @mock.patch('upload_spdx.__main__.ReleaseManager')
    @mock.patch('upload_spdx.__main__.ProductManager')
    @mock.patch('upload_spdx.__main__.CoronaConfig')
    @mock.patch('upload_spdx.__main__.logger')
    def test_main_with_verbose(self, mock_logger, mock_config,
                               mock_product_mgr, mock_release_mgr,
                               mock_image_mgr, mock_spdx_mgr):
        """Test main with verbose flag sets logging level."""
        mock_config.get_host.return_value = 'test.corona.com'
        mock_config.get_user_name.return_value = 'testuser'
        mock_config.get_product_name.return_value = 'TestProduct'
        mock_config.get_release_version.return_value = '1.0.0'
        mock_config.get_image_name.return_value = 'test-image'
        mock_config.get_spdx_file_path.return_value = 'test.spdx'
        
        mock_product_instance = mock_product_mgr.return_value
        mock_product_instance.get_or_create_product.return_value = 123
        mock_release_instance = mock_release_mgr.return_value
        mock_release_instance.get_or_create_release.return_value = 456
        mock_image_instance = mock_image_mgr.return_value
        mock_image_instance.get_or_create_image.return_value = 789
        mock_spdx_instance = mock_spdx_mgr.return_value
        
        with mock.patch('sys.argv', ['upload_spdx', '--verbose']):
            main()
        
        mock_logger.setLevel.assert_called_once()
    
    @mock.patch('upload_spdx.__main__.SpdxManager')
    @mock.patch('upload_spdx.__main__.ImageManager')
    @mock.patch('upload_spdx.__main__.ReleaseManager')
    @mock.patch('upload_spdx.__main__.ProductManager')
    @mock.patch('upload_spdx.__main__.CoronaConfig')
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_main_sets_env_vars_from_cli(self, mock_config, mock_product_mgr,
                                         mock_release_mgr, mock_image_mgr,
                                         mock_spdx_mgr):
        """Test main sets environment variables from CLI args."""
        mock_config.get_host.return_value = 'test.corona.com'
        mock_config.get_user_name.return_value = 'testuser'
        mock_config.get_product_name.return_value = 'TestProduct'
        mock_config.get_release_version.return_value = '1.0.0'
        mock_config.get_image_name.return_value = 'test-image'
        mock_config.get_spdx_file_path.return_value = 'test.spdx'
        
        mock_product_instance = mock_product_mgr.return_value
        mock_product_instance.get_or_create_product.return_value = 123
        mock_release_instance = mock_release_mgr.return_value
        mock_release_instance.get_or_create_release.return_value = 456
        mock_image_instance = mock_image_mgr.return_value
        mock_image_instance.get_or_create_image.return_value = 789
        mock_spdx_instance = mock_spdx_mgr.return_value
        
        with mock.patch('sys.argv', [
            'upload_spdx',
            '--pat', 'cli_pat',
            '--security-contact', 'sec@test.com',
            '--engineering-contact', 'eng@test.com'
        ]):
            main()
        
        assert os.environ.get('CORONA_PAT') == 'cli_pat'
        assert os.environ.get('CORONA_SECURITY_CONTACT') == 'sec@test.com'
        assert os.environ.get('CORONA_ENGINEERING_CONTACT') == 'eng@test.com'

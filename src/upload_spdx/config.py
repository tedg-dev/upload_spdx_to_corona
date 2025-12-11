"""Configuration module for Corona REST API settings."""

import os


class CoronaConfig:
    """Configuration for Corona-related environment variables and defaults."""

    @staticmethod
    def get_corona_pat():
        """Get Corona Personal Access Token from environment."""
        pat = os.getenv('CORONA_PAT')
        if not pat:
            raise ValueError(
                "CORONA_PAT environment variable is required. "
                "Please set it before running."
            )
        return pat

    @staticmethod
    def get_host():
        """Get Corona host from environment."""
        return os.getenv('CORONA_HOST', 'corona.cisco.com')

    @staticmethod
    def get_user_name():
        """Get Corona username from environment."""
        username = os.getenv('CORONA_USERNAME')
        if not username:
            raise ValueError(
                "CORONA_USERNAME environment variable is required. "
                "Please set it before running."
            )
        return username

    @staticmethod
    def get_security_contact():
        """Get security contact email from environment."""
        return os.getenv('CORONA_SECURITY_CONTACT', 'upload_spdx_mailer')

    @staticmethod
    def get_engineering_contact():
        """Get engineering contact email from environment."""
        return os.getenv('CORONA_ENGINEERING_CONTACT', 'upload_spdx_mailer')

    @staticmethod
    def get_product_name():
        """Get product name from environment."""
        product = os.getenv('CORONA_PRODUCT_NAME')
        if not product:
            raise ValueError(
                "CORONA_PRODUCT_NAME environment variable is required. "
                "Please set it before running."
            )
        return product

    @staticmethod
    def get_release_version():
        """Get release version from environment."""
        version = os.getenv('CORONA_RELEASE_VERSION')
        if not version:
            raise ValueError(
                "CORONA_RELEASE_VERSION environment variable is required. "
                "Please set it before running."
            )
        return version

    @staticmethod
    def get_image_name():
        """Get image name from environment."""
        image = os.getenv('CORONA_IMAGE_NAME')
        if not image:
            raise ValueError(
                "CORONA_IMAGE_NAME environment variable is required. "
                "Please set it before running."
            )
        return image

    @staticmethod
    def get_spdx_file_path():
        """Get SPDX file path from environment."""
        # Note: This uses CORONA_PRODUCT_NAME as default due to original code
        return os.getenv('CORONA_SPDX_FILE_PATH',
                         './bes-traceability-spdx.json')

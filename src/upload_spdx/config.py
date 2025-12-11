"""Configuration module for Corona REST API settings."""

import os


class CoronaConfig:
    """Configuration for Corona-related environment variables and defaults."""

    @staticmethod
    def get_corona_pat():
        """Get Corona Personal Access Token from environment."""
        return os.getenv(
            'CORONA_PAT',
            'corona_eyJhbGciOiJIUzI1NiJ9_eyJuYmYiOjE3MzEwOTA5NDksImlhdCI6MTczMTA5M'
            'Dk0OSwiZXhwIjoxNzM4ODY2OTQ5LCJwYXQiOnsibmFtZSI6InRlZGdjaXNjby5nZW5A'
            'Y2lzY28uY29tIn0sImp0aSI6MTA1Nn0_9YIqxLblw1thQHKzR2S6gxysWLlNqC7K1BffLrPIQm8'
        )

    @staticmethod
    def get_host():
        """Get Corona host from environment."""
        return os.getenv('CORONA_HOST', 'corona.cisco.com')

    @staticmethod
    def get_user_name():
        """Get Corona username from environment."""
        return os.getenv('CORONA_USERNAME', 'tedgcisco.gen')

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
        return os.getenv('CORONA_PRODUCT_NAME', 'tedg test 2024-11-20')

    @staticmethod
    def get_release_version():
        """Get release version from environment."""
        return os.getenv('CORONA_RELEASE_VERSION', '1.0.20')

    @staticmethod
    def get_image_name():
        """Get image name from environment."""
        return os.getenv('CORONA_IMAGE_NAME', 'test imageViaApi.20')

    @staticmethod
    def get_spdx_file_path():
        """Get SPDX file path from environment."""
        # Note: This uses CORONA_PRODUCT_NAME as default due to original code
        return os.getenv('CORONA_SPDX_FILE_PATH',
                         './bes-traceability-spdx.json')

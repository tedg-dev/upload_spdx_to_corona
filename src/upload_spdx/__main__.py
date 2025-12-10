"""Main entry point for upload_spdx package."""

import sys
import logging
from .config import CoronaConfig
from .managers import (
    ProductManager,
    ReleaseManager,
    ImageManager,
    SpdxManager
)
from .exceptions import CoronaError

logger = logging.getLogger('upload_spdx')


def main():
    """Main function to upload SPDX to Corona."""
    try:
        # Configurations
        host = CoronaConfig.get_host()
        user_name = CoronaConfig.get_user_name()

        # Initialize managers
        product_manager = ProductManager(host, user_name)
        release_manager = ReleaseManager(host, user_name)
        image_manager = ImageManager(host, user_name)
        spdx_manager = SpdxManager(host, user_name)

        product_name = CoronaConfig.get_product_name()
        release_version = CoronaConfig.get_release_version()
        image_name = CoronaConfig.get_image_name()
        spdx_file_path = CoronaConfig.get_spdx_file_path()

        msg = (f"Adding SPDX '{spdx_file_path}' to '{product_name}' "
               f"v'{release_version}', image '{image_name}')\n")
        logger.info(msg)

        # Operations
        product_id = product_manager.get_or_create_product(product_name)
        release_id = release_manager.get_or_create_release(
            product_id, release_version)
        image_id = image_manager.get_or_create_image(
            product_id, release_id, image_name)
        spdx_response = spdx_manager.update_or_add_spdx(
            image_id, spdx_file_path)

        msg = (f"SPDX added to '{product_name}' v'{release_version}', "
               f"image '{image_name}' ({image_id}) successfully.\n")
        logger.info(msg)

    except CoronaError as e:
        msg = {e}
        logger.fatal(msg)
        sys.exit(1)


if __name__ == '__main__':
    main()

"""Main entry point for upload_spdx package."""

import sys
import argparse
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


def parse_args():
    """
    Parse command-line arguments.
    
    CLI arguments override environment variables.
    """
    parser = argparse.ArgumentParser(
        description='Upload SPDX documents to Cisco Corona platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables (used as defaults):
  CORONA_PAT                Personal Access Token
  CORONA_HOST               Corona host (default: corona.cisco.com)
  CORONA_USERNAME           Corona username
  CORONA_SECURITY_CONTACT   Security contact email
  CORONA_ENGINEERING_CONTACT Engineering contact email
  CORONA_PRODUCT_NAME       Product name
  CORONA_RELEASE_VERSION    Release version
  CORONA_IMAGE_NAME         Image name
  CORONA_SPDX_FILE_PATH     Path to SPDX file

Examples:
  # Using environment variables
  export CORONA_PAT="your_pat"
  python -m upload_spdx
  
  # Using CLI arguments (ALL values in quotes for consistency)
  python -m upload_spdx --pat "your_pat" --username "your_user" \\
    --product "My Product" --release "1.0.0" --image "My Image" \\
    --spdx-file "./path/to/spdx.json"
  
  # Minimal example with quotes
  python -m upload_spdx --product "My Product" --release "1.0.0"
        """
    )
    
    # Authentication
    parser.add_argument(
        '--pat',
        help='Corona Personal Access Token (overrides CORONA_PAT)'
    )
    parser.add_argument(
        '--host',
        help='Corona host (overrides CORONA_HOST)'
    )
    parser.add_argument(
        '--username',
        help='Corona username (overrides CORONA_USERNAME)'
    )
    
    # Contacts
    parser.add_argument(
        '--security-contact',
        help='Security contact email (overrides CORONA_SECURITY_CONTACT)'
    )
    parser.add_argument(
        '--engineering-contact',
        help='Engineering contact email '
             '(overrides CORONA_ENGINEERING_CONTACT)'
    )
    
    # Product information
    parser.add_argument(
        '--product',
        help='Product name (overrides CORONA_PRODUCT_NAME)'
    )
    parser.add_argument(
        '--release',
        help='Release version (overrides CORONA_RELEASE_VERSION)'
    )
    parser.add_argument(
        '--image',
        help='Image name (overrides CORONA_IMAGE_NAME)'
    )
    parser.add_argument(
        '--spdx-file',
        help='Path to SPDX file (overrides CORONA_SPDX_FILE_PATH)'
    )
    parser.add_argument(
        '--spdx-version',
        default='SPDX-2.3',
        help='SPDX version (default: SPDX-2.3, supports 3.0+)'
    )
    
    # Options
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='upload_spdx 1.0.0'
    )
    
    return parser.parse_args()


def main():
    """Main function to upload SPDX to Corona."""
    args = parse_args()
    
    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # Get configuration (CLI args override env vars)
        host = args.host or CoronaConfig.get_host()
        user_name = args.username or CoronaConfig.get_user_name()
        product_name = args.product or CoronaConfig.get_product_name()
        release_version = args.release or CoronaConfig.get_release_version()
        image_name = args.image or CoronaConfig.get_image_name()
        spdx_file_path = args.spdx_file or CoronaConfig.get_spdx_file_path()
        
        # Override config for contacts if provided via CLI
        if args.security_contact:
            import os
            os.environ['CORONA_SECURITY_CONTACT'] = args.security_contact
        if args.engineering_contact:
            import os
            os.environ['CORONA_ENGINEERING_CONTACT'] = \
                args.engineering_contact
        if args.pat:
            import os
            os.environ['CORONA_PAT'] = args.pat
        
        # Initialize managers
        product_manager = ProductManager(host, user_name)
        release_manager = ReleaseManager(host, user_name)
        image_manager = ImageManager(host, user_name)
        spdx_manager = SpdxManager(host, user_name)

        msg = (f"Adding SPDX {spdx_file_path} to product {product_name} "
               f"version {release_version}, image {image_name}\n")
        logger.info(msg)

        # Operations
        product_id = product_manager.get_or_create_product(product_name)
        release_id = release_manager.get_or_create_release(
            product_id, release_version)
        image_id = image_manager.get_or_create_image(
            product_id, release_id, image_name)
        spdx_manager.update_or_add_spdx(image_id, spdx_file_path, args.spdx_version)

        msg = (f"SPDX added to product {product_name} version {release_version}, "
               f"image {image_name} (ID: {image_id}) successfully.\n")
        logger.info(msg)

    except CoronaError as e:
        msg = {e}
        logger.fatal(msg)
        sys.exit(1)


if __name__ == '__main__':
    main()

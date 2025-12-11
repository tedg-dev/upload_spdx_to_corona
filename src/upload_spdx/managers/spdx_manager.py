"""SPDX document management for Corona API."""

import logging
from ..api_client import CoronaAPIClient
from ..exceptions import CoronaError

logger = logging.getLogger('upload_spdx')


class SpdxManager(CoronaAPIClient):
    """Handle SPDX document operations."""

    def update_or_add_spdx(self, image_id, spdx_file_path):
        """
        Upload or update SPDX document for an image.

        Args:
            image_id: ID of the image
            spdx_file_path: Path to the SPDX file

        Returns:
            dict: API response

        Raises:
            CoronaError: If SPDX upload fails
        """
        msg = f"Uploading SPDX from '{spdx_file_path}' to image {image_id}"
        logger.info(msg)

        spdx_data = {
            'ignore_relationships': 'true',
            'ignore_eo_compliant': 'true',
            'ignore_validation': 'true',
        }
        try:
            # Read SPDX file as JSON data
            with open(spdx_file_path, 'r') as f:
                spdx_content = f.read()
                spdx_data['data'] = spdx_content
                
                # Extract spdx_version from the JSON content
                import json
                spdx_json = json.loads(spdx_content)
                if 'spdxVersion' in spdx_json:
                    spdx_data['spdx_version'] = spdx_json['spdxVersion']
        except FileNotFoundError:
            raise CoronaError(f"SPDX file '{spdx_file_path}' not found.")
        except json.JSONDecodeError as e:
            raise CoronaError(f"Invalid JSON in SPDX file: {e}")

        # First, POST the JSON data with ignore parameters
        res_json = self.make_authenticated_request(
            'POST',
            f'api/v2/images/{image_id}/spdx.json',
            data=spdx_data
        )

        # Then, POST the file itself
        with open(spdx_file_path, 'rb') as f:
            res_json = self.make_authenticated_request(
                'POST',
                f'api/v2/images/{image_id}/spdx.json',
                files={'data': f}
            )

        return res_json

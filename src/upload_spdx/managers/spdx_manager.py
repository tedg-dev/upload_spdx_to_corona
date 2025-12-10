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

        try:
            # Read SPDX file as JSON data
            with open(spdx_file_path, 'r') as f:
                spdx_data = f.read()
        except FileNotFoundError:
            raise CoronaError(f"SPDX file '{spdx_file_path}' not found.")

        # First, POST the JSON data
        res_json = self.make_authenticated_request(
            'POST',
            f'api/v2/images/{image_id}/spdx',
            data={'data': spdx_data}
        )

        # Then, POST the file itself
        with open(spdx_file_path, 'rb') as f:
            res_json = self.make_authenticated_request(
                'POST',
                f'api/v2/images/{image_id}/spdx.json',
                files={'data': f}
            )

        return res_json

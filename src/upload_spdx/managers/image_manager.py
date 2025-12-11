"""Image management for Corona API."""

import logging
from ..api_client import CoronaAPIClient
from ..config import CoronaConfig
from ..exceptions import CoronaError

logger = logging.getLogger('upload_spdx')


class ImageManager(CoronaAPIClient):
    """Handle image-related operations."""

    def get_or_create_image(self, product_id, release_id, image_name):
        """
        Retrieve or create an image for a given image_name.

        Args:
            product_id: ID of the product
            release_id: ID of the release
            image_name: Name of the image

        Returns:
            int: Image ID

        Raises:
            CoronaError: If image retrieval/creation fails
        """
        try:
            res_json = self.make_authenticated_request(
                'GET',
                f'api/v2/images?release_id={release_id}'
            )
            image = next(
                (img for img in res_json['data']
                 if img['name'] == image_name),
                None
            )
            if not image:
                return self._create_image(product_id, release_id,
                                          image_name)

            msg = f"Image '{image_name}' ({image['id']}) found"
            logger.info(msg)
            return image['id']

        except KeyError:
            raise CoronaError(
                f"Unexpected response structure while fetching image "
                f"'{image_name}'"
            )

    def _create_image(self, product_id, release_id, image_name):
        """
        Create an image for a given image_name.

        Args:
            product_id: ID of the product
            release_id: ID of the release
            image_name: Name of the image

        Returns:
            int: Image ID
        """
        data = {
            'image': {
                'name': image_name,
                'release_id': release_id,
                'product_id': product_id,
                'security_contact': CoronaConfig.get_security_contact(),
                'engineering_contact': CoronaConfig.get_engineering_contact(),
                'location_attributes': {},
                'tags_attributes': [],
                'scan_jobs_to_skip': []
            }
        }
        res_json = self.make_authenticated_request(
            'POST', 'api/v2/images', data)

        if 'id' not in res_json:
            raise CoronaError(
                f"Failed to create image '{image_name}'. "
                f"No ID in response."
            )

        msg = f"Image '{image_name}' image_id {res_json['id']} created"
        logger.info(msg)
        return res_json['id']

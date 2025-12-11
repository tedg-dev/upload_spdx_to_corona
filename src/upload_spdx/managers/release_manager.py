"""Release management for Corona API."""

import logging
from ..api_client import CoronaAPIClient
from ..config import CoronaConfig
from ..exceptions import CoronaError

logger = logging.getLogger('upload_spdx')


class ReleaseManager(CoronaAPIClient):
    """Handle release-related operations."""

    def get_or_create_release(self, product_id, release_version):
        """
        Retrieve or create a release for a given release_version.

        Args:
            product_id: ID of the product
            release_version: Version string for the release

        Returns:
            int: Release ID

        Raises:
            CoronaError: If release retrieval/creation fails
        """
        try:
            res_json = self.make_authenticated_request(
                'GET', f'api/v2/releases?product_id={product_id}')
            release = next(
                (release for release in res_json['data']
                 if release['version'] == release_version),
                None
            )
            if not release:
                return self._create_release(product_id, release_version)

            msg = f"Release '{release_version}' ({release['id']}) found"
            logger.info(msg)
            return release['id']

        except KeyError:
            raise CoronaError(
                f"Unexpected response structure while fetching release "
                f"'{release_version}'"
            )

    def _create_release(self, product_id, release_version):
        """
        Create a release for a given release_version.

        Args:
            product_id: ID of the product
            release_version: Version string for the release

        Returns:
            int: Release ID
        """
        data = {
            'release': {
                'product_id': product_id,
                'version': release_version,
                'security_contact': CoronaConfig.get_security_contact(),
                'engineering_contact': CoronaConfig.get_engineering_contact(),
                'csdl_identifier': '',
                'release_note': ''
            }
        }
        res_json = self.make_authenticated_request(
            'POST', 'api/v1/releases', data)
        msg = (f"Release '{release_version}' release_id "
               f"{res_json['id']} created")
        logger.info(msg)
        return res_json['id']

"""Product management for Corona API."""

import logging
from ..api_client import CoronaAPIClient
from ..exceptions import CoronaError

logger = logging.getLogger('upload_spdx')


class ProductManager(CoronaAPIClient):
    """Handle product-related operations."""

    def get_or_create_product(self, product_name):
        """
        Retrieve or create a product for a given product_name.

        Args:
            product_name: Name of the product

        Returns:
            int: Product ID

        Raises:
            CoronaError: If product retrieval/creation fails
        """
        try:
            res_json = self.make_authenticated_request(
                'GET', f'api/v2/products?name={product_name}')
            if not res_json['data']:
                return self._create_product(product_name)

            msg = (f"Product '{product_name}' product_id "
                   f"{res_json['data'][0]['id']} found")
            logger.info(msg)
            return res_json['data'][0]['id']

        except KeyError as e:
            raise CoronaError(
                f"Unexpected response structure while fetching product "
                f"'{product_name}'"
            ) from e

    def _create_product(self, product_name):
        """
        Create a product for a given product_name.

        Args:
            product_name: Name of the product to create

        Returns:
            int: Product ID
        """
        # Note: For Production, change or remove 'cvr_product_name'
        data = {
            'name': product_name,
            'cvr_product_name': 'Test scan – not for production use',
            'enable_certificate_notifications': True
        }
        res_json = self.make_authenticated_request(
            'POST', 'api/v2/products', data)
        msg = (f"Product '{product_name}' product_id "
               f"{res_json['id']} created")
        logger.info(msg)

        return res_json['id']

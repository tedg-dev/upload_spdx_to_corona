"""
upload_spdx: Python package for uploading SPDX documents to Cisco Corona.

This package provides classes and utilities for interacting with the Corona
REST API to manage products, releases, images, and SPDX documents.
"""

__author__ = 'Ted Gauthier'
__email__ = 'tedg@cisco.com'
__version__ = '1.0.0'

from .config import CoronaConfig
from .exceptions import CoronaError
from .api_client import CoronaAPIClient
from .managers import (
    ProductManager,
    ReleaseManager,
    ImageManager,
    SpdxManager
)

__all__ = [
    'CoronaConfig',
    'CoronaError',
    'CoronaAPIClient',
    'ProductManager',
    'ReleaseManager',
    'ImageManager',
    'SpdxManager',
]

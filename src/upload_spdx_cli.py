#!/usr/bin/env python3
"""
Command-line interface for upload_spdx package.

This script provides backward compatibility with the original monolithic
upload_spdx.py file while using the new modular structure.
"""

from upload_spdx.__main__ import main

if __name__ == '__main__':
    main()

# upload_spdx_to_corona

<H2>upload_spdx.py</H2>
<H3>
This module contains functions and classes related to uploading an SPDX document file to Corona utilizing the Corona REST_API.
</H3>
  
- Get all Corona configuration info (including PAT creds) from environment variables
- validate via auth api, get API token for Corona headers
- Get user info
- Get/Create Product
- Get/Create Release
- Get/Create Image
- Update/Add SPDX doc file to Image

Also includes 
- extensive unit mock testing via Pytest (```test\test_upload_spdx.py```)
- Sample SPDX document file (JSON) to upload (```bes-traceability-spdx.json```)
- 


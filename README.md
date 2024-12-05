# upload_spdx_to_corona

<H1>upload_spdx.py</H1>
<H3>
This module contains functions and classes related to uploading an SPDX document file to Corona utilizing the Corona REST_API.
</H3>
  
- Get PAT creds
- validate via auth api, get API token for Corona headers
- Get user info
- Get/Create Product
- Get/Create Release
- Get/Create Image
- Update/Add SPDX doc file to Image

Also includes 
- extensive unit mock testing via Pytest (```test_upload_spdx.py```)
- Sample SPDX document file (JSON) to upload (```bes-traceability-spdx.json```)
- 

<H1>conjur_client.py</H1>
<H3>
This module contains functions and classes related to Conjur interactions to manage Corona secrets.
</H3>
  
- Authenticate with Conjur
- Get secrets from Conjur


NOTE:  Microsoft Code Pytest configuration requires these entries for these files:

```launch.json``` - Requires "version" to be added
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Current File with Arguments",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "args": [
                "--product_name",
                "tedg test 2024-11-08",
                "--release_version",
                "1.0.07",
                "--image_name",
                "test imageViaApi.04",
                "--spdx_file_path",
                "./bes-traceability-spdx.json"
            ]
        }
    ]
}
```

```settings.json``` - added ...pytestArgs
```
{
    "python.testing.pytestArgs": [
        "upload_spdx"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "-v",
        "--cov=myproj/",
        "--cov-report=xml",
        "--pdb",
        "./"
    ]
}
```

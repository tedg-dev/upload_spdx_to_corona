pipeline {
    agent any

    environment {
        CORONA_PAT = "corona_eyJhbGciOiJIUzI1NiJ9_eyJuYmYiOjE3MzEwOTA5NDksImlhdCI6MTczMTA5MDk0OSwiZXhwIjoxNzM4ODY2OTQ5LCJwYXQiOnsibmFtZSI6InRlZGdjaXNjby5nZW5AY2lzY28uY29tIn0sImp0aSI6MTA1Nn0_9YIqxLblw1thQHKzR2S6gxysWLlNqC7K1BffLrPIQm8"
        CORONA_HOST = 'corona.cisco.com'
        CORONA_USERNAME = 'tedgcisco.gen'
        CORONA_ENGINEERING_CONTACT = 'tedg-corona-eng-mailer'
        CORONA_SECURITY_CONTACT = 'tedg-corona-sec-mailer'
        CORONA_PRODUCT_NAME = 'TEST - tedg - upload_spdx 2024-11-20'
        CORONA_RELEASE_VERSION = '1.0.0'
        CORONA_IMAGE_NAME = 'imageViaApi.01'
        SPDX_FILE_PATH = './bes-traceability-spdx.json'
        DOCKER_IMAGE = "your-docker-image"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out the source code...'
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                script {
                    echo 'Preparing environment...'
                    // Install dependencies
                    pip install requests pytest
                }
            }
        }

        stage('Build') {
            steps {
                // Build upload_spdx.py
                sh 'cd src'
                sh 'python3 upload_spdx.py'
            }
        }

        stage('Test') {
            steps {
                // Run tests
                sh 'pytest test/test_upload_spdx.py'
            }
        }

        stage('Run - upload') {
            steps {
                sh 'cd src'
                sh 'python3 upload_spdx.py'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
        always {
            echo 'Cleaning up workspace... NOT'
//             cleanWs()
        }
    }
}

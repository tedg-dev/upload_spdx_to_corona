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
//                 script {
//                     git clone --single-branch --branch master ssh://git@wwwin-github.cisco.com:tedg/upload_spdx_to_corona.git
//                 }
            }
        }

        stage('Setup') {
            steps {
                sh "echo 'Preparing environment...'"
                // Create a virtual environment
                sh "python3 -m venv upload_spdx_py_venv"
                sh "source upload_spdx_py_venv/bin/activate"

                // Install dependencies
                pip install requests pytest

//                 script {
//                     echo 'Preparing environment...'
//                     // Create a virtual environment
//                     python3 -m venv upload_spdx_py_venv
//                     source upload_spdx_py_venv/bin/activate

//                     // Install dependencies
//                     pip install requests pytest
//                 }
            }
        }

//         stage('Build Docker Image') {
//             steps {
//                 script {
//                     echo 'Building Docker image...'
//                     sh "docker build -t ${env.DOCKER_IMAGE} ."
//                 }
//             }
//         }

        stage('Build') {
            steps {
                // Activate the virtual environment
                sh 'source upload_spdx_py_venv/bin/activate'

                // Build upload_spdx.py
                sh 'cd src'
                sh 'python3 upload_spdx.py'

                // Build Docker image (if applicable)
//                 sh 'docker build -t my-app .'
            }
        }

        stage('Test') {
            steps {
                // Activate the virtual environment
                sh 'source upload_spdx_py_venv/bin/activate'

                // Run tests
                sh 'pytest test/test_upload_spdx.py'
            }
        }

        stage('Run - upload') {
            steps {
                // Activate the virtual environment
                sh 'source upload_spdx_py_venv/bin/activate'

                sh 'cd src'
                sh 'python3 upload_spdx.py'
            }
        }


//         stage('Build Docker Image') {
//             steps {
//                 script {
//                     echo 'Building Docker image...'
//                     sh "docker build -t ${env.DOCKER_IMAGE} ."
//                 }
//             }
//         }

//         stage('Run Ephemeral Container') {
//             steps {
//                 script {
//                     echo 'Running application in ephemeral Docker container...'
//                     sh "docker run --rm -e ENV_VAR_KEY=MY_ENV_KEY -e ENV_VAR_VALUE=MY_ENV_VALUE -e INPUT_FILE=${env.INPUT_FILE} -e OUTPUT_FILE=${env.OUTPUT_FILE} ${env.DOCKER_IMAGE}"
//                 }
//             }
//         }

//         stage('Archive Output') {
//             steps {
//                 script {
//                     echo 'Archiving the output file...'
//                     archiveArtifacts artifacts: env.OUTPUT_FILE, onlyIfSuccessful: true
//                 }
//             }
//         }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
    }
}

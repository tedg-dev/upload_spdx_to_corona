pipeline {
    agent any // Use any available agent

    environment {
        CORONA_PAT = credentials('corona-pat')
        CORONA_HOST = 'corona.cisco.com'
        CORONA_USERNAME = 'tedgcisco.gen'
        CORONA_ENGINEERING_CONTACT = 'tedg-corona-eng-mailer'
        CORONA_SECURITY_CONTACT = 'tedg-corona-sec-mailer'
        CORONA_PRODUCT_NAME = 'TEST - tedg - upload_spdx 2024-12-18'
        CORONA_RELEASE_VERSION = '1.0.0'
        CORONA_IMAGE_NAME = 'imageViaApi.01'
        CORONA_SPDX_FILE_PATH = './bes-traceability-spdx.json'
        DOCKER_IMAGE = 'upload_spdx'
    }

    stages {
        stage('Checkout from SCM') {
            steps {
                checkout scm
            }
        }

        stage('Setup - Install Dependencies') {
            steps {
                sh '''
                    python3 --version
                    python3.11 -m pip install --upgrade pip
                    pip -V
                    pip install requests
                    pip install pytest
                    echo $PATH
                    printenv | grep CORONA
                '''
            }
        }

//         stage('Test - Pytest') {
//             steps {
//                 // Activate the virtual environment
//                 sh 'source upload_spdx_py_venv/bin/activate'
//                 // Run tests
//                 sh 'pytest test/test_upload_spdx.py'
            }
        }

        stage('Build Docker Image as latest') {
            steps {
                // Activate the virtual environment
                sh 'source upload_spdx_py_venv/bin/activate'

                sh 'docker build -t containers.cisco.com/tedg/$DOCKER_IMAGE .'
            }
        }

        stage('Push Docker Image to containers.cisco.com') {
            steps {
                // Activate the virtual environment
                sh 'source upload_spdx_py_venv/bin/activate'

                sh'docker push containers.cisco.com/tedg/$DOCKER_IMAGE'
            }
        }

        stage('Pull Container from containers.cisco.com') {
            steps {
                // Activate the virtual environment
                sh 'source upload_spdx_py_venv/bin/activate'

                sh 'docker pull containers.cisco.com/tedg/$DOCKER_IMAGE'
            }
        }

        stage('Run Container from containers.cisco.com') {
            steps {
                // Activate the virtual environment
                sh 'source upload_spdx_py_venv/bin/activate'
                sh 'printenv | grep CORONA'

                //                 sh 'docker run -d --name upload-spdx-container containers.cisco.com/tedg/$DOCKER_IMAGE'
                sh 'docker run containers.cisco.com/tedg/$DOCKER_IMAGE'
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
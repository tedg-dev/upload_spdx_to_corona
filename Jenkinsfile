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
                    // Ensure input file exists
                    writeFile file: env.INPUT_FILE, text: "Sample input data"
                }
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

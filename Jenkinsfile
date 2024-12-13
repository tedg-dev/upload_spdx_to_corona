pipeline {
    agent any

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

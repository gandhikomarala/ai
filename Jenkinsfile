pipeline {
    agent any

    environment {
        DOCKER_IMAGE_API = 'aegisai-api:latest'
        DOCKER_IMAGE_FRONTEND = 'aegisai-frontend:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint & Static Analysis') {
            steps {
                sh 'ruff check .'
                sh 'mypy app'
            }
        }

        stage('Unit & Integration Tests') {
            steps {
                sh 'pytest -v tests/unit/ tests/integration/'
            }
        }

        stage('Security & Injection Tests') {
            steps {
                sh 'pytest -v tests/security/'
            }
        }

        stage('RAG Regression Quality Gate') {
            steps {
                sh 'python -m app.evaluation.runner'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE_API} -f docker/Dockerfile.backend .'
                sh 'docker build -t ${DOCKER_IMAGE_FRONTEND} -f docker/Dockerfile.frontend .'
            }
        }

        stage('Deploy Staging') {
            steps {
                echo 'Deploying AegisAI to Staging Cluster...'
            }
        }

        stage('Smoke Tests') {
            steps {
                sh 'curl -f http://staging.aegisai.internal/api/v1/health'
            }
        }

        stage('Production Approval') {
            steps {
                input message: 'Approve production deployment for AegisAI?'
            }
        }

        stage('Deploy Production') {
            steps {
                echo 'Promoting build to Production High-Availability Cluster...'
            }
        }
    }
}

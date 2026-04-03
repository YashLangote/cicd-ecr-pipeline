pipeline {
    agent any
    environment {
        AWS_ACCOUNT_ID = '123456789012' // Replace with your AWS Account ID
        AWS_REGION = 'eu-north-1'       // Replace with your AWS Region
        ECR_REPO_NAME = 'my-flask-app' // Replace with your ECR Repo Name
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    }
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${ECR_REPO_NAME}:${IMAGE_TAG} ."
                }
            }
        }
        stage('Push to Amazon ECR') {
            steps {
                script {
                    // 1. Authenticate Docker with AWS ECR
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}"

                    // 2. Tag the image with the Build Number and 'latest'
                    sh "docker tag ${ECR_REPO_NAME}:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPO_NAME}:${IMAGE_TAG}"
                    sh "docker tag ${ECR_REPO_NAME}:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPO_NAME}:latest"

                    // 3. Push both tags to ECR
                    sh "docker push ${ECR_REGISTRY}/${ECR_REPO_NAME}:${IMAGE_TAG}"
                    sh "docker push ${ECR_REGISTRY}/${ECR_REPO_NAME}:latest"
                }
            }
        }
    }
    post {
        always {
            cleanWs() // Clean up the workspace after the build
        }
    }
}

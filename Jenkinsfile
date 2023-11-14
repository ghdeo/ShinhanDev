pipeline {
    agent any

    environment {
        // Docker Hub 계정 정보
        DOCKER_HUB_CREDENTIALS = 'docker-hub-credentials-id'
        // Docker 이미지 이름 및 태그
        DOCKER_IMAGE_NAME = 'your-docker-image-name'
        DOCKER_IMAGE_TAG = 'latest'
    }

    stages {
        stage('Checkout') {
            steps {
                // Git 저장소에서 소스 코드 체크아웃
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                // Dockerfile이 있는 디렉토리로 이동
                dir('path/to/dockerfile') {
                    // Docker 이미지 빌드
                    script {
                        docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}")
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                // Docker 이미지를 Docker Hub에 푸시
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_HUB_CREDENTIALS) {
                        docker.image("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}").push()
                    }
                }
            }
        }
    }

    post {
        success {
            // 빌드 성공 시 추가 작업 수행
            echo 'Build and push to Docker Hub successful!'
        }

        failure {
            // 빌드 실패 시 추가 작업 수행
            echo 'Build or push to Docker Hub failed!'
        }
    }
}

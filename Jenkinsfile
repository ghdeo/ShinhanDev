pipeline {
    agent any
    
    environment {
        REPOSITORY  = 'goldencorn7'
        IMAGE       = 'shinhan'
    }

    stages {
        stage('Checkout from GitHub') {
            steps {
                // GitHub 저장소에서 소스 코드 체크아웃
                script {
                    checkout([$class: 'GitSCM', branches: [[name: '*/main']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/ghdeo/ShinhanDev.git']]])
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                // Dockerfile이 있는 디렉토리로 이동
                dir('.') {
                    // Docker 이미지 빌드
                    script {
                        def dockerfilePath = '.' // Dockerfile이 있는 디렉토리의 상대 경로
                        def contextPath = '.' // 빌드 컨텍스트의 상대 경로
                        def destination = "${REPOSITORY}/${IMAGE}:${GIT_COMMIT}"

                        // executor 명령어 대신 docker build 명령어 사용
                        sh "docker build -t ${destination} -f ${dockerfilePath}/Dockerfile ${contextPath}"
                    }
                }
            }
        }
        stage('GitOps') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'git_cre', passwordVariable: 'password', usernameVariable: 'username')]) {
                        container('gitops') {
                            git credentialsId: 'git_cre', url: 'https://github.com/junkmm/GitopsDummy.git', branch: 'main'
                            sh """
                            git init
                            git config --global --add safe.directory /home/jenkins/agent/workspace/demo
                            git config --global user.email 'jenkins@jenkins.com'
                            git config --global user.name 'jenkins'
                            sed -i 's@nginx:.*@goldencorn7/shinhan:${GIT_COMMIT}@g' deploy.yaml
                            git add deploy.yaml
                            git commit -m 'Update: Image ${GIT_COMMIT}'
                            git remote set-url origin https://${username}:${password}@github.com/ghdeo/ShinhanGitops.git
                            git push origin main
                            """
                        }
                    }
                }
            }
        }
    }
}

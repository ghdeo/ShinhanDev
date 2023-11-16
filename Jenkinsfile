pipeline {
    agent {
        kubernetes {
            yaml """
kind: Pod
metadata:
  name: kaniko
spec:
  nodeName: k8s-worker02
  dnsPolicy: Default
  containers:
  - name: kaniko
    namespace: jenkins
    image: gcr.io/kaniko-project/executor:debug
    imagePullPolicy: Always
    command:
    - /busybox/cat
    tty: true
    volumeMounts:
      - name: jenkins-docker-cfg
        mountPath: /kaniko/.docker
  - name: kubectl
    namespace: jenkins
    image: bitnami/kubectl:latest
    imagePullPolicy: Always
    command:
    - /bin/sh
    tty: true
    securityContext:
      runAsUser: 0
  volumes:
  - name: jenkins-docker-cfg
    namespace: jenkins
    projected:
      sources:
      - secret:
          name: registry-credentials
          items:
            - key: .dockerconfigjson
              path: config.json
"""
        }
    }
    environment {
        REPOSITORY  = 'goldencorn7'
        IMAGE       = 'shinhan'
    }
    stages {
        stage('Build Docker image') {
            steps {
                container('kaniko') {
                    script {
                        withCredentials([usernamePassword(credentialsId: 'docker_cre', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]){
                        sh "executor --dockerfile=Dockerfile --context=./ --destination=${REPOSITORY}/${IMAGE}:${GIT_COMMIT}"
                    }
                }
            }
        }
    }
        stage('Deploy') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        container('kubectl') {
                            sh """
                            export KUBECONFIG=\$KUBECONFIG
                            kubectl set image deployment/test test=${REPOSITORY}/${IMAGE}:${GIT_COMMIT} -n demo
                            kubectl rollout restart deployment/test -n demo
                            """
                        }
                    }
                }
            }
        }
    }
}


pipeline {
    agent any

    environment {
        REGISTRY   = 'docker.io'
        IMAGE_NAME = 'janetjohn15/devops-task-tracker'
    }

    stages {
        stage('CI Pipeline Initialization') {
            steps {
                echo "Starting pipeline for registry: ${env.REGISTRY}"
                echo "Target image name: ${env.IMAGE_NAME}"
            }
        }

        stage('Checkout The Repository Code') {
            steps {
                echo 'Checking out repository code'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo 'Create Python virtual environment'
                sh 'python3 -m venv venv'

                echo 'Install dependencies'
                sh './venv/bin/python -m pip install --upgrade pip'
                
                echo 'Install pytest'
                sh './venv/bin/python -m pip install pytest'
                
                echo 'Run tests'
                sh './venv/bin/python -m pytest'
            }
        }

        stage('Login To Docker') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-credentials',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set -e
                        echo "$DOCKERHUB_TOKEN" | docker login \
                            -u "$DOCKERHUB_USERNAME" \
                            --password-stdin
                    '''
                }
            }
        }

        stage('Build and Push Docker Image') {
            when {
                branch 'master'
            }

            steps {
                script {
                    def fullSha = env.GIT_COMMIT
                    def image = "${env.REGISTRY}/${env.IMAGE_NAME}"

                    echo "Building Docker image"

                    sh "docker build -t '${image}:latest' -t '${image}:${fullSha}' ."

                    echo "Pushing Docker images to Docker Hub"

                    sh "docker push '${image}:latest'"
                    sh "docker push '${image}:${fullSha}'"
                }
            }
        }

        stage('Deploy Via SSH') {
            when {
                branch 'master'
            }

            environment {
                SSH_HOST = '0.tcp.in.ngrok.io'
                SSH_PORT = '24894'
                SSH_USER = 'janet_john'
            }

            steps {
                sshagent(['ssh-server-credentials']) {
                    sh """
                        set -e

                        echo "Connecting to remote server..."

                        ssh -o StrictHostKeyChecking=no \
                            -p "\${SSH_PORT}" \
                            "\${SSH_USER}@\${SSH_HOST}" << EOF

                            set -e
                            echo "Connected to the remote server"

                            cd /mnt/c/Users/user/Documents/Ansible_workflow/devops-task-tracker

                            git pull --ff-only origin master

                            ansible-playbook --syntax-check deploy.yml

                            export IMAGE_TAG='${env.GIT_COMMIT}'

                            ansible-playbook deploy.yml

                        EOF
                    """
                }
            }
        }
    }
}

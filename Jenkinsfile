pipeline{
    agent any

    environment{
        registry: docker.io
        image_name: janetjohn15/devops-task-tracker
    }

    stages{
        stage('CI Pipeline Initialization'){
            steps{
                echo "Starting pipleine for registry: ${env.registry}"
                echo "Target Image Name: ${env.image_name}"
            }
        }

        stage('Checkout The Repository Code'){
            steps{
                echo "Copying The Repo Code"
                checkout scm
            }
        }

        stage('Test'){
            steps{
                echo 'Install Python Virtual Environment'
                sh 'python3 -m venv venv'

                echo 'Install dependencies'
                sh './venv/bin/python -m pip install --upgrade pip'
                
                echo 'Run the tests'
                sh './venv/bin/pytest'
            
            }

        }

        stage('Login To Docker'){
            steps{
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-credentials',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ])
                 {
                    sh '''
                        echo "$DOCKERHUB_TOKEN2" | docker login \
                        -u "$DOCKERHUB_USERNAME" \
                        --password-stdin
                    '''
                }
            }
        }

        stage('Build and push Docker Image'){
            when{
                branch 'master'
            }
            steps{
                def fullsha = env.GIT_COMMIT
                echo "Build a Docker Image"
                sh "docker build -t '${env.registry}/${env.image_name}':latest"
                sh "docker build -t '${env.registry}/${env.image_name}:${fullsha}'"

                echo "Push Docker image to Hub"
                sh "docker push '${env.registry}/${env.image_name}':latest"
                sh "docker push '${env.registry}/${env.image_name}:${fullsha}'"
            }
        }

        stage('Deploy Via SSH') {
            environment {
                // Change these three values to match your ngrok status and WSL account

                SSH_HOST = '0.tcp.in.ngrok.io' 
                SSH_PORT = '24894' 

                SSH_USER = 'janet_john' 
            }
            steps {
                sshagent(['ssh-server-credentials']) {
                    sh """
                        set -e
                        echo "Connecting to remote server..."

                        ssh -o StrictHostKeyChecking=no -p "${SSH_PORT}" "${SSH_USER}@${SSH_HOST}" << 'EOF'
                            set -e
                            echo "Connected to the Remote server"
                            cd /mnt/c/Users/user/Documents/Ansible_workflow
                            git pull --ff-only origin master
                            ansible-playbook --syntax-check deploy.yml
                            export IMAGE_TAG="${fullSha}"
                            ansible-playbook deploy.yml
                            
                        """
        }

    }
}
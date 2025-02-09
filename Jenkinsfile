pipeline {
    agent any
    environment {
        GITHUB_TOKEN = credentials('github-token-id')
        BIRTHDAY = "12 March, 2004"  // Replace with your actual birthdate (YYYY-MM-DD)
        ACCESS_TOKEN = credentials('github-token-id') // Uses Jenkins credential
        USER_NAME = "hoangpham6337" // Replace with your GitHub username
    }
    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', credentialsId: 'github-token-id', url: 'https://github.com/${USER_NAME}/${USER_NAME}.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Generate Markdown') {
            steps {
                sh 'python3 generate_markdown.py'
            }
        }
        stage('Commit & Push') {
            steps {
                sh '''
                git config --global user.email "hoangpham4171@gmail.com"
                git config --global user.name "HoangPham6337"
                git add README.md
                git commit -m "Auto-update GitHub Markdown"
                git push https://${GITHUB_TOKEN}@github.com/${USER_NAME}/${USER_NAME}.git
                '''
            }
        }
    }
}
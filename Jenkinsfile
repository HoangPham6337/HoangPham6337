pipeline {
    agent any
    environment {
        TOKEN = credentials('github-token-id')
        GITHUB_TOKEN = credentials('github-token')
        BIRTHDAY = credentials('birthday')
        USER_NAME = "hoangpham6337"
    }
    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', credentialsId: 'github-token-id', url: 'https://github.com/HoangPham6337/HoangPham6337.git'
            }
        }
        stage('Setup Virtual Environment') {
            steps {
                sh 'python3 -m venv venv'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                venv/bin/pip install --upgrade pip
                venv/bin/pip install -r requirements.txt
                '''
            }
        }
        stage('Generate Markdown') {
            steps {
                    sh 'venv/bin/python generate_markdown.py'
            }
        }
        stage('Commit & Push') {
            steps {
                sh '''
                git config --global user.email "hoangpham4171@gmail.com"
                git config --global user.name "HoangPham6337"
                git add README.md
                if ! git diff --cached --quiet; then
                    git commit -m "Auto-update GitHub Markdown"
                    git push https://${TOKEN}@github.com/HoangPham6337/HoangPham6337.git
                else
                    echo "No changes to commit"
                fi
                '''
            }
        }
    }
}
pipeline {
    agent any
    environment {
        GITHUB_TOKEN = credentials('github-token-id')
        BIRTHDAY = "12 March, 2004"
        ACCESS_TOKEN = credentials('github-token-id')
        USER_NAME = "hoangpham6337"
        PYTHON_BIN = "/usr/bin/python3"
    }
    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', credentialsId: 'github-token-id', url: 'https://github.com/HoangPham6337/HoangPham6337.git'
            }
        }
        stage('Setup Virtual Environment') {
            steps {
                sh '''
                ${PYTHON_BIN} -m venv venv
                '''
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }
        stage('Generate Markdown') {
            steps {
                sh '''
                . venv/bin/activate
                sh 'python3 generate_markdown.py'
                '''
            }
        }
        stage('Commit & Push') {
            steps {
                sh '''
                git config --global user.email "hoangpham4171@gmail.com"
                git config --global user.name "HoangPham6337"
                git add README.md
                git commit -m "Auto-update GitHub Markdown"
                git push https://${GITHUB_TOKEN}@github.com/HoangPham6337/HoangPham6337.git
                '''
            }
        }
    }
}
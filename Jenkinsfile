pipeline {
    agent {
        docker {
            image 'python:3.12-slim'
            args '--shm-size=2g'
        }
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
    }

    triggers {
        githubPush()
    }

    environment {
        BROWSER         = 'chrome'
        PYTHONPATH      = "${WORKSPACE}"
        DEBIAN_FRONTEND = 'noninteractive'
    }

    stages {

        stage('Install System Dependencies') {
            steps {
                sh '''
                    apt-get update -qq
                    apt-get install -y -qq \
                        wget curl gnupg unzip \
                        fonts-liberation libappindicator3-1 libasound2 \
                        libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 \
                        libgtk-3-0 libnss3 libxss1 libxtst6 xdg-utils libgbm1

                    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
                    apt-get install -y ./google-chrome-stable_current_amd64.deb || apt-get install -yf
                    rm google-chrome-stable_current_amd64.deb

                    echo "Chrome version: $(google-chrome --version)"
                '''
            }
        }

        stage('Install Python Dependencies') {
            steps {
                sh '''
                    pip install --upgrade pip -q
                    pip install -r requirements.txt -q
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    mkdir -p reports screenshots
                    pytest tests/ \
                        --browser=chrome \
                        --html=reports/report.html \
                        --self-contained-html \
                        --junit-xml=reports/junit.xml \
                        -v \
                        || true
                '''
            }
        }
    }

    post {
        always {
            publishHTML(target: [
                allowMissing         : true,
                alwaysLinkToLastBuild: true,
                keepAll              : true,
                reportDir            : 'reports',
                reportFiles          : 'report.html',
                reportName           : 'Pytest HTML Report'
            ])

            archiveArtifacts(
                artifacts: 'screenshots/*.png,reports/report.html',
                allowEmptyArchive: true
            )

            junit(
                testResults: 'reports/junit.xml',
                allowEmptyResults: true
            )
        }

        success {
            echo '✅ All tests passed!'
        }

        failure {
            echo '❌ Some tests failed. Check the report.'
        }
    }
}
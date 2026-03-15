pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
    }

    triggers {
        githubPush()
    }

    environment {
        PYTHONPATH     = "${WORKSPACE}"
        SELENIUM_HOST  = "selenium-chrome-${BUILD_NUMBER}"
        SELENIUM_URL   = "http://selenium-chrome-${BUILD_NUMBER}:4444/wd/hub"
    }

    stages {

        stage('Start Selenium Grid') {
            steps {
                sh '''
                    docker run -d \
                        --name selenium-chrome-${BUILD_NUMBER} \
                        --network insider-test-network \
                        --shm-size=2g \
                        seleniarm/standalone-chromium:latest

                    echo "Waiting for Selenium Grid..."
                    sleep 15
                    echo "Selenium Grid should be ready"
                '''
            }
        }

        stage('Install Python Dependencies') {
            steps {
                sh '''
                    apt-get install -y -qq python3-venv
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip -q
                    pip install -r requirements.txt -q
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    mkdir -p reports screenshots
                    SELENIUM_REMOTE_URL=${SELENIUM_URL} pytest tests/ \
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
            sh 'docker rm -f selenium-chrome-${BUILD_NUMBER} || true'

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
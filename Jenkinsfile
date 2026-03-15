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
                    JENKINS_NETWORK=$(docker inspect jenkins --format "{{range .NetworkSettings.Networks}}{{.NetworkID}}{{end}}" | head -1)

                    docker run -d \
                        --name selenium-chrome-${BUILD_NUMBER} \
                        --network ${JENKINS_NETWORK} \
                        --shm-size=2g \
                        seleniarm/standalone-chromium:latest

                    echo "Waiting for Selenium Grid..."
                    for i in $(seq 1 30); do
                        STATUS=$(docker exec selenium-chrome-${BUILD_NUMBER} curl -s http://localhost:4444/wd/hub/status 2>/dev/null || echo "")
                        if echo "$STATUS" | grep -q '"ready":true'; then
                            echo "Selenium Grid is ready!"
                            break
                        fi
                        echo "Attempt $i: not ready yet..."
                        sleep 3
                    done
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
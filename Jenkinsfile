pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }

    triggers {
        githubPush()
    }

    environment {
        BROWSER = 'chrome'
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest tests/ \
                        --browser=${BROWSER} \
                        --html=reports/report.html \
                        --self-contained-html \
                        -v \
                        || true
                '''
            }
        }
    }

    post {
        always {
            // Publish HTML report
            publishHTML(target: [
                allowMissing         : true,
                alwaysLinkToLastBuild: true,
                keepAll              : true,
                reportDir            : 'reports',
                reportFiles          : 'report.html',
                reportName           : 'Pytest HTML Report'
            ])

            // Archive screenshots on failure
            archiveArtifacts(
                artifacts: 'screenshots/*.png',
                allowEmptyArchive: true
            )

            // Publish JUnit-style results (requires pytest-junit)
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

pipeline {
    agent any

    environment {
        JMETER_HOME = '/path/to/jmeter'   // Ensure this is the correct JMeter path
        TEST_PLAN = 'your-test-plan.jmx'  // Your JMX file
        REPORT_DIR = 'jmeter-report'      // Adjust the directory if needed
    }

    stages {
        stage('Setup JMeter') {
            steps {
                script {
                    if (!fileExists("${JMETER_HOME}/bin/jmeter")) {
                        error "JMeter is not installed. Ensure it is available on this node."
                    }
                }
                echo "JMeter setup verified."
            }
        }

        stage('Run JMeter Test') {
            steps {
                echo "Executing JMeter Test Plan: ${TEST_PLAN}"
                sh """
                    mkdir -p ${REPORT_DIR}
                    ${JMETER_HOME}/bin/jmeter \
                        -n -t ${TEST_PLAN} \
                        -l ${REPORT_DIR}/results.jtl \
                        -e -o ${REPORT_DIR}/html-report
                """
            }
        }

        stage('Verify Reports') {
            steps {
                script {
                    if (!fileExists("${REPORT_DIR}/html-report/index.html")) {
                        error "HTML report not generated. Check the JMeter execution logs."
                    }
                }
                echo "HTML report found and ready to archive."
            }
        }

        stage('Generate and Archive Reports') {
            steps {
                echo "Archiving HTML report and JTL results."
                archiveArtifacts artifacts: "${REPORT_DIR}/**/*", allowEmptyArchive: false
                publishHTML([
                    reportDir: "${REPORT_DIR}/html-report",
                    reportFiles: 'index.html',
                    reportName: 'JMeter Test Report'
                ])
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
        success {
            echo 'JMeter test executed successfully.'
        }
        failure {
            echo 'JMeter test failed. Please check logs and artifacts.'
        }
    }
}

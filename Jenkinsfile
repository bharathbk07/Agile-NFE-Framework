pipeline {
    agent any

    environment {
        JMETER_HOME = '/Users/bharathkumarm/apache-jmeter-5.6.3'   // Set the JMeter path here (if installed manually)
        TEST_PLAN = '/Users/bharathkumarm/Docker/JmeterScript/Wordsmith.jmx'  // Your JMX file
        REPORT_DIR = '/Users/bharathkumarm/Docker/JmeterScript/jmeter-report'
    }

    stages {
        stage('Cleanup Previous Reports') {
            steps {
                echo "Checking for existing JMeter report folder."
                script {
                    if (fileExists(REPORT_DIR)) {
                        echo "Found existing report directory. Deleting..."
                        sh "rm -rf ${REPORT_DIR}"
                    } else {
                        echo "No existing report directory found. Proceeding..."
                    }
                }
            }
        }

        stage('Setup JMeter') {
            steps {
                script {
                    if (!fileExists("${JMETER_HOME}/bin/jmeter")) {
                        error "JMeter is not installed or not available on this node."
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

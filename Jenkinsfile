pipeline {
    agent none

    environment {
        config = readYaml file: 'configfile.yml'  // Read the YAML configuration
        JMETER_HOME = config.tests.jmeter.JMETER_HOME
        TEST_PLAN = config.tests.jmeter.TEST_PLAN
        REPORT_DIR = config.tests.jmeter.REPORT_DIR
        ATTACK_ID = ''
    }

    parameters {
        string(name: 'TARGET_IDENTIFIER', defaultValue: config.tests.chaos_experiment.TARGET_IDENTIFIER, description: 'Host to target')
        string(name: 'CPU_LENGTH', defaultValue: "${config.tests.chaos_experiment.CPU_LENGTH}", description: 'Duration of CPU attack')
        string(name: 'CPU_CORE', defaultValue: "${config.tests.chaos_experiment.CPU_CORE}", description: 'Number of cores to impact')
        string(name: 'CPU_CAPACITY', defaultValue: "${config.tests.chaos_experiment.CPU_CAPACITY}", description: 'Percentage of total CPU capacity to consume')
    }

    stages {
        stage('Cleanup Previous Reports') {
            agent any
            when {
                expression { config.tests.jmeter.enabled }  // Run only if JMeter is enabled
            }
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
            agent any
            when {
                expression { config.tests.jmeter.enabled }  // Run only if JMeter is enabled
            }
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
            agent any
            when {
                expression { config.tests.jmeter.enabled }  // Run only if JMeter is enabled
            }
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

        stage('Run Chaos Experiment') {
            agent any
            when {
                expression { config.tests.chaos_experiment.enabled }  // Run only if chaos experiment is enabled
            }
            steps {
                withCredentials([
                    string(credentialsId: 'GREMLIN_API_KEY', variable: 'GREMLIN_API_KEY'),
                    string(credentialsId: 'GREMLIN_TEAM_ID', variable: 'GREMLIN_TEAM_ID')
                ]) {
                    script {
                        ATTACK_ID = sh(
                            script: """
                                curl -s -H 'Content-Type: application/json;charset=utf-8' \
                                -H 'Authorization: Key ${GREMLIN_API_KEY}' \
                                https://api.gremlin.com/v1/attacks/new?teamId=${GREMLIN_TEAM_ID} \
                                --data '{
                                    "command": {
                                        "type": "cpu",
                                        "args": ["-c", "${CPU_CORE}", "-l", "${CPU_LENGTH}", "-p", "${CPU_CAPACITY}"]
                                    },
                                    "target": {
                                        "type": "Exact",
                                        "hosts": { "ids": ["${TARGET_IDENTIFIER}"] }
                                    }
                                }' --compressed
                            """, 
                            returnStdout: true
                        ).trim()
                        echo "View your experiment at https://app.gremlin.com/attacks/${ATTACK_ID}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
        success {
            echo 'Pipeline executed successfully.'
        }
        failure {
            echo 'Pipeline failed. Please check logs and artifacts.'
        }
    }
}

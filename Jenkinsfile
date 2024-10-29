pipeline {
    agent none

    environment {
        ATTACK_ID = ''
    }

    stages {
        stage('Load Configuration') {
            agent any
            steps {
                script {
                    // Load the YAML configuration file
                    def config = readYaml file: 'configfile.yml'

                    // Set environment variables based on the configuration
                    env.JMETER_HOME = config.tests.jmeter.JMETER_HOME
                    env.TEST_PLAN = config.tests.jmeter.TEST_PLAN
                    env.REPORT_DIR = config.tests.jmeter.REPORT_DIR

                    // Store chaos experiment values as local variables
                    def targetIdentifier = config.tests.chaos_experiment.TARGET_IDENTIFIER
                    def cpuLength = config.tests.chaos_experiment.CPU_LENGTH
                    def cpuCore = config.tests.chaos_experiment.CPU_CORE
                    def cpuCapacity = config.tests.chaos_experiment.CPU_CAPACITY

                    // Read enabled status
                    def jmeterEnabled = config.tests.jmeter.enabled
                    def chaosEnabled = config.tests.chaos_experiment.enabled

                    // Logging for debugging
                    echo "JMeter Enabled: ${jmeterEnabled}"
                    echo "Chaos Experiment Enabled: ${chaosEnabled}"
                    echo "Target Identifier: ${targetIdentifier}"
                    echo "CPU Length: ${cpuLength}"
                    echo "CPU Core: ${cpuCore}"
                    echo "CPU Capacity: ${cpuCapacity}"

                    // Setting these as environment variables for later use
                    env.JMETER_ENABLED = jmeterEnabled.toString()
                    env.CHAOS_ENABLED = chaosEnabled.toString()
                    env.TARGET_IDENTIFIER = targetIdentifier
                    env.CPU_LENGTH = "${cpuLength}"
                    env.CPU_CORE = "${cpuCore}"
                    env.CPU_CAPACITY = "${cpuCapacity}"
                }
            }
        }

        stage('Setup JMeter') {
            agent any
            when {
                expression { env.JMETER_ENABLED == 'true' }  // Run only if JMeter is enabled
            }
            steps {
                script {
                    if (!fileExists("${env.JMETER_HOME}/bin/jmeter")) {
                        error "JMeter is not installed or not available on this node."
                    }
                }
                echo "JMeter setup verified."
            }
        }

        stage('Run JMeter Test') {
            agent any
            when {
                expression { env.JMETER_ENABLED == 'true' }  // Run only if JMeter is enabled
            }
            steps {
                echo "Executing JMeter Test Plan: ${env.TEST_PLAN}"
                sh """
                    mkdir -p ${env.REPORT_DIR}
                    ${env.JMETER_HOME}/bin/jmeter \
                        -n -t ${env.TEST_PLAN} \
                        -l ${env.REPORT_DIR}/results.jtl \
                        -e -o ${env.REPORT_DIR}/html-report
                """
            }
        }

        stage('Run Chaos Experiment') {
            agent any
            when {
                expression { env.CHAOS_ENABLED == 'true' }  // Run only if chaos experiment is enabled
            }
            steps {
                withCredentials([
                    string(credentialsId: 'GREMLIN_API_KEY', variable: 'GREMLIN_API_KEY'),
                    string(credentialsId: 'GREMLIN_TEAM_ID', variable: 'GREMLIN_TEAM_ID')
                ]) {
                    script {
                        // Use local variables for chaos experiment values
                        ATTACK_ID = sh(
                            script: """
                                curl -s -H 'Content-Type: application/json;charset=utf-8' \
                                -H 'Authorization: Key ${GREMLIN_API_KEY}' \
                                https://api.gremlin.com/v1/attacks/new?teamId=${GREMLIN_TEAM_ID} \
                                --data '{
                                    "command": {
                                        "type": "cpu",
                                        "args": ["-c", "${env.CPU_CORE}", "-l", "${env.CPU_LENGTH}", "-p", "${env.CPU_CAPACITY}"]
                                    },
                                    "target": {
                                        "type": "Exact",
                                        "hosts": { "ids": ["${env.TARGET_IDENTIFIER}"] }
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
            cleanWs()  // Clean the workspace after pipeline execution
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

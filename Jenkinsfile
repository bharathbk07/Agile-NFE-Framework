pipeline {
    agent {
        label 'localhost_mac'  // Ensure the job runs on your Mac agent
    }

    environment {
        PROJECT_DIR = 'project_source_code'  // Directory for cloning and scanning
        ATTACK_ID = ''
        SONARQUBE_URL = 'http://localhost:9000'
    }

    tools {
        maven 'Maven'  // Use the configured Maven installation
    }

    stages {
        stage('Load Configuration') {
            steps {
                script {
                    def config = readYaml file: 'configfile.yml'

                    // Set environment variables from the YAML config
                    env.JMETER_HOME = config.tests.jmeter.JMETER_HOME
                    env.TEST_PLAN = config.tests.jmeter.TEST_PLAN
                    env.REPORT_DIR = config.tests.jmeter.REPORT_DIR
                    env.JMETER_ENABLED = config.tests.jmeter.enabled.toString()
                    env.CHAOS_ENABLED = config.tests.chaos_experiment.enabled.toString()
                    
                    // Chaos experiment variables
                    env.TARGET_IDENTIFIER = config.tests.chaos_experiment.TARGET_IDENTIFIER
                    env.CPU_LENGTH = "${config.tests.chaos_experiment.CPU_LENGTH}"
                    env.CPU_CORE = "${config.tests.chaos_experiment.CPU_CORE}"
                    env.CPU_CAPACITY = "${config.tests.chaos_experiment.CPU_CAPACITY}"

                    // GitHub project details
                    env.GITHUB_REPO = config.project.github_repo
                    env.BRANCH_NAME = config.project.branch_name

                    echo "Loaded configuration successfully."
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    echo "Cloning repository: ${env.GITHUB_REPO} from branch: ${env.BRANCH_NAME}"
                    dir(env.PROJECT_DIR) {
                        git(url: "${env.GITHUB_REPO}", branch: "${env.BRANCH_NAME}")
                    }
                }
            }
        }

        stage('Static Code Analysis (SonarQube)') {
            steps {
                withSonarQubeEnv('Wordsmith') {
                    withCredentials([string(credentialsId: 'SonarQube_Wordsmith', variable: 'SONAR_TOKEN')]) {
                        script {
                            dir("${env.PROJECT_DIR}/api") {
                                sh """
                                mvn clean verify sonar:sonar \
                                  -Dsonar.projectKey=Wordsmith \
                                  -Dsonar.projectName='Wordsmith' \
                                  -Dsonar.host.url=${SONARQUBE_URL} \
                                  -Dsonar.login=${SONAR_TOKEN}
                                """
                            }
                        }
                    }
                }
            }
        }

        stage('Validate and Deploy Docker') {
            steps {
                script {
                    // Validate Docker is running
                    def dockerRunning = sh(script: "docker info", returnStatus: true) == 0
                    if (!dockerRunning) {
                        error "Docker is not running. Please start Docker and retry."
                    }
                    echo "Docker is running."

                    // Build and Deploy with Docker Compose
                    dir(env.PROJECT_DIR) {
                        sh "docker compose up --build -d"
                        def runningContainers = sh(script: "docker ps --format '{{.Names}}'", returnStdout: true).trim()
                        if (runningContainers) {
                            echo "Running containers: ${runningContainers}"
                        } else {
                            error "No containers are running. Please check your Docker setup."
                        }
                    }
                }
            }
        }

        stage('JMeter Performance Testing') {
            when {
                expression { env.JMETER_ENABLED == 'true' }
            }
            steps {
                script {
                    if (!fileExists("${env.JMETER_HOME}/bin/jmeter")) {
                        error "JMeter is not installed or not available on this node."
                    }
                    echo "JMeter setup verified."

                    // Clean old reports if they exist
                    if (fileExists(env.REPORT_DIR)) {
                        echo "Found existing report directory. Deleting..."
                        sh "rm -rf ${env.REPORT_DIR}"
                    }
                    echo "Ready for JMeter testing."

                    // Run Performance Test
                    sh """
                    mkdir -p ${env.REPORT_DIR}
                    ${env.JMETER_HOME}/bin/jmeter -n -t ${env.TEST_PLAN} \
                        -l ${env.REPORT_DIR}/results.jtl \
                        -e -o ${env.REPORT_DIR}/html-report
                    """
                    echo "Performance test completed. Reports generated at ${env.REPORT_DIR}/html-report."
                }
            }
        }

        stage('Run Chaos Experiment') {
            when {
                expression { env.CHAOS_ENABLED == 'true' }
            }
            steps {
                withCredentials([
                    string(credentialsId: 'GREMLIN_API_KEY', variable: 'GREMLIN_API_KEY'),
                    string(credentialsId: 'GREMLIN_TEAM_ID', variable: 'GREMLIN_TEAM_ID')
                ]) {
                    script {
                        // Pass credentials as environment variables within the sh block
                        ATTACK_ID = sh(
                            script: '''
                                export API_KEY=$GREMLIN_API_KEY
                                export TEAM_ID=$GREMLIN_TEAM_ID
                                curl -s -H "Content-Type: application/json;charset=utf-8" \
                                    -H "Authorization: Key $API_KEY" \
                                    "https://api.gremlin.com/v1/attacks/new?teamId=$TEAM_ID" \
                                    --data '{
                                        "command": {
                                            "type": "cpu",
                                            "args": ["-c", "'${CPU_CORE}'", "-l", "'${CPU_LENGTH}'", "-p", "'${CPU_CAPACITY}'"]
                                        },
                                        "target": {
                                            "type": "Exact",
                                            "hosts": { "ids": ["'${TARGET_IDENTIFIER}'"] }
                                        }
                                    }' --compressed
                            ''',
                            returnStdout: true
                        ).trim()

                        echo "Chaos experiment initiated. View details at: https://app.gremlin.com/attacks/${ATTACK_ID}"
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()  // Clean up workspace after pipeline execution
            echo 'Pipeline execution completed.'
        }
        success {
            echo 'Pipeline executed successfully.'
        }
        failure {
            echo 'Pipeline failed. Please review logs and artifacts.'
        }
    }
}
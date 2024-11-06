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
        stage('Load Job Configuration') {
            steps {
                script {
                    // Load configuration from YAML file
                    def config = readYaml file: 'configfile.yml'

                    // Set environment variables from the YAML config
                    env.JMETER_HOME = config.tests.jmeter.JMETER_HOME
                    env.TEST_PLAN = config.tests.jmeter.TEST_PLAN
                    env.REPORT_DIR = config.tests.jmeter.REPORT_DIR
                    env.JMETER_ENABLED = config.tests.jmeter.enabled.toString()
                    env.CHAOS_ENABLED = config.tests.chaos_experiment.enabled.toString()
                    
                    // Chaos experiment variables
                    env.TARGET_IDENTIFIER = config.tests.chaos_experiment.TARGET_IDENTIFIER ?: ''
                    env.CPU_LENGTH = "${config.tests.chaos_experiment.CPU_LENGTH}"
                    env.CPU_CORE = "${config.tests.chaos_experiment.CPU_CORE}"
                    env.CPU_CAPACITY = "${config.tests.chaos_experiment.CPU_CAPACITY}"

                    // GitHub project details
                    env.GITHUB_REPO = config.project.github_repo
                    env.BRANCH_NAME = config.project.branch_name

                    // Email settings
                    env.SEND_EMAIL = config.email.sendEmail.toString()
                    env.EMAIL_RECIPIENTS = config.email.recipients
                    env.EMAIL_SENDER = config.email.sender
                    env.EMAIL_SUBJECT = config.email.subject
                    env.EMAIL_REPLY_TO = config.email.replyTo
                    
                    // Read attachments from config
                    def attachmentsList = config.email.attachments.collect { it }.join(",")
                    env.ATTACHMENTS = attachmentsList

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

        stage('Health Check and API Validation') {
            steps {
                script {
                    // List of containers to check, using the environment variable
                    def containers = [
                        "${env.PROJECT_DIR}-api-4",
                        "${env.PROJECT_DIR}-api-5",
                        "${env.PROJECT_DIR}-api-2",
                        "${env.PROJECT_DIR}-db-1",
                        "${env.PROJECT_DIR}-api-3",
                        "${env.PROJECT_DIR}-api-1",
                        "${env.PROJECT_DIR}-web-1"
                    ]

                    // Check the status of each container
                    def notRunning = []
                    containers.each { container ->
                        def status = sh(script: "docker inspect --format='{{.State.Status}}' ${container} 2>/dev/null", returnStdout: true).trim()
                        if (status != 'running') {
                            notRunning.add(container)
                        }
                    }

                    // If any container is not running, fail the job
                    if (notRunning) {
                        error "The following containers are not running: ${notRunning.join(', ')}"
                    } else {
                        echo "All specified containers are running."

                        // Proceed to check API health if all containers are running
                        def apiResponse = sh(script: "curl -s 'http://localhost:8080/words/noun?n=1'", returnStdout: true).trim()

                        // Check if the API response contains the word "words"
                        if (apiResponse.contains("word")) {
                            echo "Application is working."
                        } else {
                            error "Application is not working. Terminating the process."
                        }
                    }
                }
            }
        }

        stage('Performance Testing (JMeter)') {
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

        stage('Chaos Testing (Gremlin)') {
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
                        env.ATTACK_ID = sh(script: """
                            curl --location 'https://api.gremlin.com/v1/attacks/new?teamId=${GREMLIN_TEAM_ID}' \
                                    --header 'Content-Type: application/json;charset=utf-8' \
                                    --header 'Authorization: Key ${GREMLIN_API_KEY}' \
                            --data '{
                                "command": {
                                    "type": "cpu",
                                    "args": ["-c", "${env.CPU_CORE}", "-l", "${env.CPU_LENGTH}", "-p", "${env.CPU_CAPACITY}"]
                                },
                                "target": {
                                    "type": "Exact",
                                    "hosts": { "ids": ["${env.TARGET_IDENTIFIER}"] }
                                }
                            }' --compressed || true
                        """, returnStdout: true).trim()

                        echo "Chaos experiment initiated. View details at: https://app.gremlin.com/attacks/${env.ATTACK_ID}"
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                    // Get values to replace in the templates
                    def projectName = env.JOB_NAME // Name of the project/job
                    def buildNumber = env.BUILD_NUMBER // Jenkins build number
                    def timestamp = new Date().format("yyyy-MM-dd HH:mm:ss") // Current timestamp
                    // Check the current build result, defaulting to 'SUCCESS' if it's null
                    def buildResult = currentBuild.result ?: 'SUCCESS' // Default to 'SUCCESS' if null


                    // Prepare email content based on build result
                    def emailBodyContent
                    def emailSubject = "${env.EMAIL_SUBJECT} - Build ${buildResult}"
                    echo "Current Build Status: ${buildResult}."

                    if (buildResult == 'SUCCESS') {
                        sh "python ./Python/json_html_conv.py ${env.REPORT_DIR}/html-report"
                        emailBodyContent = readFile 'Templates/success.html' // Store success template in environment variable
                    } else {
                        emailBodyContent = readFile 'Templates/failure.html' // Store failure template in environment variable
                    }

                    // Replace placeholders with actual values
                    emailBodyContent = emailBodyContent
                        .replace('${PROJECT_NAME}', projectName)
                        .replace('${BUILD_NUMBER}', buildNumber)
                        .replace('${TIMESTAMP}', timestamp)

                    // Write the email body content to a temporary file
                    def emailBodyFile = 'emailBodyContent.html'
                    writeFile file: emailBodyFile, text: emailBodyContent

                    // Send email using mail step
                    emailext(
                        to: env.EMAIL_RECIPIENTS,
                        from: env.EMAIL_SENDER,
                        subject: emailSubject,
                        body: readFile(emailBodyFile),
                        replyTo: env.EMAIL_REPLY_TO,
                        attachLog: true,  // Attach build log
                        attachments: "${env.ATTACHMENTS}"  // Attach specified files
                    )
                }
            //cleanWs()  // Clean up workspace after pipeline execution
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

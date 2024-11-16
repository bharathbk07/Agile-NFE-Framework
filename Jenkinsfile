pipeline {
    agent {
        label 'localhost_mac'  // Ensure the job runs on your Mac agent
    }

    environment {
        PROJECT_DIR = 'project_source_code'  // Directory for cloning and scanning
        ATTACK_ID = ''
        SONARQUBE_URL = 'http://localhost:9000'
        PATH = "${tool 'Nodejs'}/bin:${env.PATH}"  // Set PATH to include the Node.js bin folder from the NodeJS installation
        JIRA_SITE = 'https://mkumarbharath50.atlassian.net'
        SLACK_CHANNEL = '#social' // Slack channel for testing
    }

    tools {
        maven 'Maven'  // Use the configured Maven installation
    }

    stages {
        stage('Sustainability Monitor (psutil)') {
            steps {
                script {
                    echo "Starting Sustainability Monitoring in the background."
                    sh "nohup python Python/sustainability.py start &"
                }
            }
        }

        stage('Load Job Configuration') {
            steps {
                script {
                    // Load configuration from YAML file
                    def config = readYaml file: 'configfile.yml'

                    // Postman Collection
                    env.POSTMAN_ENABLED = config.tests.postman.enable.toString()
                    env.POSTAM_FOLDER_LOC = config.tests.postman.FOLDER_NAME

                    // Set environment variables from the YAML config
                    env.JMETER_HOME = config.tests.jmeter.JMETER_HOME
                    env.TEST_PLAN = config.tests.jmeter.TEST_PLAN
                    env.REPORT_DIR = config.tests.jmeter.REPORT_DIR
                    env.JMETER_ENABLED = config.tests.jmeter.enabled.toString()
                    
                    // Chaos experiment variables
                    env.CHAOS_ENABLED = config.tests.chaos_experiment.enabled.toString()
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

                    //Jira Comment
                    env.ISSUE_KEY = config.jira.issue_key

                    // Set environment variables based on config
                    env.LIGHTHOUSE_RUN = config.tests.lighthouse.enabled.toString()
                    env.LIGHTHOUSE_URL = config.tests.lighthouse.url

                    // Accessibility Testing
                    env.accessibility_RUN = config.tests.accessibility.enabled.toString()
                    env.accessibility_URL = config.tests.lighthouse.url
                    
                    // Read attachments from config
                    def attachmentsList = config.email.attachments.collect { it }.join(",")
                    env.ATTACHMENTS = attachmentsList
                    echo "Attachments List ${env.ATTACHMENTS}"
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

        stage('Validate and Deploy (Docker)') {
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

        stage('Front-End Testing (Lighthouse)') {
            when {
                expression { env.LIGHTHOUSE_RUN == 'true' }
            }
            steps {
                sh """
                lighthouse ${env.LIGHTHOUSE_URL} \
                    --output html \
                    --output-path lighthouse_report.html \
                    --no-enable-error-reporting \
                    --chrome-flags="--headless"
                """
            }
        }

        stage('Accessibility Testing (Pa11y)') {
            when {
                expression { env.accessibility_RUN == 'true' }
            }
            steps {
                sh """
                pa11y ${env.accessibility_URL} > accessibility_report.csv --reporter csv || true
                """
            }
        }

        stage('PT Script Creation (Postman)') {
            when {
                expression { env.POSTMAN_ENABLED == 'true' }
            }
            steps {
                sh """
                python Python/postman2jmx.py Postman_Collection || true
                """
                script {
                    if (fileExists("${env.TEST_PLAN}")) {             
                        withCredentials([
                            string(credentialsId: 'DataDog', variable: 'DataDog'),
                        ]) {
                            echo "Updating JMeter with datadog for monitor."
                            jmeterscript = readFile "${env.TEST_PLAN}"
                            // Replace placeholders in JMeter script with DataDog API Key
                            jmeterscript = jmeterscript.replace('DATADOG-API-KEY', "${DataDog}")
                            // Write back the modified script to the TEST_PLAN file
                            writeFile file: "${env.TEST_PLAN}", text: jmeterscript
                        }
                    }
                    else{
                        error "JMeter script not created. Postman to JMeter script conversion failed."
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

        stage('Smart Analysis (lab45)') {
            when {
                expression { env.LIGHTHOUSE_RUN == 'true' }
            }
            steps {
                sh """
                python Python/lab45_ai.py
                """
            }
        }
    }

    post {
        always {
            script {
                def projectName = env.JOB_NAME
                def buildNumber = env.BUILD_NUMBER
                def timestamp = new Date().format("yyyy-MM-dd HH:mm:ss")
                def buildResult = currentBuild.result ?: 'SUCCESS'
                def user = env.BUILD_USER_ID ?: 'Unknown User' // User who triggered the build
                
                echo "Current Build Status: ${buildResult}."

                // Determine the comment body based on build result
                def commentBody
                switch (buildResult) {
                    case 'SUCCESS':
                        commentBody = "Pipeline passed successfully."
                        break
                    case 'FAILURE':
                        commentBody = "Pipeline failed."
                        break
                    case 'ABORTED':
                        commentBody = "Pipeline was aborted."
                        break
                    default:
                        commentBody = "Pipeline status is unknown."
                }

                // Construct the Jira comment with detailed context
                def pipelineDetails = "Pipeline: ${projectName}, Build Number: ${buildNumber}, Triggered by: ${user}, Timestamp: ${timestamp} - ${env.BUILD_URL}"
                def jiraCommentText = "${commentBody} ${pipelineDetails}"

                // Add comment to Jira issue
                jiraComment site: env.JIRA_SITE, issueKey: env.ISSUE_KEY, body: jiraCommentText
                echo "Comment added to Jira issue ${env.ISSUE_KEY} with content: ${jiraCommentText}"

                // Send the Slack message with the build.log attached
                slackSend channel: env.SLACK_CHANNEL, message: "${commentBody} - ${pipelineDetails}"

                // Prepare email content based on build result
                def emailBodyContent
                def emailSubject = "${env.EMAIL_SUBJECT} - Build ${buildResult} for build number ${buildNumber}"

                if (buildResult == 'SUCCESS') {
                    sh "python ./Python/json_html_conv.py ${env.REPORT_DIR}/html-report"
                    sh "mv ./Templates/datadog_report.html datadog_report.html"
                    emailBodyContent = readFile 'Templates/success.html'
                } else {
                    emailBodyContent = readFile 'Templates/failure.html'
                }

                // Replace placeholders in email body
                emailBodyContent = emailBodyContent
                    .replace('${PROJECT_NAME}', projectName)
                    .replace('${BUILD_NUMBER}', buildNumber)
                    .replace('${TIMESTAMP}', timestamp)

                // Write email body to a temporary file
                def emailBodyFile = 'emailBodyContent.html'
                writeFile file: emailBodyFile, text: emailBodyContent
                
                // Stop Sustainability Monitor
                sh "python Python/sustainability.py stop"

                // Send email notification
                emailext(
                    to: env.EMAIL_RECIPIENTS,
                    from: env.EMAIL_SENDER,
                    subject: emailSubject,
                    body: readFile(emailBodyFile),
                    replyTo: env.EMAIL_REPLY_TO,
                    attachLog: true,
                    attachmentsPattern: "${env.ATTACHMENTS}"
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

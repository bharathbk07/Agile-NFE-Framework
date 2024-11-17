# Agile-NFE Framework - Jenkins Pipeline Documentation
## Introduction
The **Agile-NFE Framework** is a comprehensive Continuous Integration and Continuous Deployment (CI/CD) pipeline designed to automate the deployment of applications while ensuring they meet Non-Functional Engineering (NFE) standards. This framework integrates key engineering practices such as **performance testing**, **static code analysis**, **chaos engineering**, **frontend testing with Lighthouse**, **accessibility testing**, **AI-based result analysis**, and **sustainability monitoring** to ensure that the application is not only functional but also **reliable**, **resilient**, **performant**, and **accessible under real-world conditions**.

The framework adopts a **Shift-Left approach** by incorporating **performance**, **static code**, and **accessibility** checks early in the development process, minimizing risks and costs associated with defect detection. Additionally, it introduces a **Shift-Right** element through **chaos engineering** and **AI-based analysis**, validating the application’s **resilience, performance**, and **sustainability** in production-like environments, which helps ensure that the application can handle unexpected failures, maintain stability, and adapt based on real-time data insights.

With seamless integrations for **Slack Notifications**, **Email Updates**, and **Jira Story Updates**, the Agile-NFE Framework ensures stakeholders are always informed of the latest build status, performance scan results, and application health. Slack **Notifications** keep teams up to date by sending messages to the designated Slack channels when builds, performance scans, and sustainability checks are completed. Email notifications are sent to configured recipients with the build results, performance metrics, and analysis reports. Additionally, the framework automatically updates the linked Jira story with the build status and performance testing results, ensuring full traceability and visibility across the team.

By automating these critical processes, the Agile-NFE Framework promotes the development of high-quality, production-ready software that adheres to performance, security, sustainability, and accessibility standards, while fostering rapid, continuous delivery in a collaborative and efficient Agile environment.

## Diagram
Refer to the workflow diagram for a visual representation of the pipeline.

![Franewrok flow Diagram](Screenshot/Agile-NFE.png)

## Prerequisites

## Jenkins Setup
Ensure Jenkins is installed and running with the agent configured on the system.

## Tools Required

1. **Datadog**
2. **SonarQube**
3. **Slack**
4. **Jira**
5. **Pa11y**
6. **Gremlin**
7. **JMeter**
8. **Lighthouse**
9. **Docker**

## Jenkins Plugins
The following plugins must be installed and configured in Jenkins:

1. **Slack Notifications Plugin**
2. **NodeJS Plugin**
3. **Datadog Plugin**
4. **Maven Integration Plugin**
5. **Sonar Scanner Plugin**
6. **Sonar Quality Gate Plugin**
7. **Email Extension Plugin**
8. **Jira Integration Plugin**

> **Note**: Be sure to install all the suggested plugins shown by Jenkins in the Manage Plugins section.

Refer to each plugin’s documentation for detailed configuration instructions.By ensuring these plugins are properly configured, Jenkins can automate builds, perform quality checks, and provide comprehensive notifications and monitoring.


## Shift-Left or Shift-Right Approach?
This pipeline follows a **shift-left approach** by integrating testing (performance and static code analysis) early in the CI/CD process. Shift-left practices help catch issues earlier in the development cycle, minimizing risks and reducing the cost of fixing defects. Additionally, chaos engineering introduces a **shift-right component** by validating the resilience of the application in production-like scenarios, ensuring that the system behaves reliably under real-world conditions.


## Jenkins Pipeline Workflow Steps

## Overview

The pipeline is designed to:
- Monitor sustainability using `psutil`
- Clone the repository
- Perform static code analysis using SonarQube
- Validate and deploy the application using Docker
- Run health checks and validate APIs
- Conduct front-end testing using Lighthouse
- Run accessibility testing with Pa11y
- Generate Postman-to-JMeter scripts for performance testing
- Execute performance testing using JMeter
- Conduct chaos testing with Gremlin
- Analyze the results using AI models from `lab45`


## 1. **Load Job Configuration**
   - **Action**: Read configuration from `configfile.yml`.
   - **Tools**: Jenkins, YAML plugin.
   - **Outputs**: Environment variables for various tests (Postman, JMeter, Lighthouse, Chaos).

## 2. **Clone Repository**
   - **Action**: Clone the GitHub repository and switch to the specified branch.
   - **Tools**: Git.

## 3. **Static Code Analysis (SonarQube)**
   - **Action**: Perform static code analysis using SonarQube.
   - **Tools**: Maven, SonarQube.

## 4. **Validate and Deploy (Docker)**
   - **Action**: Validate Docker setup, build, and deploy the application using Docker Compose.
   - **Tools**: Docker.

## 5. **Health Check and API Validation**
   - **Action**: Verify container statuses and perform a basic health check of the API.
   - **Tools**: Docker, curl.

## 6. **Front-End Testing (Lighthouse) (Conditional)**
   - **Action**: Run Lighthouse for front-end performance testing if enabled.
   - **Tools**: Lighthouse.

## 7. **Accessibility Testing (Pa11y) (Conditional)**
   - **Action**: Perform accessibility testing using Pa11y if enabled.
   - **Tools**: Pa11y.

## 8. **PT Script Creation (Postman) (Conditional)**
   - **Action**: Convert Postman collections to JMeter scripts for performance testing if enabled.
   - **Tools**: Postman2JMX, JMeter.

## 9. **Performance Testing (JMeter) (Conditional)**
   - **Action**: Run performance tests with JMeter if enabled.
   - **Tools**: JMeter.

## 10. **Chaos Testing (Gremlin) (Conditional)**
   - **Action**: Initiate a chaos experiment using Gremlin if enabled.
   - **Tools**: Gremlin API.

## 11. **Analyze the Results Using AI Models (lab45)**
   - **Action**: Leverage AI models from `lab45` to analyze the results from performance, chaos, and accessibility tests.
   - **Tools**: lab45 AI models.

## 12. **Monitor Sustainability Using `python psutil`**
   - **Action**: Use `python psutil` to monitor system sustainability during the tests and deployments, including CPU, memory, and disk usage.
   - **Tools**: `python psutil`.

---

## Post-Execution Steps

### 1. **Comment on Jira**
   - **Action**: Add a comment to the linked Jira issue with the build result and pipeline details.
   - **Tools**: Jira plugin.

### 2. **Send Slack Notifications**
   - **Action**: Send pipeline status and logs to the configured Slack channel.
   - **Tools**: Slack plugin.

### 3. **Send Email Notifications**
   - **Action**: Notify recipients with build status, logs, and reports attached.
   - **Tools**: Email plugin (configured with SMTP).

---

## Conditional Paths

- **Lighthouse & Pa11y**: Execute only if respective tests are enabled in the configuration file.
- **JMeter & Gremlin**: Execute based on configuration and environment setup.

---

## Tools Used

- **Git**: For cloning the repository.
- **SonarQube**: For static code analysis.
- **Docker**: For containerization and deployment.
- **Lighthouse**: For front-end performance testing.
- **Pa11y**: For accessibility testing.
- **Postman2JMX**: For converting Postman collections to JMeter scripts.
- **JMeter**: For performance testing.
- **Gremlin**: For chaos testing.
- **Jira Plugin**: For adding comments to Jira issues.
- **Slack Plugin**: For sending notifications.
- **Email Plugin**: For sending build status emails.
- **lab45 AI models**: For analyzing results.
- **python psutil**: For system sustainability monitoring.

## Pros of the Agile-NFE Framework

### 1. Early Detection of Issues (Shift-Left Approach)
The framework integrates performance testing, static code analysis, and other quality checks early in the development process, enabling faster detection of issues. This minimizes the cost and risk of defects surfacing later in the development cycle, which is key to achieving high-quality software.

### 2. Continuous Monitoring and Quality Control
By including SonarQube for static code analysis, the framework ensures that every code commit is scrutinized for quality issues, improving code maintainability and preventing technical debt. The use of JMeter for performance testing further ensures that any performance bottlenecks are identified and resolved promptly.

### 3. Enhanced System Resilience (Shift-Right Approach)
The chaos engineering component of the framework introduces resilience testing, validating the application’s ability to handle unexpected failures and operate reliably under production-like conditions. This proactive approach helps ensure high availability and fault tolerance in real-world usage.

### 4. Automated Frontend Performance Testing with Lighthouse
The integration of Lighthouse into the pipeline automates frontend performance testing, enabling teams to monitor critical frontend metrics such as page load time, SEO, accessibility, and best practices continuously. This ensures that user experience is prioritized and optimized throughout the development process.

### 5. Comprehensive Accessibility Testing
By including Pa11y for automated accessibility testing, the framework ensures that the application is compliant with accessibility standards (such as WCAG), improving inclusivity and ensuring the application is usable by a broader audience.

### 6. Seamless Integration with Notifications and Issue Tracking
The framework includes automatic Slack Notifications and Email Notifications, providing timely updates to team members about build and performance scan results. Jira Updates ensure that the associated Jira story is updated with the latest status, performance metrics, and results, keeping everyone aligned on progress.

### 7. End-to-End Automation
The framework automates critical tasks such as build verification, testing, deployment readiness, and stakeholder notification, reducing manual intervention and enabling faster release cycles. This automation boosts productivity and ensures that the application is always production-ready.

### 8. Improved Collaboration Across Teams
The integration with Jira, Slack, and Email enhances communication across different teams (e.g., developers, testers, and project managers), ensuring that everyone has up-to-date information on the status of the build and testing phases. This promotes collaboration and faster decision-making.

### 9. Scalability and Flexibility
With the ability to scale performance and chaos testing based on configurable parameters, the framework adapts to various project needs, whether for small applications or large-scale, distributed systems. The framework's flexibility ensures it can grow with the project.

### 10. Complete Feedback Loop
The combination of static analysis, performance testing, chaos experiments, and frontend testing establishes a complete feedback loop from development through production, ensuring that the software is continuously validated for quality, performance, and resilience.

### 11. Efficient and Cost-Effective
By shifting testing and quality checks earlier in the development lifecycle, the framework helps reduce the costs associated with late-stage defect detection and remediation. This proactive testing and monitoring approach saves time and effort in the long run.

### 12. Comprehensive Reporting
Detailed reports generated from performance scans, code quality analysis, and accessibility tests ensure that stakeholders have access to clear, actionable insights about the application’s quality, performance, and compliance, helping in data-driven decision-making.

### 13. Consistent Build and Deployment Process
The pipeline ensures that builds are tested consistently, deployed in a controlled manner, and updated with relevant notifications, making the deployment process predictable and reliable, with minimal risk of issues arising during deployment.

## How to Use
1. Update `configfile.yml` with relevant configurations.
2. Ensure all prerequisites are fulfilled.
3. Run the pipeline from Jenkins and monitor the logs for each stage.

## Troubleshooting
- If Docker is not running, start it and retry.
- For SonarQube login failures, ensure the correct token is used.
- Verify Gremlin credentials if the chaos experiment fails to initiate.

## Reference

 - [DataDog](https://app.datadoghq.com/)
 - [Installing SonarQube in Docker](https://medium.com/@HoussemDellai/setup-sonarqube-in-a-docker-container-3c3908b624df)
 - [Installing Jenkins in Docker](https://octopus.com/blog/jenkins-docker-install-guide)
 - [Gremlin Trial Account](https://www.gremlin.com/trial)
 - [How to Install and Use Gremlin with Docker](https://www.gremlin.com/community/tutorials/how-to-install-and-use-gremlin-with-docker-on-ubuntu-16-04)
 - [How to Send Slack Notifications From Jenkins](https://youtu.be/EDVZli8GdUM?si=dM5tRvyvZk9Dviko)
 - [How to Integrate Jira With Jenkins](https://youtu.be/-KrlCWVPfJM?si=-SXdIDdTYdNnK3ms)
 - [How to setup Pa11y and its Dashboard](https://pa11y.org/)

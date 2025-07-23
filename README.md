# GitHub Actions CI/CD Wrapper Workflows

Welcome! This repository provides **wrapper workflows** that trigger standardized CI and CD reusable workflows hosted in [cicd-templates](https://github.com/AmanjotSinghSaini/cicd-templates). These wrappers make it easy for your teams to implement secure, consistent CI/CD pipelines with minimal setup.

---

## What’s Inside

- `ci-wrapper.yml` — triggers Docker Build + Security Scans (CI)
  - Gitleaks secrets scanning
  - Trivy vulnerability scanning
  - OWASP Dependency Check
  - SonarQube analysis
  - Pytest
  - Image Size Validator
  - ECR push
  - Slack alerts
  - Artifact uploads

- `cd-wrapper.yml` — triggers deployment to EKS using kubectl (CD)
  - Pulls latest ECR image
  - Applies manifests to EKS (supports multiple modes)
  - Validates rollout with retry logic
  - Prunes old & untagged images 

---

## Prerequisites

Before using the CI/CD workflows, ensure the following setup is complete.

---

### GitHub Secrets Configuration

1. Go to your repository (e.g., `https://github.com/your-org/your-repo`)
2. Click on the **"Settings"** tab at the top
3. In the left sidebar, go to **"Secrets and variables" → "Actions"**
4. Click the **"New repository secret"** button
5. Enter the **secret name** (e.g., `AWS_ACCESS_KEY_ID`)
6. Enter the **secret value** (your actual AWS access key, token, etc.)
7. Click **"Add secret"**
8. Repeat steps 4–7 for each secret required by the pipeline

> See [Secrets Table](#required-github-secrets) for a full list.

---

### Repository Requirements

Make sure your repository includes the following:

- A `Dockerfile` in the root or specified path
- Kubernetes manifest files:
  - For single-file mode: `deployment.template.yaml`
  - For multi-file mode: `deployment.yaml`, `service.yaml`, `ingress.yaml` inside a `k8s/` folder
- Dependency files for your tech stack:
  - Python: `requirements.txt`
  - Node.js: `package.json`
  - Java: `pom.xml`, `build.gradle`, etc.
- (Optional) A SonarQube project already created if `run_sonar` is enabled  
  🔗 [Create a SonarQube project](https://docs.sonarsource.com/sonarqube/latest/project-administration/adding-a-project/)
- (Optional) Slack channel created and Slack webhook URL generated (if `slack-enabled` is true)  
  🔗 [Set up a Slack webhook](https://api.slack.com/messaging/webhooks)

---

### Permissions & Access

- GitHub Actions must be **enabled** for the repository  
  🔗 [GitHub Actions documentation](https://docs.github.com/en/actions/using-workflows/about-workflows)
- User running the workflow must have **write access** to the repo
- AWS IAM user/role used must have:
  - ECR access permissions:  
    🔗 [Set up permissions for Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/ecr_managed_policies.html)
  - EKS cluster access:  
    🔗 [Configure access to EKS using IAM](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html)
- (Optional) Slack webhook must be allowed to post to the selected channel
- (Optional) SonarQube token must have permission to execute analysis on the selected project

---

### Recommendations (Optional but Useful)

- Enable branch protection rules to enforce successful CI before merging  
  🔗 [Protect branches in GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)

---

# Inputs

## CI Wrapper Inputs

| Input Name                  | Required | Type     | Default         | Description                                                                 |
|-----------------------------|----------|----------|-----------------|-----------------------------------------------------------------------------|
| `image_name`                  | Yes      | string   | -               | Full image name (e.g., `ghcr.io/my-org/my-app`)                            |
| `image_tag`                   | Yes      | string   | -               | Tag for the built image (e.g., `latest`, `v1.0.0`)                          |
| `dockerfile_path`             | No       | string   | ./Dockerfile    | Path to the Dockerfile                                                     |
| `context`                     | No       | string   | .               | Docker build context directory                                              |
| `build_args`                  | No       | string   | --no-cache      | Extra arguments to pass to Docker build                                    |
| `run_gitleaks`                | No       | boolean  | true            | Enable Gitleaks scan                                                       |
| `gitleaks_fetch_depth`        | No       | number   | 1               | Git fetch depth for Gitleaks (**0 = all commits**, **1 = most recent**)   |
| `continue_on_gitleaks_error` | No       | boolean  | false           | Whether to continue pipeline if Gitleaks scan fails                        |
| `run_owasp`                   | No       | boolean  | true            | Enable OWASP dependency check                                              |
| `continue_on_owasp_error`     | No       | boolean  | false           | Whether to continue pipeline if OWASP scan fails                           |
| `run_pytest`                  | No       | boolean  | true            | Run tests using Pytest                                                     |
| `continue_on_pytest_error`    | No       | boolean  | true            | Whether to continue pipeline if tests fail                                 |
| `run_trivy`                   | No       | boolean  | true            | Enable Trivy scan for vulnerabilities                                      |
| `continue_on_trivy_error`     | No       | boolean  | false           | Whether to continue pipeline if Trivy scan fails                           |
| `image_size_threshold_mb`     | No       | number   | 200             | Maximum allowed image size in MB                                           |
| `continue_on_size_check_error`| No       | boolean  | false           | Whether to continue pipeline if image exceeds size                         |
| `push_to_ecr`                 | No       | boolean  | true            | Whether to push the image to AWS ECR                                       |
| `ecr_repository`              | Yes*     | string   | -               | ECR repository name (required if `push_to_ecr` is true)                    |
| `run_sonar`                   | No       | boolean  | true            | Whether to run SonarQube static analysis                                   |
| `sonar_host_url`              | Yes*     | string   | -               | SonarQube server URL (required if `run_sonar` is true)                     |
| `sonar_project_key`           | Yes*     | string   | -               | SonarQube project key                                                      |
| `sonar_project_name`          | Yes*     | string   | -               | SonarQube project name                                                     |
| `slack_enabled`               | No       | boolean  | true            | Whether to send Slack notifications                                        |
| `slack_channel`               | No       | string   | "#github-actions-notification" | Slack channel to send notifications to                           |

## CD Wrapper Inputs

| Input Name                  | Required | Type     | Default                         | Description                                                                 |
|-----------------------------|----------|----------|----------------------------------|-----------------------------------------------------------------------------|
| `ecr_repo`                    | Yes      | string   | -                                | Full ECR image URL to deploy (e.g., `account.dkr.ecr.region.amazonaws.com/repo-name`) |
| `eks_cluster_name`            | Yes      | string   | -                                | Name of the EKS cluster to connect and deploy into                         |
| `deployment_mode`             | No       | string   | "singlefile"                     | Deployment mode: `singlefile`, `filenames`, or `recursive`                 |
| `deployment_file`             | No*      | string   | ./deployment.template.yaml       | Path to single manifest file (used if `deployment_mode` is `singlefile`)   |
| `deployment_files`            | No*      | string   | -                                | Comma-separated list of files (used if `deployment_mode` is `filenames`)   |
| `continue_on_validation_error`| No       | boolean  | false                            | Whether to continue if post-deploy validation fails                         |
| `delete_old_images`           | No       | boolean  | true                             | Whether to delete older unused ECR images after deployment                 |

> *Only one of `deployment_file` or `deployment_files` is required, depending on the deployment mode.

## Required GitHub Secrets

| Secret Name           | Required | Description                                                       |
|------------------------|----------|-------------------------------------------------------------------|
| SLACK_WEBHOOK_URL      | No       | Slack webhook URL used for sending pipeline notifications         |
| AWS_ACCESS_KEY_ID      | Yes      | AWS access key for authenticating with ECR and EKS                |
| AWS_SECRET_ACCESS_KEY  | Yes      | AWS secret key for ECR and EKS authentication                     |
| AWS_REGION             | Yes      | AWS region (e.g., `ap-south-1`) where your resources are hosted    |
| AWS_ACCOUNT_ID         | Yes      | AWS account ID used in constructing ECR repository URLs           |
| SONAR_TOKEN            | No       | Token used to authenticate with SonarQube for static code analysis|

> **Note:**  
> `SLACK_WEBHOOK_URL` and `SONAR_TOKEN` are optional. They are only required if:
> - `slack_enabled: true` is set in your workflow inputs (for Slack notifications), or  
> - `run_sonar: true` is enabled (for SonarQube static analysis).  
> If these secrets are not provided while the respective features are enabled, the pipeline may fail at runtime.


---

## How to Use

To use the CI/CD pipeline with the provided **wrapper workflows**, follow these steps:

---

### Folder Structure Requirement

Ensure your repository contains the following structure:

```
your-repo/
├── .github/
│   └── workflows/
│       ├── ci-wrapper.yml
│       └── cd-wrapper.yml
```

- Create a `.github/workflows/` folder at the **root of your repository** if it doesn't already exist.
- Place both the CI and CD wrapper workflow files (`ci-wrapper.yml` and `cd-wrapper.yml`) inside this folder.

---

### How the Pipeline Triggers

The pipeline can be triggered in **three ways**:

#### 1. **On Push**

```yaml
on:
  push:
    branches:
      - main
```

- Every time you push code to the `main` branch, the pipeline will automatically trigger.
- branch name can be changed according to the usage
- No manual action is needed.

---

#### 2. **Manual Trigger via Workflow Dispatch**

```yaml
on:
  workflow_dispatch:
```

To run manually:

1. Go to the **Actions** tab on your GitHub repository.
2. Click on the desired workflow (`ci-wrapper` or `cd-wrapper`).
3. Click **"Run workflow"**.
4. Click **Run** to start the workflow manually.

---

#### 3. **Scheduled Run (Cron Job)**

```yaml
on:
  schedule:
    - cron: '20 8 * * *'  # Runs every day at 08:20 AM UTC
```

- The workflow will automatically run at the defined time.
- No user action is needed after setup.

---

### Monitoring the Pipeline

After triggering the workflow:

1. Open the **Actions** tab in your GitHub repository.
2. Click on the workflow run (CI or CD) you want to inspect.
3. Click on any job or step to expand and **view logs** in real time or post-run.

---

### Viewing Artifacts

If the workflow generates artifacts (e.g., scan reports, test results, deployment files):

1. Open the **Actions** tab.
2. Select the completed run.
3. Scroll to the bottom to the **Artifacts** section.
4. Click the artifact name to **download** it.

---

> **Make sure all required `secrets` and `inputs` are configured correctly in your repository settings for the pipeline to work successfully.**

---

## CI Pipeline

<img width="1431" height="563" alt="Image" src="https://github.com/user-attachments/assets/e73b2a6c-2148-400a-9b0d-6f43f69aa90e" />

## Artifacts

<img width="1430" height="513" alt="Image" src="https://github.com/user-attachments/assets/74ed35b0-e211-4b9b-bc36-6ab5b39760f1" />

## CD Pipeline

<img width="1449" height="434" alt="Image" src="https://github.com/user-attachments/assets/dc8431d6-3557-406b-9c56-93396f86710b" />

## Slack Notifications

<img width="1373" height="834" alt="Image" src="https://github.com/user-attachments/assets/2fde2c48-dd0e-4e56-8613-9e0c91ff795b" />

## Final Deployment

<img width="1915" height="969" alt="Image" src="https://github.com/user-attachments/assets/d7bbba83-0e1e-4880-8005-4d67812d2908" />

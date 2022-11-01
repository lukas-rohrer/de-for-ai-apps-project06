# Data Engineer for AI Applications: Project 5 - Cloud Native Project

TechTrends is an online website used as a news sharing platform, that enables consumers to access the latest news within the cloud-native ecosystem. In addition to accessing the available articles, readers are able to create new media articles and share them with the wider community.

The task was to package and deploy the application to a Kubernetes platform. Docker was used to package the application, and an automated Continuous Integration process with GitHub Actions was implemented. For the release process, Kubernetes declarative manifests were used, which were templated using Helm. To automate the Continuous Delivery process, ArgoCD was used.

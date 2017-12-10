#!/usr/bin/env groovy

podTemplate(label: 'default',
containers: [
    containerTemplate(name: 'docker', image: 'docker', command: 'cat', args: '', ttyEnabled: true, resourceRequestCpu: '25m'),
    containerTemplate(name: 'helm', image: 'lachlanevenson/k8s-helm', command: 'cat', args: '', ttyEnabled: true, resourceRequestCpu: '25m'),
],
volumes: [
    hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock'),
    secretVolume(secretName: 'jenkins-gcr-keys', mountPath: '/repo_keys'),
],
nodeSelector: 'jenk=true') {
    node('default') {
        def currentCommitHash = ""
        def pwd = pwd()
        def helmChartPath = "helm/demo-app"
        def helmReleaseName = "demo-app-jenk"

        stage('checkout') {
            scm_vars = checkout scm
            println "checkout successful"
            currentCommitHash = "${scm_vars.GIT_COMMIT}"
        }

        def gcloud_project = "sharktopus-148619"
        def containerName = "test_app"
        def releaseVersion = "${currentCommitHash}.${env.BUILD_NUMBER}"
        def releaseTag = "${containerName}:${releaseVersion}"
        def dockerRepo = "gcr.io/${gcloud_project}/"
        def repoTag = "${dockerRepo}${releaseTag}"

        def gcr_cred = readFile('/repo_keys/deploy.json')

        stage('build') {
            container('docker') {
                sh("cd app && docker build -f good.Dockerfile -t ${releaseTag} .")
            }
        }

        stage('test') {
            container('docker') {
                // test command goes here
                sh("docker run ${releaseTag} echo 'OK'")
            }
        }

        stage('deploy') {
            container('docker') {
                sh("docker tag ${releaseTag} ${repoTag}")
                sh("docker login -u _json_key -p '${gcr_cred}' https://gcr.io")
                sh("docker push ${repoTag}")
            }

            container('helm') {
                sh("helm upgrade --install --set image.repository=${dockerRepo}${containerName},image.tag=${releaseVersion} ${helmReleaseName} ${helmChartPath}")
            }
        }

    }
}

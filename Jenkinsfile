#!/usr/bin/env groovy

podTemplate(label: 'default',
containers: [
    containerTemplate(name: 'docker', image: 'docker', command: 'cat', ttyEnabled: true, resourceRequestCpu: '25m'),
    containerTemplate(name: 'helm', image: 'lachlanevenson/k8s-helm', command: 'cat', ttyEnabled: true, resourceRequestCpu: '25m'),
],
volumes: [hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')]
) {
    node('default') {
        def currentCommitHash = "${env.GIT_COMMIT}"
        def gcloud_project = "sharktopus-148619"
        def releaseTag = "test_app:${currentCommitHash}.${env.BUILD_NUMBER}"
        def dockerRepo = "gcr.io/${gcloud_project}/"
        def repoTag = "${dockerRepo}${releaseTag}"

        stage('checkout') {
            checkout scm
            println "checkout successful"
        }

        stage('build') {
            container('docker') {
                sh("cd app && docker build -f good.Dockerfile -t ${releaseTag} .")
            }
        }

        stage('test') {

        }

        stage('deploy') {
            container('docker') {
                sh("docker tag ${releaseTag} ${repoTag}")
                sh("docker push ${repoTag}")
            }

            container('helm') {
                sh("helm list")
            }
        }

    }
}

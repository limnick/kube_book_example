#!/usr/bin/env groovy

podTemplate(label: 'default',
containers: [
    containerTemplate(name: 'docker', image: 'docker', command: 'cat', ttyEnabled: true, resourceRequestCpu: '25m'),
    containerTemplate(name: 'helm', image: 'lachlanevenson/k8s-helm', command: 'cat', ttyEnabled: true, resourceRequestCpu: '25m'),
],
volumes: [hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')]
) {
    node('default') {

        stage('checkout') {
            checkout scm
            println "checkout successful"
        }

        stage('build') {
            container('docker') {
                sh("cd app && ./build.sh good")
            }
        }

        stage('test') {}

        stage('deploy') {
            container('helm') {
                sh("helm list")
            }
        }

    }
}

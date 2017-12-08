#!/usr/bin/env groovy

podTemplate(label: 'default',
containers: [
    containerTemplate(name: 'helm', image: 'lachlanevenson/k8s-helm', command: 'cat', ttyEnabled: true, resourceRequestCpu: '25m'),
]) {
    node('default') {

        stage('checkout') {
            checkout scm
            println "checkout successful"
        }

        stage('test') {}

        stage('deploy') {
            container('helm') {
                sh("helm list")
            }
        }

    }
}

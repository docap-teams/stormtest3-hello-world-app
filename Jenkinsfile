// Replace all occurences of with your actual quay.io account.
// Tip: use Replace, you find this in the menu under Edit -> Replace. 
// Replace stormtest3 with the prefix you used for creating your hello-world-app repository.

pipeline {
  agent none

  //check every minute for changes
  triggers {
    pollSCM('*/1 * * * *')
  }

  stages {
  //Build goes here
    stage('Build') {
      agent {
        kubernetes {
          defaultContainer 'kaniko'
          yaml """
kind: Pod
metadata:
  name: kaniko
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    imagePullPolicy: Always
    command:
    - /busybox/cat
    tty: true
    volumeMounts:
      - name: docker-config
        mountPath: /kaniko/.docker
    securityContext:
        runAsUser: 0
  volumes:
  - name: docker-config
    projected:
      sources:
      - secret:
          name: smidigstorm-docap-pull-secret
          items:
            - key: .dockerconfigjson
              path: config.json
"""
        }
      }

      steps {
        script {
          //write the version number to a file which gets copied into the container
          sh 'echo $BUILD_ID > VERSION.txt'
          sh "/kaniko/executor --dockerfile `pwd`/Dockerfile --context `pwd` --destination=quay.io/smidigstorm/hello-world-app:${env.BUILD_ID}"
        } //container
      } //steps
    } //stage(build)

/*
    //Test goes here
    stage('Test') {
      parallel {

        stage('Static Analysis') {
          //Run this code within our container for this build
          agent {
            kubernetes {
              defaultContainer 'appy'
              yaml """
kind: Pod
metadata:
  name: appy
spec:
  containers:
  - name: appy
    image: quay.io/smidigstorm/hello-world-app:${env.BUILD_ID}
    imagePullPolicy: IfNotPresent
    command:
    - cat
    tty: true
"""
        }
      }

      //Run pylint on app.py
      steps {
        sh 'pylint app.py'
      }
    } //stage(static analysis)

    //Functional testing goes here
    stage('Functional Tests') {
      //Run this code within our container for this build
      agent {
        kubernetes {
          defaultContainer 'appy'
            yaml """
kind: Pod
metadata:
  name: appy
spec:
  containers:
  - name: appy
    image: quay.io/smidigstorm/hello-world-app:${env.BUILD_ID}
    imagePullPolicy: IfNotPresent
    command:
    - cat
    tty: true
"""
        }
      }

      steps {
        sh 'py.test --disable-pytest-warnings --junitxml xunit-result-functional.xml --cov=. --cov-config .coveragerc --cov-append functionaltest.py'
      }

      //Tell Jenkins about the test report
      post {
        always {
          junit 'xunit-result-*.xml'

          // make files available for later stages in build pipeline
          stash includes: 'xunit-result-*.xml', name: 'functional-test-results'
          stash includes: '.coverage', name: 'cobertura-data'
        }
      }
    } //stage(functional tests)

    //BDD testing goes here
    stage('BDD Tests') {
      agent {
        kubernetes {
          defaultContainer 'appy'
          yaml """
kind: Pod
metadata:
  name: appy
spec:
  containers:
  - name: appy
    image: quay.io/smidigstorm/hello-world-app:${env.BUILD_ID}
    imagePullPolicy: IfNotPresent
    command:
    - cat
    tty: true
"""
        }
      }

      steps {
        sh 'coverage run --source=. --omit=conf.py -a -m behave --junit --junit-directory .'
      }

      post {
        always {
          stash includes: '.coverage', name: 'cobertura-data-bdd'
          stash includes: 'TESTS-*.xml', name: 'bdd-test-results'
          junit 'TESTS-*.xml'
        }
      }
    } //stage(BDD Tests)

  } //parallel
} //stage(test)

*/

/*
    //Coverage goes here
    stage('Coverage') {
      agent {
        kubernetes {
          defaultContainer 'appy'
          yaml """
kind: Pod
metadata:
  name: appy
spec:
  containers:
  - name: appy
    image: quay.io/smidigstorm/hello-world-app:${env.BUILD_ID}
    imagePullPolicy: IfNotPresent
    command:
    - cat
    tty: true
"""
        }
      }

      steps {
        dir('./coverage-func') {
          unstash 'cobertura-data'
        }

        dir('./coverage-bdd') {
          unstash 'cobertura-data-bdd'
        }

        // combine the coverage datafiles
        sh 'coverage combine coverage-func/.coverage coverage-bdd/.coverage'

        // generate the coverage report, publish to jenkins and store for use in sonarqube stage
        sh 'coverage xml -i -o coverage/coverage.xml'
        cobertura coberturaReportFile: 'coverage/coverage.xml'
        stash includes: 'coverage/coverage.xml', name: 'cobertura-report'
      }
    }
*/

/*
    //SonarQube goes here
    stage('Sonarqube') {
      agent {
        kubernetes {
          defaultContainer 'sonar'
          yaml """
kind: Pod
metadata:
  name: sonar
spec:
  containers:
  - name: sonar
    image: jenkins/jnlp-slave:latest-jdk11
    imagePullPolicy: IfNotPresent
    command:
    - cat
    tty: true
"""
        }
      }

      environment {
        scannerHome = tool 'my-sonar-scanner'
      }

      steps {
        //unstash will go here
        unstash 'cobertura-report'
        unstash 'functional-test-results'
        unstash 'bdd-test-results'
        // unstash 'cobertura-data'

        withSonarQubeEnv('sonarqube-server') {
          sh "${scannerHome}/bin/sonar-scanner"
        }

        timeout(time: 2, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }
*/

/*
    //Documentation generation goes here
    stage('Documentation') {
      agent {
        kubernetes {
          defaultContainer 'appy'
          yaml """
kind: Pod
metadata:
  name: appy
spec:
  containers:
  - name: appy
    image: quay.io/smidigstorm/hello-world-app:${env.BUILD_ID}
    imagePullPolicy: IfNotPresent
    command:
    - cat
    tty: true
"""
        }
      }

      steps {
        //generate documentation in html format and put in a directory called output
        sh 'sphinx-build -b html . output'

        //tell jenkins we made an HTML report and to publish it
        publishHTML target: [
          allowMissing: false,
          alwaysLinkToLastBuild: false,
          keepAll: true,
          reportDir: 'output',
          reportFiles: 'index.html',
          reportName: 'Sphinx'
        ]
      }
    }
*/

/*
    //Deploy goes here
    stage('Deploy to Production') {

      environment {
        //put your credential identifier below in single quotes ''
        GIT_CREDS = credentials('github')
      }

      agent {
        kubernetes {
          defaultContainer 'argo-cd-ci-builder'
          yaml """
kind: Pod
metadata:
  name: argo-cd-ci-builder
spec:
  containers:
  - name: argo-cd-ci-builder
    image: argoproj/argo-cd-ci-builder:v1.0.0
    imagePullPolicy: IfNotPresent
    command:
    - cat
    tty: true
"""          
        }
      }

      steps {
        //input message:'Approve deployment?'
        container('argo-cd-ci-builder') {

          //get the GitOps repository - you're going to need to change [teams] to your team name.          
          // GIT_CREDS_PSW is the app token. 
          sh "git clone https://$GIT_CREDS_PSW@github.com/docap-teams/[team]-hello-world-deployment.git"
          sh "git config --global user.email 'ci@ci.com'"
          
          dir("hello-world-deployment") {
            //update the image to be the current build number from Jenkins
            sh "cd prod && kustomize edit set image quay.io/smidigstorm/hello-world-app:${env.BUILD_ID}"
            //and save it (or print "no changes")
            sh "git commit -am 'Publish new version' && git push || echo 'no changes'"
          }
        }
      }
    }
*/

  } //stages
} //pipeline


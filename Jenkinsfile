// DevSecOps declarative pipeline: same shift-left scanning as the GitLab pipeline.
pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  environment {
    IMAGE = "secure-sdlc-sample:${env.BUILD_NUMBER}"
  }

  stages {
    stage('Build') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install -r app/requirements.txt
          python -m compileall app
        '''
      }
    }

    stage('Secret scan (Gitleaks)') {
      steps {
        sh 'docker run --rm -v $PWD:/repo zricethezav/gitleaks:latest detect --source /repo --report-path /repo/gitleaks.sarif --report-format sarif --redact'
      }
    }

    stage('SAST (Semgrep)') {
      steps {
        sh 'docker run --rm -v $PWD:/src returntocorp/semgrep:latest semgrep --config auto --sarif --output /src/semgrep.sarif /src/app'
      }
    }

    stage('SCA (Trivy filesystem)') {
      steps {
        sh 'docker run --rm -v $PWD:/src aquasec/trivy:latest fs --scanners vuln,license --severity HIGH,CRITICAL --exit-code 1 /src/app'
      }
    }

    stage('Build and scan image (Trivy)') {
      steps {
        sh 'docker build -t $IMAGE app/'
        sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL --exit-code 1 $IMAGE'
      }
    }

    stage('SBOM (Syft)') {
      steps {
        sh 'docker run --rm -v $PWD:/src anchore/syft:latest dir:/src/app -o cyclonedx-json=/src/sbom.json'
      }
    }

    stage('DAST (OWASP ZAP)') {
      steps {
        sh '''
          docker run -d --name app -p 8080:8080 $IMAGE
          sleep 5
          docker run --rm --network host -v $PWD:/zap/wrk ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://localhost:8080 -r zap-report.html || true
          docker rm -f app
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: '*.sarif, sbom.json, zap-report.html', allowEmptyArchive: true
    }
  }
}

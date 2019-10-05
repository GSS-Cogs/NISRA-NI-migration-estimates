pipeline {
    agent {
        label 'master'
    }
    triggers {
        upstream(upstreamProjects: '../Reference/ref_migration',
                 threshold: hudson.model.Result.SUCCESS)
    }
    stages {
        stage('Clean') {
            steps {
                sh 'rm -rf out'
            }
        }
        stage('Transform') {
            agent {
                docker {
                    image 'csscogs/databaker'
                    reuseNode true
                }
            }
            steps {
                sh "jupyter-nbconvert --output-dir=out --execute 'main.ipynb'"
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'gsscogs/csvlint'
                    reuseNode true
                }
            }
            steps {
                script {
                    ansiColor('xterm') {
                        sh "csvlint -s schema.json"
                    }
                }
            }
        }
        stage('Upload draftset') {
            steps {
                script {
                    def csvs = []
                    for (def file : findFiles(glob: 'out/*.csv')) {
                        csvs.add("out/${file.name}")
                    }
                    jobDraft.replace()
                    uploadTidy(csvs, 'https://github.com/GSS-Cogs/ref_migration/raw/master/columns.csv')
                }
            }
        }
        stage('Publish') {
            steps {
                script {
                    jobDraft.publish()
                }
            }
        }
    }
    post {
        always {
            script {
                archiveArtifacts 'out/*'
                updateCard '5b9bb9cbf28e5f6a27594a66'
            }
        }
        success {
            build job: '../GDP-tests', wait: false
        }
    }
}

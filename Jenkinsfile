#!groovy
@Library(["devpi", "PythonHelpers"]) _

def remove_from_devpi(devpiExecutable, pkgName, pkgVersion, devpiIndex, devpiUsername, devpiPassword){
    script {
            try {
                bat "${devpiExecutable} login ${devpiUsername} --password ${devpiPassword}"
                bat "${devpiExecutable} use ${devpiIndex}"
                bat "${devpiExecutable} remove -y ${pkgName}==${pkgVersion}"
            } catch (Exception ex) {
                echo "Failed to remove ${pkgName}==${pkgVersion} from ${devpiIndex}"
        }

    }
}

pipeline {
    agent {
        label "Windows && Python3"
    }
    triggers {
        cron('@daily')
    }
    options {
        disableConcurrentBuilds()  //each branch has 1 job running at a time
//        timeout(25)  // Timeout after 20 minutes. This shouldn't take this long but it hangs for some reason
        checkoutToSubdirectory("scm")
        buildDiscarder logRotator(artifactDaysToKeepStr: '10', artifactNumToKeepStr: '10')
        preserveStashes(buildCount: 5)
    }
    environment {
        WORKON_HOME ="${WORKSPACE}\\pipenv"
        PKG_NAME = pythonPackageName(toolName: "CPython-3.6")
        PKG_VERSION = pythonPackageVersion(toolName: "CPython-3.6")
        DOC_ZIP_FILENAME = "${env.PKG_NAME}-${env.PKG_VERSION}.doc.zip"
        DEVPI = credentials("DS_devpi")

    }
    parameters {
        booleanParam(name: "FRESH_WORKSPACE", defaultValue: false, description: "Purge workspace before staring and checking out source")
        booleanParam(name: "TEST_RUN_PYTEST", defaultValue: true, description: "Run PyTest unit tests")
        booleanParam(name: "TEST_RUN_DOCTEST", defaultValue: true, description: "Test documentation")
        booleanParam(name: "TEST_RUN_FLAKE8", defaultValue: true, description: "Run Flake8 static analysis")
        booleanParam(name: "TEST_RUN_MYPY", defaultValue: true, description: "Run MyPy static analysis")
        booleanParam(name: "TEST_RUN_TOX", defaultValue: true, description: "Run Tox Tests")
        booleanParam(name: "DEPLOY_DEVPI", defaultValue: false, description: "Deploy to DevPi on https://devpi.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: "DEPLOY_DEVPI_PRODUCTION", defaultValue: false, description: "Deploy to https://devpi.library.illinois.edu/production/release")
//        booleanParam(name: "DEPLOY_HATHI_TOOL_BETA", defaultValue: false, description: "Deploy standalone to \\\\storage.library.illinois.edu\\HathiTrust\\Tools\\beta\\")
//        booleanParam(name: "DEPLOY_SCCM", defaultValue: false, description: "Request deployment of MSI installer to SCCM")
        booleanParam(name: "DEPLOY_DOCS", defaultValue: false, description: "Update online documentation")
    }

    stages {
        stage("Configure"){
            environment{
                PATH = "${tool 'CPython-3.6'};${PATH}"
            }
            stages{
                stage("Initial setup"){
                    parallel{
                        stage("Purge all existing data in workspace"){
                            when{
                                anyOf{
                                    equals expected: true, actual: params.FRESH_WORKSPACE
                                    triggeredBy "TimerTriggerCause"
                                }
                            }
                            steps{
                                deleteDir()
                                dir("scm"){
                                   checkout scm
                                }
                            }
                        }
                    }
                }
                stage("Installing Pipfile"){
                    options{
                        timeout(5)
                    }
                    steps {
                        bat "if not exist logs mkdir logs"
                        dir("scm"){
                            bat "python -m pipenv install --dev --deploy && python -m pipenv run pip list > ..\\logs\\pippackages_pipenv_${NODE_NAME}.log && python -m pipenv check"
                        }
                    }
                    post{
                        always{
                            archiveArtifacts artifacts: "logs/pippackages_pipenv_*.log"
                        }
                        failure {
                            deleteDir()
                        }
                        cleanup{
                            cleanWs(patterns: [[pattern: "logs/pippackages_pipenv_*.log", type: 'INCLUDE']])
                        }
                    }
                }
            }
            post{
                always{
                    echo "Configured ${env.PKG_NAME}, version ${env.PKG_VERSION}, for testing."
                }
            }
        }
        stage('Build') {
            environment{
                PATH = "${tool 'CPython-3.6'};${PATH}"
            }
            parallel {
                stage("Python Package"){
                    steps {

                        dir("scm"){
                            lock("system_pipenv_${NODE_NAME}"){
                                bat "python -m pipenv run python setup.py build -b ${WORKSPACE}\\build"
                            }
                        }
                    }
                }
                stage("Sphinx Documentation"){
                    steps {
                        echo "Building docs on ${env.NODE_NAME}"
                        dir("scm"){
                            bat "python -m pipenv run sphinx-build docs ${WORKSPACE}\\build\\docs\\html -d ${WORKSPACE}\\build\\docs\\.doctrees -w ${WORKSPACE}\\logs\\build_sphinx.log"
                        }
                    }
                    post{
                        always {
                            recordIssues(tools: [pep8(pattern: 'logs/build_sphinx.log')])
                            archiveArtifacts artifacts: 'logs/build_sphinx.log'
                        }
                        success{
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                            zip archive: true, dir: "${WORKSPACE}/build/docs/html", glob: '', zipFile: "dist/${env.DOC_ZIP_FILENAME}"
                            stash includes: "dist/${env.DOC_ZIP_FILENAME},build/docs/html/**", name: 'DOCS_ARCHIVE'

                        }
                        cleanup{
                            cleanWs(patterns:
                                    [
                                        [pattern: 'logs/build_sphinx.log', type: 'INCLUDE'],
                                        [pattern: "dist/${env.DOC_ZIP_FILENAME}", type: 'INCLUDE']
                                    ]
                                )
                        }
                    }
                }
            }
        }
        stage("Test") {
            environment{
                PATH = "${tool 'CPython-3.6'};${tool 'CPython-3.6'}\\Scripts;${PATH}"
            }
            stages{
                stage("Running Tests"){
                    parallel {
                        stage("Run PyTest Unit Tests"){
                            when {
                               equals expected: true, actual: params.TEST_RUN_PYTEST
                            }
                            environment{
                                junit_filename = "junit-${env.NODE_NAME}-${env.GIT_COMMIT.substring(0,7)}-pytest.xml"
                            }
                            steps{
                                dir("scm"){
                                    bat "python -m pipenv run coverage run --parallel-mode --source=uiucprescon -m pytest --junitxml=${WORKSPACE}/reports/pytest/${junit_filename} --junit-prefix=${env.NODE_NAME}-pytest"
                                }
                            }
                            post {
                                always {
                                    junit "reports/pytest/${junit_filename}"
                                }
                            }
                        }
                        stage("Run Doctest Tests"){
                            when {
                               equals expected: true, actual: params.TEST_RUN_DOCTEST
                            }
                            steps {
                                dir("scm"){
                                    bat "python -m pipenv run sphinx-build -b doctest docs ${WORKSPACE}\\build\\docs -d ${WORKSPACE}\\build\\docs\\doctrees -w ${WORKSPACE}\\logs\\doctest.log"
        //                            bat "pipenv run sphinx-build -b doctest docs\\scm ${WORKSPACE}\\build\\docs -d ${WORKSPACE}\\build\\docs\\doctrees"
                                }
                            }
                            post{
                                always {
                                    archiveArtifacts artifacts: "logs/doctest.log"
                                }
                                cleanup{
                                    cleanWs(patterns: [[pattern: 'logs/doctest.log', type: 'INCLUDE']])
                                }
                            }
                        }
                        stage("Run MyPy Static Analysis") {
                            when {
                                equals expected: true, actual: params.TEST_RUN_MYPY
                            }
                            steps{
                                dir("scm"){
                                    bat returnStatus: true, script: "pipenv run mypy -p uiucprescon --html-report ${WORKSPACE}\\reports\\mypy\\html > ${WORKSPACE}\\logs\\mypy.log"
                                }
                            }
                            post {
                                always {
                                    archiveArtifacts "logs\\mypy.log"
                                    recordIssues(tools: [myPy(pattern: 'logs/mypy.log')])

                                    publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy/html/', reportFiles: 'index.html', reportName: 'MyPy HTML Report', reportTitles: ''])
                                }
                                cleanup{
                                    cleanWs(patterns: [[pattern: 'logs/mypy.log', type: 'INCLUDE']])
                                }
                            }
                        }
                        stage("Run Tox test") {
                            when{
                                equals expected: true, actual: params.TEST_RUN_TOX
                            }
                            steps {
                                dir("scm"){
                                    script{
                                        try{
                                          bat "python -m pipenv run tox.exe --parallel=auto --parallel-live --workdir ${WORKSPACE}\\tox"
                                        } catch (exc) {
                                          bat "python -m pipenv run tox.exe --parallel=auto --parallel-live --workdir ${WORKSPACE}\\tox -vv --recreate"
                                        }
                                    }
                                }
                            }
                            post {
                                always {
                                    recordIssues(tools: [pep8(id: 'tox', name: 'Tox', pattern: '.tox/**/*.log')])
                                    archiveArtifacts artifacts: "tox/**/*.log", allowEmptyArchive: true
                                }
                                cleanup{
                                    cleanWs(
                                        patterns: [
                                                [pattern: 'tox/**/*.log', type: 'INCLUDE']
                                            ]
                                        )
                                }
                            }
                        }
                        stage("Run Flake8 Static Analysis") {
                            when {
                                equals expected: true, actual: params.TEST_RUN_FLAKE8
                            }
                            steps{
                                dir("scm"){
                                    bat returnStatus: true, script: "pipenv run flake8 uiucprescon --tee --output-file=${WORKSPACE}\\logs\\flake8.log"
                                }
                            }
                            post {
                                always {
                                      archiveArtifacts 'logs/flake8.log'
                                      recordIssues(tools: [flake8(pattern: 'logs/flake8.log')])
                                }
                                cleanup{
                                    cleanWs(patterns: [[pattern: 'logs/flake8.log', type: 'INCLUDE']])
                                }
                            }
                        }
                    }

                    post{
                        always{
                            dir("scm"){
                                bat "\"${tool 'CPython-3.6'}\\python.exe\" -m pipenv run coverage combine && \"${tool 'CPython-3.6'}\\python.exe\" -m pipenv run coverage xml -o ${WORKSPACE}\\reports\\coverage.xml && \"${tool 'CPython-3.6'}\\python.exe\" -m pipenv run coverage html -d ${WORKSPACE}\\reports\\coverage"

                            }
                            publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: "reports/coverage", reportFiles: 'index.html', reportName: 'Coverage', reportTitles: ''])
                            archiveArtifacts 'reports/coverage.xml'
                            publishCoverage(
                                adapters: [
                                    coberturaAdapter("reports/coverage.xml")
                                    ],
                                sourceFileResolver: sourceFiles('STORE_ALL_BUILD')
                            )
                        }
                        cleanup{
                            cleanWs(patterns: [
                                    [pattern: 'reports/coverage.xml', type: 'INCLUDE'],
                                    [pattern: 'reports/coverage', type: 'INCLUDE'],
                                    [pattern: 'scm/.coverage', type: 'INCLUDE'],
                                ])
                        }
                    }
                }
            }
        }
        stage("Packaging") {
            environment{
                PATH = "${tool 'CPython-3.6'};${tool 'CPython-3.6'}\\Scripts;${PATH}"
            }
            failFast true
            parallel {
                stage("Source and Wheel formats"){
                    stages{

                        stage("Packaging sdist and wheel"){

                            steps{
                                dir("scm"){
                                    bat script: "python -m pipenv run python setup.py build -b ../build sdist -d ../dist --format zip bdist_wheel -d ../dist"
                                }
                            }
                            post {
                                success {
                                    archiveArtifacts artifacts: "dist/*.whl,dist/*.tar.gz,dist/*.zip", fingerprint: true
                                    stash includes: "dist/*.whl,dist/*.tar.gz,dist/*.zip", name: 'PYTHON_PACKAGES'
                                }
                                cleanup{
                                    cleanWs deleteDirs: true, patterns: [[pattern: 'dist/*.whl,dist/*.tar.gz,dist/*.zip', type: 'INCLUDE']]
                                }
                            }
                        }
                    }
                }
            }


        }
        stage("Deploy to DevPi"){
            when {
                allOf{
                    anyOf{
                        equals expected: true, actual: params.DEPLOY_DEVPI
                        triggeredBy "TimerTriggerCause"
                    }
                    anyOf {
                        equals expected: "master", actual: env.BRANCH_NAME
                        equals expected: "dev", actual: env.BRANCH_NAME
                    }
                }
            }
            options{
                timestamps()
            }
//            environment{
//                PATH = "${WORKSPACE}\\venv\\Scripts;${tool 'CPython-3.6'};${tool 'CPython-3.6'}\\Scripts;${PATH}"
//            }

            stages{
                stage("Installing DevPi Client"){
                    environment{
                        PATH = "${tool 'CPython-3.6'};${PATH}"
                    }
                    steps{
                        bat "python -m venv venv\\36"
                        bat "venv\\36\\Scripts\\python.exe -m pip install pip --upgrade && venv\\36\\Scripts\\pip install devpi-client"
                    }
                }
                stage("Deploy to DevPi Staging") {
                    environment{
                        PATH = "${WORKSPACE}\\venv\\36\\Scripts;${PATH}"
                    }

                    steps {
                        unstash 'DOCS_ARCHIVE'
                        unstash 'PYTHON_PACKAGES'
                        bat "devpi use https://devpi.library.illinois.edu && devpi login ${env.DEVPI_USR} --password ${env.DEVPI_PSW} && devpi use /${env.DEVPI_USR}/${env.BRANCH_NAME}_staging && devpi upload --from-dir dist"
                    }
                }
                stage("Test DevPi packages") {
                    parallel {
                        stage("Source Distribution: .zip") {
                            agent {
                                node {
                                    label "Windows && Python3"
                                }
                            }
                            options {
                                skipDefaultCheckout(true)

                            }

                            stages{

                                stage("Creating Env for DevPi to test sdist"){
                                    environment{
                                        PATH = "${tool 'CPython-3.6'};${PATH}"
                                    }
                                    steps {
                                        lock("system_python_${NODE_NAME}"){
                                            bat "python -m venv venv"
                                        }
                                        bat "venv\\Scripts\\python.exe -m pip install pip --upgrade && venv\\Scripts\\pip.exe install setuptools --upgrade && venv\\Scripts\\pip.exe install \"tox<3.7\" detox devpi-client"
                                    }
                                }
                                stage("Testing sdist"){
                                    environment{
                                        PATH = "${WORKSPACE}\\venv\\Scripts;${tool 'CPython-3.6'};${tool 'CPython-3.7'}${PATH}"
                                    }
                                    options{
                                        timeout(10)
                                    }
                                    steps{
                                        bat "devpi use https://devpi.library.illinois.edu/${env.BRANCH_NAME}_staging"
                                        devpiTest(
                                            devpiExecutable: "${powershell(script: '(Get-Command devpi).path', returnStdout: true).trim()}",
                                            url: "https://devpi.library.illinois.edu",
                                            index: "${env.BRANCH_NAME}_staging",
                                            pkgName: "${env.PKG_NAME}",
                                            pkgVersion: "${env.PKG_VERSION}",
                                            pkgRegex: "zip",
                                            detox: false
                                        )
                                    }
                                }

                            }
                            post{
                                cleanup{
                                    cleanWs deleteDirs: true, patterns: [
                                            [pattern: 'certs', type: 'INCLUDE'],
                                            [pattern: '*tmp', type: 'INCLUDE']
                                        ]
                                }
                            }
                        }

                        stage("Built Distribution: .whl") {
                            agent {
                                node {
                                    label "Windows && Python3"
                                }
                            }
                            options {
                                skipDefaultCheckout(true)
                            }

                            stages{
                                stage("Creating Env for DevPi to test whl"){
                                    environment{
                                        PATH = "${tool 'CPython-3.6'};$PATH"
                                    }
                                    steps{
                                        lock("system_python_${NODE_NAME}"){
                                            bat "python -m pip install pip --upgrade && python -m venv venv "
                                        }
                                        bat "venv\\Scripts\\python.exe -m pip install pip --upgrade && venv\\Scripts\\pip.exe install setuptools --upgrade && venv\\Scripts\\pip.exe install \"tox<3.7\"  detox devpi-client"
                                    }
                                }
                                stage("Testing Whl"){
                                    options{
                                        timeout(10)
                                    }
                                    environment{
                                        PATH = "${WORKSPACE}\\venv\\Scripts;${tool 'CPython-3.6'};${tool 'CPython-3.7'};${PATH}"
                                    }
                                    steps {
                                        devpiTest(
                                            devpiExecutable: "${powershell(script: '(Get-Command devpi).path', returnStdout: true).trim()}",
                                            url: "https://devpi.library.illinois.edu",
                                            index: "${env.BRANCH_NAME}_staging",
                                            pkgName: "${env.PKG_NAME}",
                                            pkgVersion: "${env.PKG_VERSION}",
                                            pkgRegex: "whl",
                                            detox: false
                                        )
                                    }
                                }
                            }


                            post{
                                failure{
                                    cleanWs deleteDirs: true, patterns: [[pattern: 'venv', type: 'INCLUDE']]
                                }
                                cleanup{
                                    cleanWs deleteDirs: true, patterns: [
                                            [pattern: 'certs', type: 'INCLUDE'],
                                            [pattern: '*tmp', type: 'INCLUDE']
                                        ]
                                }
                            }
                        }
                    }
                    post {
                        success {
                            echo "It Worked. Pushing file to ${env.BRANCH_NAME} index"
                            bat "venv\\36\\Scripts\\devpi.exe use https://devpi.library.illinois.edu/${env.BRANCH_NAME}_staging && venv\\36\\Scripts\\devpi login ${env.DEVPI_USR} --password ${env.DEVPI_PSW} && venv\\36\\Scripts\\devpi.exe use http://devpi.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}_staging && venv\\36\\Scripts\\devpi.exe push ${env.PKG_NAME}==${env.PKG_VERSION} DS_Jenkins/${env.BRANCH_NAME}"
                        }
                    }
                }
                stage("Deploy to DevPi Production") {
                    when {
                        allOf{
                            equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
                            branch "master"
                        }
                    }
                    stages{
                        stage("Pushing to DevPi Production"){
                            input {
                                message "Release to DevPi Production?"
                            }
                            steps {
//                                input "Release ${env.PKG_NAME} ${env.PKG_VERSION} to DevPi Production?"
                                bat "venv\\36\\Scripts\\devpi.exe login ${env.DEVPI_USR} --password ${env.DEVPI_PSW} && venv\\36\\Scripts\\devpi.exe use /${env.DEVPI_USR}/${env.BRANCH_NAME}_staging && venv\\36\\Scripts\\devpi.exe push ${env.PKG_NAME}==${env.PKG_VERSION} production/release"
                            }

                        }
                    }

                }
            }
            post{
                cleanup{
                    remove_from_devpi("venv\\36\\Scripts\\devpi.exe", "${env.PKG_NAME}", "${env.PKG_VERSION}", "/${env.DEVPI_USR}/${env.BRANCH_NAME}_staging", "${env.DEVPI_USR}", "${env.DEVPI_PSW}")
                }
            }
        }
        stage("Deploy"){
            parallel {
                stage("Deploy Online Documentation") {
                    when{
                        equals expected: true, actual: params.DEPLOY_DOCS
                    }
                    steps{
                        unstash "DOCS_ARCHIVE"

                        dir("build/docs/html/"){
                            input 'Update project documentation?'
                            sshPublisher(
                                publishers: [
                                    sshPublisherDesc(
                                        configName: 'apache-ns - lib-dccuser-updater',
                                        sshLabel: [label: 'Linux'],
                                        transfers: [sshTransfer(excludes: '',
                                        execCommand: '',
                                        execTimeout: 120000,
                                        flatten: false,
                                        makeEmptyDirs: false,
                                        noDefaultExcludes: false,
                                        patternSeparator: '[, ]+',
                                        remoteDirectory: "${env.PKG_NAME}",
                                        remoteDirectorySDF: false,
                                        removePrefix: '',
                                        sourceFiles: '**')],
                                    usePromotionTimestamp: false,
                                    useWorkspaceInPromotion: false,
                                    verbose: true
                                    )
                                ]
                            )
                        }
                    }
                }

            }
        }

    }
    post {
        cleanup {

            cleanWs deleteDirs: true, patterns: [
                    [pattern: 'logs', type: 'INCLUDE'],
                    [pattern: 'dist', type: 'INCLUDE'],
                    [pattern: 'reports', type: 'INCLUDE'],
                    [pattern: 'build', type: 'INCLUDE'],
                    [pattern: 'scm', type: 'INCLUDE'],
                    [pattern: '*tmp', type: 'INCLUDE']
                ]
        }

    }
}

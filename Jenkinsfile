#!groovy
@Library(["devpi", "PythonHelpers"]) _

CONFIGURATIONS = [
    '3.6': [
        test_docker_image: "python:3.6-windowsservercore",
        tox_env: "py36"
        ],
    "3.7": [
        test_docker_image: "python:3.7",
        tox_env: "py37"
        ]
]

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

def parseBanditReport(htmlReport){
    script {
        try{
            def summary = createSummary icon: 'warning.gif', text: "Bandit Security Issues Detected"
            summary.appendText(readFile("${htmlReport}"))

        } catch (Exception e){
            echo "Failed to reading ${htmlReport}"
        }
    }
}

def get_sonarqube_unresolved_issues(report_task_file){
    script{

        def props = readProperties  file: '.scannerwork/report-task.txt'
        def response = httpRequest url : props['serverUrl'] + "/api/issues/search?componentKeys=" + props['projectKey'] + "&resolved=no"
        def outstandingIssues = readJSON text: response.content
        return outstandingIssues
    }
}

def get_sonarqube_scan_data(report_task_file){
    script{

        def props = readProperties  file: '.scannerwork/report-task.txt'

        def ceTaskUrl= props['ceTaskUrl']
        def response = httpRequest ceTaskUrl
        def ceTask = readJSON text: response.content

        def response2 = httpRequest url : props['serverUrl'] + "/api/qualitygates/project_status?analysisId=" + ceTask["task"]["analysisId"]
        def qualitygate =  readJSON text: response2.content
        return qualitygate
    }
}

def get_sonarqube_project_analysis(report_task_file, buildString){
    def props = readProperties  file: '.scannerwork/report-task.txt'
    def response = httpRequest url : props['serverUrl'] + "/api/project_analyses/search?project=" + props['projectKey']
    def project_analyses = readJSON text: response.content

    for( analysis in project_analyses['analyses']){
        if(!analysis.containsKey("buildString")){
            continue
        }
        def build_string = analysis["buildString"]
        if(build_string != buildString){
            continue
        }
        return analysis
    }
}


def get_package_version(stashName, metadataFile){
    ws {
        unstash "${stashName}"
        script{
            def props = readProperties interpolate: true, file: "${metadataFile}"
            deleteDir()
            return props.Version
        }
    }
}

def get_package_name(stashName, metadataFile){
    ws {
        unstash "${stashName}"
        script{
            def props = readProperties interpolate: true, file: "${metadataFile}"
            deleteDir()
            return props.Name
        }
    }
}

pipeline {
    agent none
    triggers {
        parameterizedCron '@daily % DEPLOY_DEVPI=true; TEST_RUN_TOX=true'
    }
    options {
        disableConcurrentBuilds()  //each branch has 1 job running at a time
        buildDiscarder logRotator(artifactDaysToKeepStr: '10', artifactNumToKeepStr: '10')
        preserveStashes(buildCount: 5)
    }
    environment {
        WORKON_HOME ="${WORKSPACE}\\pipenv"
    }
    parameters {
        booleanParam(name: "FRESH_WORKSPACE", defaultValue: false, description: "Purge workspace before staring and checking out source")
        booleanParam(name: "TEST_RUN_TOX", defaultValue: false, description: "Run Tox Tests")
        booleanParam(name: "DEPLOY_DEVPI", defaultValue: false, description: "Deploy to DevPi on https://devpi.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: "DEPLOY_DEVPI_PRODUCTION", defaultValue: false, description: "Deploy to https://devpi.library.illinois.edu/production/release")
        booleanParam(name: "DEPLOY_DOCS", defaultValue: false, description: "Update online documentation")
    }

    stages {
        stage("Getting Distribution Info"){
            agent {
                dockerfile {
                    filename 'ci/docker/python37/windows/build/msvc/Dockerfile'
                    label 'Windows&&Docker'
                 }
            }
            steps{
                bat "python setup.py dist_info"
            }
            post{
                success{
                    stash includes: "uiucprescon.images.dist-info/**", name: 'DIST-INFO'
                    archiveArtifacts artifacts: "uiucprescon.images.dist-info/**"
                }
                cleanup{
                    cleanWs(
                        deleteDirs: true,
                        patterns: [
                            [pattern: "uiucprescon.images.dist-info/", type: 'INCLUDE'],
                            [pattern: ".eggs/", type: 'INCLUDE'],
                        ]
                    )
                }
            }
        }
        stage('Build') {
            parallel {
                stage("Python Package"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python37/windows/build/msvc/Dockerfile'
                            label 'Windows&&Docker'
                         }
                    }
                    steps {
                        bat "if not exist logs mkdir logs"
                        bat "python setup.py build -b ${WORKSPACE}\\build"
                    }
                }
                stage("Sphinx Documentation"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python37/windows/build/msvc/Dockerfile'
                            label 'Windows&&Docker'
                         }
                    }
                    environment{
                        PKG_NAME = get_package_name("DIST-INFO", "uiucprescon.images.dist-info/METADATA")
                        PKG_VERSION = get_package_version("DIST-INFO", "uiucprescon.images.dist-info/METADATA")
                    }
                    steps {
                        bat "if not exist logs mkdir logs"
                        bat(
                            label: "Building docs on ${env.NODE_NAME}",
                            script: "python -m sphinx docs ${WORKSPACE}\\build\\docs\\html -d ${WORKSPACE}\\build\\docs\\.doctrees -w ${WORKSPACE}\\logs\\build_sphinx.log"
                            )
                    }
                    post{
                        always {
                            recordIssues(tools: [pep8(pattern: 'logs/build_sphinx.log')])
                            archiveArtifacts artifacts: 'logs/build_sphinx.log'
                        }
                        success{
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                            script{
                                def DOC_ZIP_FILENAME = "${env.PKG_NAME}-${env.PKG_VERSION}.doc.zip"
                                zip archive: true, dir: "${WORKSPACE}/build/docs/html", glob: '', zipFile: "dist/${DOC_ZIP_FILENAME}"
                                stash includes: "dist/${DOC_ZIP_FILENAME},build/docs/html/**", name: 'DOCS_ARCHIVE'
                            }

                        }
                        cleanup{
                            cleanWs(
                                patterns: [
                                    [pattern: 'logs/', type: 'INCLUDE'],
                                    [pattern: "build/docs/", type: 'INCLUDE'],
                                    [pattern: "dist/", type: 'INCLUDE']
                                ],
                                deleteDirs: true
                            )
                        }
                    }
                }
            }
        }
        stage("Test") {
            agent {
                dockerfile {
                    filename 'ci/docker/python37/windows/build/msvc/Dockerfile'
                    label 'Windows&&Docker'
                 }
            }
            stages{
                stage("Setting up Tests"){
                    steps{
                        bat "if not exist reports mkdir reports"
                        bat "if not exist logs mkdir logs"
                    }
                }
                stage("Running Tests"){
                    parallel {
                        stage("Run PyTest Unit Tests"){
                            steps{
                                bat "coverage run --parallel-mode -m pytest --junitxml=${WORKSPACE}/reports/pytest/junit-${env.NODE_NAME}-pytest.xml --junit-prefix=${env.NODE_NAME}-pytest"
                            }
                            post {
                                always {
                                    junit "reports/pytest/junit-${env.NODE_NAME}-pytest.xml"
                                }
                                cleanup{
                                    cleanWs(
                                        patterns: [
                                            [pattern: 'reports/pytest/junit-*.xml', type: 'INCLUDE'],
                                            [pattern: '.pytest_cache/', type: 'INCLUDE'],
                                        ],
                                        deleteDirs: true,
                                    )
                                }
                            }
                        }
                        stage("Run Doctest Tests"){
                            steps {
                                bat "sphinx-build -b doctest docs ${WORKSPACE}\\build\\docs -d ${WORKSPACE}\\build\\docs\\doctrees -w ${WORKSPACE}\\logs\\doctest.log"
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
                            steps{
                                bat returnStatus: true, script: "mypy -p uiucprescon --html-report ${WORKSPACE}\\reports\\mypy\\html > ${WORKSPACE}\\logs\\mypy.log"
                            }
                            post {
                                always {
                                    archiveArtifacts "logs\\mypy.log"
                                    recordIssues(tools: [myPy(pattern: 'logs/mypy.log')])
                                    publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy/html/', reportFiles: 'index.html', reportName: 'MyPy HTML Report', reportTitles: ''])
                                }
                                cleanup{
                                    cleanWs(
                                        patterns: [
                                            [pattern: 'logs/mypy.log', type: 'INCLUDE'],
                                            [pattern: '.mypy_cache/', type: 'INCLUDE'],
                                        ],
                                        deleteDirs: true,
                                    )
                                }
                            }
                        }
                        stage("Run Tox test") {
                            when{
                                equals expected: true, actual: params.TEST_RUN_TOX
                            }
                            steps {
                                  bat "tox --workdir ${WORKSPACE}\\tox -e py"
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
                            steps{
                                bat returnStatus: true, script: "flake8 uiucprescon --tee --output-file=${WORKSPACE}\\logs\\flake8.log"
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
                        stage("Run Pylint Static Analysis") {
                            steps{
                                catchError(buildResult: 'SUCCESS', message: 'Pylint found issues', stageResult: 'UNSTABLE') {
                                    bat(
                                        script: 'pylint uiucprescon  -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > %WORKSPACE%\\reports\\pylint.txt & pylint uiucprescon  -r n --msg-template="{path}:{module}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > %WORKSPACE%\\reports\\pylint_issues.txt',
                                        label: "Running pylint"
                                    )
                                }
                                script{
                                    if(env.BRANCH_NAME == "master"){
                                        bat(
                                            script: 'pylint uiucprescon  -r n --msg-template="{path}:{module}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports\\pylint_issues.txt',
                                            label: "Running pylint for sonarqube",
                                            returnStatus: true
                                        )
                                    }
                                }
                            }
                            post{
                                always{
                                    archiveArtifacts allowEmptyArchive: true, artifacts: "reports/pylint.txt"
                                    recordIssues(tools: [pyLint(pattern: 'reports/pylint_issues.txt')])
                                    stash(
                                        name: 'PYLINT_SONAR_REPORT',
                                        includes: "reports\\pylint_issues.txt",
                                        allowEmpty: true
                                        )
                                }
                            }
                        }
                        stage("Run Bandit Static Analysis") {
                            steps{
                                catchError(buildResult: 'SUCCESS', message: 'Bandit found issues', stageResult: 'UNSTABLE') {
                                    bat(
                                        label: "Running bandit",
                                        script: "bandit --format json --output ${WORKSPACE}\\reports\\bandit-report.json --recursive ${WORKSPACE}\\uiucprescon\\images || bandit -f html --recursive ${WORKSPACE}\\uiucprescon\\images --output ${WORKSPACE}/reports/bandit-report.html"
                                    )
                                }
                            }
                            post {
                                always {
                                    archiveArtifacts "reports/bandit-report.json,reports/bandit-report.html"
                                    stash( includes: "reports/bandit-report.json", name: 'BANDIT_REPORT')
                                }
                                unstable{
                                    script{
                                        if(fileExists('reports/bandit-report.html')){
                                            parseBanditReport("reports/bandit-report.html")
                                            addWarningBadge text: "Bandit security issues detected", link: "${currentBuild.absoluteUrl}"
                                        }
                                    }
                                }
                            }
                        }
                    }
                    post{
                        always{
                            bat "coverage combine && coverage xml -o ${WORKSPACE}\\reports\\coverage.xml && coverage html -d ${WORKSPACE}\\reports\\coverage"
                            publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: "reports/coverage", reportFiles: 'index.html', reportName: 'Coverage', reportTitles: ''])
                            publishCoverage(
                                adapters: [
                                    coberturaAdapter("reports/coverage.xml")
                                    ],
                                sourceFileResolver: sourceFiles('STORE_ALL_BUILD')
                            )
                            stash( includes: "reports/coverage.xml", name: 'COVERAGE_REPORT')
                            archiveArtifacts 'reports/coverage.xml'
                        }
                        cleanup{
                            cleanWs(
                                patterns: [
                                    [pattern: 'build/', type: 'INCLUDE'],
                                    [pattern: 'logs/', type: 'INCLUDE'],
                                    [pattern: 'reports/', type: 'INCLUDE'],
                                    [pattern: "uiucprescon.images.egg-info/", type: 'INCLUDE'],
                                ],
                                deleteDirs: true,
                            )
                        }
                    }
                }
            }
            post{
                cleanup{
                    cleanWs(patterns: [
                            [pattern: 'reports/coverage.xml', type: 'INCLUDE'],
                            [pattern: 'reports/coverage', type: 'INCLUDE'],
                        ])
                }
            }
        }
        stage("Run SonarQube Analysis"){
            when{
                equals expected: "master", actual: env.BRANCH_NAME
                beforeAgent true
            }
            agent{
                label "windows"
            }
            environment{
                scannerHome = tool name: 'sonar-scanner-3.3.0', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
            }
            steps{
                unstash "DIST-INFO"
                unstash "COVERAGE_REPORT"
                unstash "BANDIT_REPORT"
                unstash "PYLINT_SONAR_REPORT"
                script{
                    def props = readProperties interpolate: true, file: 'uiucprescon.images.dist-info/METADATA'
                    withSonarQubeEnv('sonarqube.library.illinois.edu') {
                        withEnv(["PROJECT_DESCRIPTION=${props.Summary}"]) {
                            bat(
                                label: "Running Sonar Scanner",
                                script: "${env.scannerHome}/bin/sonar-scanner \
-Dsonar.projectBaseDir=${WORKSPACE} \
-Dsonar.python.coverage.reportPaths=reports/coverage.xml \
-Dsonar.python.xunit.reportPath=reports/pytest/junit-${env.NODE_NAME}-pytest.xml \
-Dsonar.projectVersion=${props.Version} \
-Dsonar.python.bandit.reportPaths=${WORKSPACE}/reports/bandit-report.json \
-Dsonar.links.ci=${env.JOB_URL} \
-Dsonar.buildString=${env.BUILD_TAG} \
-Dsonar.analysis.packageName=${props.Name} \
-Dsonar.analysis.buildNumber=${env.BUILD_NUMBER} \
-Dsonar.analysis.scmRevision=${env.GIT_COMMIT} \
-Dsonar.working.directory=${WORKSPACE}\\.scannerwork \
-Dsonar.python.pylint.reportPath=${WORKSPACE}\\reports\\pylint.txt \
-Dsonar.projectDescription=\"%PROJECT_DESCRIPTION%\" \
"
                            )
                        }
                    }
                }
                script{
                    def sonarqube_result = waitForQualityGate abortPipeline: false
                    if(sonarqube_result.status != "OK"){
                        unstable("SonarQube quality gate: ${sonarqube_result}")
                    }
                    def sonarqube_data = get_sonarqube_scan_data(".scannerwork/report-task.txt")
                    echo sonarqube_data.toString()

                    echo get_sonarqube_project_analysis(".scannerwork/report-task.txt", BUILD_TAG).toString()
                    def outstandingIssues = get_sonarqube_unresolved_issues(".scannerwork/report-task.txt")
                    writeJSON file: 'reports/sonar-report.json', json: outstandingIssues
                }
            }
            post{
                always{
                    archiveArtifacts allowEmptyArchive: true, artifacts: 'reports/sonar-report.json'
                    recordIssues(tools: [sonarQube(pattern: 'reports/sonar-report.json')])
                }
                cleanup{
                    dir(".scannerwork"){
                        deleteDir()
                    }
                }
            }
        }
        stage("Packaging") {
            agent {
                dockerfile {
                    filename 'ci/docker/python37/windows/build/msvc/Dockerfile'
                    label 'Windows&&Docker'
                 }
            }
            steps{
                bat script: "python setup.py build -b build sdist -d dist --format zip bdist_wheel -d dist"
            }
            post {
                success {
                    archiveArtifacts artifacts: "dist/*.whl,dist/*.tar.gz,dist/*.zip", fingerprint: true
                    stash includes: "dist/*.whl,dist/*.tar.gz,dist/*.zip", name: 'PYTHON_PACKAGES'
                }
                cleanup{
                    cleanWs(
                        deleteDirs: true,
                        patterns: [
                            [pattern: 'dist/', type: 'INCLUDE'],
                            [pattern: 'build/', type: 'INCLUDE'],
                            [pattern: "uiucprescon.images.egg-info/", type: 'INCLUDE'],
                        ]
                    )
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
                beforeAgent true
            }
            options{
                timestamps()
            }
            agent none
            environment{
                DEVPI = credentials("DS_devpi")
            }
            stages{
                stage("Deploy to Devpi Staging") {
                    agent {
                        dockerfile {
                            filename 'ci/docker/deploy/devpi/deploy/Dockerfile'
                            label 'linux&&docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                          }
                    }
                    steps {
                        unstash 'DOCS_ARCHIVE'
                        unstash 'PYTHON_PACKAGES'
                        sh(
                            label: "Connecting to DevPi Server",
                            script: 'devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi'
                        )
                        sh(
                            label: "Uploading to DevPi Staging",
                            script: """devpi use /${env.DEVPI_USR}/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi
devpi upload --from-dir dist --clientdir ${WORKSPACE}/devpi"""
                        )
                    }
                }
                stage("Test DevPi packages") {
                    matrix {
                        axes {
                            axis {
                                name 'FORMAT'
                                values 'zip', "whl"
                            }
                            axis {
                                name 'PYTHON_VERSION'
                                values '3.6', "3.7"
                            }
                        }
                        agent {
                          dockerfile {
                            additionalBuildArgs "--build-arg PYTHON_DOCKER_IMAGE_BASE=${CONFIGURATIONS[PYTHON_VERSION].test_docker_image}"
                            filename 'CI/docker/deploy/devpi/test/windows/Dockerfile'
                            label 'windows && docker'
                          }
                        }
                        stages{
                            stage("Testing DevPi Package"){
                                options{
                                    timeout(10)
                                }
                                steps{
                                    script{
                                        unstash "DIST-INFO"
                                        def props = readProperties interpolate: true, file: 'uiucprescon.images.dist-info/METADATA'
                                        bat(
                                            label: "Connecting to Devpi Server",
                                            script: "devpi use https://devpi.library.illinois.edu --clientdir certs\\ && devpi login %DEVPI_USR% --password %DEVPI_PSW% --clientdir certs\\ && devpi use ${env.BRANCH_NAME}_staging --clientdir certs\\"
                                        )
                                        bat(
                                            label: "Testing package stored on DevPi",
                                            script: "devpi test --index ${env.BRANCH_NAME}_staging ${props.Name}==${props.Version} -s ${FORMAT} --clientdir certs\\ -e ${CONFIGURATIONS[PYTHON_VERSION].tox_env} -v"
                                        )
                                    }
                                }
                                post{
                                    cleanup{
                                        cleanWs(
                                            deleteDirs: true,
                                            patterns: [
                                                [pattern: "dist/", type: 'INCLUDE'],
                                                [pattern: "certs/", type: 'INCLUDE'],
                                                [pattern: "dcc_qc.dist-info/", type: 'INCLUDE'],
                                                [pattern: 'build/', type: 'INCLUDE']
                                            ]
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
            post{
                success{
                    node('linux && docker') {
                       script{
                            docker.build("uiucpresconimages:devpi.${env.BUILD_ID}",'-f ./ci/docker/deploy/devpi/deploy/Dockerfile --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .').inside{
                                unstash "DIST-INFO"
                                def props = readProperties interpolate: true, file: 'uiucprescon.images.dist-info/METADATA'
                                sh(
                                    label: "Connecting to DevPi Server",
                                    script: 'devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi'
                                )
                                sh(
                                    label: "Selecting to DevPi index",
                                    script: "devpi use /DS_Jenkins/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi"
                                )
                                sh(
                                    label: "Pushing package to DevPi index",
                                    script:  "devpi push ${props.Name}==${props.Version} DS_Jenkins/${env.BRANCH_NAME} --clientdir ${WORKSPACE}/devpi"
                                )
                            }
                       }
                    }
                }
                cleanup{
                    node('linux && docker') {
                       script{
                            docker.build("uiucpresconimages:devpi.${env.BUILD_ID}",'-f ./ci/docker/deploy/devpi/deploy/Dockerfile --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .').inside{
                                unstash "DIST-INFO"
                                def props = readProperties interpolate: true, file: 'uiucprescon.images.dist-info/METADATA'
                                sh(
                                    label: "Connecting to DevPi Server",
                                    script: 'devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi'
                                )
                                sh(
                                    label: "Selecting to DevPi index",
                                    script: "devpi use /DS_Jenkins/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi"
                                )
                                sh(
                                    label: "Removing package to DevPi index",
                                    script: "devpi remove -y ${props.Name}==${props.Version} --clientdir ${WORKSPACE}/devpi"
                                )
                            }
                       }
                    }
                }
            }
        }
        stage("Deploy"){
            parallel {
                stage("Deploy Online Documentation") {
                    agent any
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
}

#!groovy
def getDevPiStagingIndex(){

    if (env.TAG_NAME?.trim()){
        return 'tag_staging'
    } else{
        return "${env.BRANCH_NAME}_staging"
    }
}

def DEVPI_CONFIG = [
    stagingIndex: getDevPiStagingIndex(),
    server: 'https://devpi.library.illinois.edu',
    credentialsId: 'DS_devpi',
]

SONARQUBE_CREDENTIAL_ID = 'sonarcloud-uiucprescon.images'
SUPPORTED_MAC_VERSIONS = ['3.8', '3.9']
SUPPORTED_LINUX_VERSIONS = ['3.6', '3.7', '3.8', '3.9']
SUPPORTED_WINDOWS_VERSIONS = ['3.6', '3.7', '3.8', '3.9']

PYPI_SERVERS = [
    'https://jenkins.library.illinois.edu/nexus/repository/uiuc_prescon_python_public/',
    'https://jenkins.library.illinois.edu/nexus/repository/uiuc_prescon_python/',
    'https://jenkins.library.illinois.edu/nexus/repository/uiuc_prescon_python_testing/'
    ]


CONFIGURATIONS = [
    "3.7" : [
        os: [
            windows: [
                agents: [
                    build: [
                        dockerfile: [
                            filename: 'ci/docker/python/windows/build/msvc/Dockerfile',
                            label: 'Windows&&Docker',
                            additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                        ]
                    ],
                    test: [
                        dockerfile: [
                            filename: 'ci/docker/python/windows/build/msvc/Dockerfile',
                            label: 'Windows&&Docker',
                            additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                        ]
                    ],
                    devpi: [
                        dockerfile: [
                            filename: 'ci/docker/python/windows/build/msvc/Dockerfile',
                            label: 'windows && docker',
                            additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.7'
                        ]
                    ]
                ],
                pkgRegex: [
                    wheel: "*.whl",
                    sdist: "*.zip"
                ]
            ],
            linux: [
                agents: [
                    build: [
                        dockerfile: [
                            filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                            label: 'linux&&docker',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ],
                    test: [
                        dockerfile: [
                            filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                            label: 'linux&&docker',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ],
                    devpi: [
                        dockerfile: [
                            filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                            label: 'linux&&docker',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ]
                ],
                pkgRegex: [
                    wheel: "*.whl",
                    sdist: "*.zip"
                ]
            ]
        ],
        tox_env: "py37",
        devpiSelector: [
            sdist: "zip",
            wheel: "whl",
        ],
        pkgRegex: [
            wheel: "*.whl",
            sdist: "*.zip"
        ]
    ],
    "3.8" : [
        os: [
            windows: [
                agents: [
                    build: [
                        dockerfile: [
                            filename: 'ci/docker/python/windows/build/msvc/Dockerfile',
                            label: 'Windows&&Docker',
                            additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                        ]
                    ],
                    test: [
                        dockerfile: [
                            filename: 'ci/docker/python/windows/build/msvc/Dockerfile',
                            label: 'windows && docker',
                            additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                        ]
                    ],
                    devpi: [
                        dockerfile: [
                            filename: 'ci/docker/python/windows/build/msvc/Dockerfile',
                            label: 'windows && docker',
                            additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PYTHON_DOCKER_IMAGE_BASE=python:3.8'
                        ]
                    ]

                ],
                pkgRegex: [
                    wheel: "*.whl",
                    sdist: "*.zip"
                ]
            ],
            linux: [
                agents: [
                    build: [
                        dockerfile: [
                            filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                            label: 'linux&&docker',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ],
                    test: [
                        dockerfile: [
                            filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                            label: 'linux&&docker',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ],
                    devpi: [
                        dockerfile: [
                            filename: 'ci/docker/python/linux/jenkins/Dockerfile',
                            label: 'linux&&docker',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ]
                ],
                pkgRegex: [
                    wheel: "*.whl",
                    sdist: "*.zip"
                ]
            ]
        ],
        tox_env: "py38",
        devpiSelector: [
            sdist: "zip",
            wheel: "whl",
        ],
        pkgRegex: [
            wheel: "*.whl",
            sdist: "*.zip"
        ]
    ],
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
        if (! fileExists(report_task_file)){
            error "File not found ${report_task_file}"
        }
        def props = readProperties  file: report_task_file
        def response = httpRequest url : props['serverUrl'] + "/api/issues/search?componentKeys=" + props['projectKey'] + "&resolved=no"
        def outstandingIssues = readJSON text: response.content
        return outstandingIssues
    }
}

def get_sonarqube_scan_data(report_task_file){
    script{
        if (! fileExists(report_task_file)){
            error "File not found ${report_task_file}"
        }
        def props = readProperties  file: report_task_file

        def ceTaskUrl= props['ceTaskUrl']
        def response = httpRequest ceTaskUrl
        def ceTask = readJSON text: response.content
        def analysisId = ceTask["task"]["analysisId"]
         if(analysisId == null){
            error "Unable to parse analysisId from ${report_task_file}"
        }

        def response2 = httpRequest url : props['serverUrl'] + "/api/qualitygates/project_status?analysisId=" + analysisId
        def qualitygate =  readJSON text: response2.content
        return qualitygate
    }
}

def get_sonarqube_project_analysis(report_task_file, buildString){
    if (! fileExists(report_task_file)){
            error "File not found ${report_task_file}"
        }
    def props = readProperties  file: report_task_file

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

defaultParameterValues = [
    USE_SONARQUBE: false
]

def startup(){
    parallel(
        [
            failFast: true,
            'Checking Sonarqube Settings': {
                def SONARQUBE_CREDENTIAL_ID = SONARQUBE_CREDENTIAL_ID
                node(){
                    try{
                        withCredentials([string(credentialsId: SONARQUBE_CREDENTIAL_ID, variable: 'dddd')]) {
                            echo 'Found credentials for sonarqube'
                        }
                        defaultParameterValues.USE_SONARQUBE = true
                    } catch(e){
                        echo "Setting defaultValue for USE_SONARQUBE to false. Reason: ${e}"
                        defaultParameterValues.USE_SONARQUBE = false
                    }
                }
            },
            'Getting Distribution Info': {
                node('linux && docker') {
                    try{
                        checkout scm
                        docker.image('python').inside {
                            timeout(2){
                                withEnv(['PIP_NO_CACHE_DIR=off']) {
                                    sh(
                                       label: 'Running setup.py with dist_info',
                                       script: """python --version
                                                  python setup.py dist_info
                                               """
                                    )
                                }
                                stash includes: '*.dist-info/**', name: 'DIST-INFO'
                                archiveArtifacts artifacts: '*.dist-info/**'
                            }
                        }
                    } finally{
                        cleanWs(
                           deleteDirs: true,
                           patterns: [
                              [pattern: '*.dist-info/', type: 'INCLUDE'],
                              [pattern: '**/__pycache__', type: 'INCLUDE'],
                              [pattern: '.eggs/', type: 'INCLUDE'],
                          ]
                       )
                    }
                }
            }
        ]
    )
}
def get_props(){
    stage('Reading Package Metadata'){
        node() {
            try{
                unstash 'DIST-INFO'
                def metadataFile = findFiles( glob: '*.dist-info/METADATA')[0]
                def packageMetadata = readProperties(
                    interpolate: true,
                    file: metadataFile.path
                    )

                if(packageMetadata.Name == null){
                    error("No 'Name' located in ${metadataFile.path} file")
                }

                if(packageMetadata.Version == null){
                    error("No 'Version' located in ${metadataFile.path} file")
                }

                echo """Metadata for ${metadataFile.path}:

Name      ${packageMetadata.Name}
Version   ${packageMetadata.Version}
"""
                return packageMetadata
            } finally {
                cleanWs(
                    deleteDirs: true,
                    patterns: [
                            [pattern: '*.dist-info/', type: 'INCLUDE'],
                        ]
                    )
            }
        }
    }
}
startup()
props = get_props()

pipeline {
    agent none
    parameters {
        booleanParam(name: "RUN_CHECKS", defaultValue: true, description: "Run checks on code")
        booleanParam(name: "TEST_RUN_TOX", defaultValue: false, description: "Run Tox Tests")
        booleanParam(name: "USE_SONARQUBE", defaultValue: defaultParameterValues.USE_SONARQUBE, description: "Send data test data to SonarQube")
        booleanParam(name: "BUILD_PACKAGES", defaultValue: false, description: "Build Python packages")
        booleanParam(name: 'TEST_PACKAGES', defaultValue: true, description: 'Test Python packages')
        booleanParam(name: 'BUILD_MAC_PACKAGES', defaultValue: false, description: 'Test Python packages on Mac')
        booleanParam(name: "DEPLOY_DEVPI", defaultValue: false, description: "Deploy to DevPi on https://devpi.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: "DEPLOY_DEVPI_PRODUCTION", defaultValue: false, description: "Deploy to https://devpi.library.illinois.edu/production/release")
        booleanParam(name: 'DEPLOY_PYPI', defaultValue: false, description: 'Deploy to pypi')
        booleanParam(name: "DEPLOY_DOCS", defaultValue: false, description: "Update online documentation")
    }
    stages {
        stage('Build') {
            stages {
                stage("Sphinx Documentation"){
                    agent{
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                        }
                    }
                    steps {
                        sh(
                            label: "Building docs",
                            script: '''mkdir -p logs
                                       python -m sphinx docs build/docs/html -d build/docs/.doctrees -w logs/build_sphinx.log
                                       '''
                            )
                    }
                    post{
                        always {
                            recordIssues(tools: [sphinxBuild(pattern: 'logs/build_sphinx.log')])
                            archiveArtifacts artifacts: 'logs/build_sphinx.log'
                        }
                        success{
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                            script{
                                zip(
                                    archive: true,
                                    dir: "${WORKSPACE}/build/docs/html",
                                    glob: '',
                                    zipFile: "dist/${props.Name}-${props.Version}.doc.zip"
                                )
                                stash(
                                    name: 'DOCS_ARCHIVE',
                                    includes: 'dist/*.doc.zip,build/docs/html/**'
                                )
                            }
                        }
                        cleanup{
                            cleanWs(
                                patterns: [
                                    [pattern: 'logs/', type: 'INCLUDE'],
                                    [pattern: "build/docs/", type: 'INCLUDE'],
                                    [pattern: "dist/", type: 'INCLUDE'],
                                    [pattern: '**/__pycache__', type: 'INCLUDE'],
                                ],
                                deleteDirs: true
                            )
                        }
                    }
                }
            }
        }
        stage("Checks"){
            when{
                equals expected: true, actual: params.RUN_CHECKS
            }
            stages{
                stage('Code Quality'){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                            args '--mount source=sonar-cache-uiucprescon-images,target=/home/user/.sonar/cache'
                        }
                    }
                    stages{
                        stage("Test") {
                            stages{
                                stage("Running Tests"){
                                    parallel {
                                        stage("Run PyTest Unit Tests"){
                                            steps{
                                                catchError(buildResult: 'UNSTABLE', message: 'PyTest found issues', stageResult: 'UNSTABLE') {
                                                    sh "coverage run --parallel-mode -m pytest --junitxml=reports/pytest/junit-pytest.xml"
                                                }
                                            }
                                            post {
                                                always {
                                                    junit "reports/pytest/junit-pytest.xml"
                                                    stash includes: "reports/pytest/*.xml", name: 'PYTEST_REPORT'
                                                }
                                            }
                                        }
                                        stage("Run Doctest Tests"){
                                            steps {
                                                catchError(buildResult: 'SUCCESS', message: 'DocTest found issues', stageResult: 'UNSTABLE') {
                                                    sh(label:"Running Doctest",
                                                       script: '''mkdir -p logs
                                                                  python -m sphinx -b doctest docs build/docs -d build/docs/doctrees -w logs/doctest.log
                                                        '''
                                                    )
                                                }
                                            }
                                            post{
                                                always {
                                                    archiveArtifacts artifacts: "logs/doctest.log"
                                                }
                                            }
                                        }
                                        stage("Run MyPy Static Analysis") {
                                            steps{
                                                catchError(buildResult: 'SUCCESS', message: 'MyPy found issues', stageResult: 'UNSTABLE') {
                                                    sh(label:"Running MyPy",
                                                       script: '''mkdir -p logs
                                                                  mypy -p uiucprescon --html-report reports/mypy/html | tee logs/mypy.log
                                                                  '''
                                                       )
                                               }
                                            }
                                            post {
                                                always {
                                                    archiveArtifacts "logs/mypy.log"
                                                    recordIssues(tools: [myPy(pattern: 'logs/mypy.log')])
                                                    publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy/html/', reportFiles: 'index.html', reportName: 'MyPy HTML Report', reportTitles: ''])
                                                }
                                            }
                                        }
                                        stage("Run Flake8 Static Analysis") {
                                            steps{
                                                catchError(buildResult: 'SUCCESS', message: 'Flake8 found issues', stageResult: 'UNSTABLE') {
                                                    sh(label:"Running Flake8",
                                                       script: '''mkdir -p logs
                                                                  flake8 uiucprescon --tee --output-file=logs/flake8.log
                                                               '''
                                                    )
                                                }
                                            }
                                            post {
                                                always {
                                                      archiveArtifacts 'logs/flake8.log'
                                                      recordIssues(tools: [flake8(pattern: 'logs/flake8.log')])
                                                      stash includes: "logs/flake8.log", name: 'FLAKE8_REPORT'
                                                }
                                            }
                                        }
                                        stage("Run Pylint Static Analysis") {
                                            steps{
                                                catchError(buildResult: 'SUCCESS', message: 'Pylint found issues', stageResult: 'UNSTABLE') {
                                                    tee('reports/pylint.txt'){
                                                        sh(label: "Running pylint",
                                                           script: '''mkdir -p reports
                                                                      pylint uiucprescon --persistent=n -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"
                                                                   '''
                                                        )
                                                    }
                                                    sh(
                                                        script: 'pylint uiucprescon --persistent=n  -r n --msg-template="{path}:{module}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports/pylint_issues.txt',
                                                        label: "Running pylint for sonarqube",
                                                        returnStatus: true
                                                    )
                                                }
                                            }
                                            post{
                                                always{
                                                    archiveArtifacts allowEmptyArchive: true, artifacts: "reports/pylint.txt"
                                                    recordIssues(tools: [pyLint(pattern: 'reports/pylint.txt')])
                                                    stash includes: "reports/pylint_issues.txt,reports/pylint.txt", name: 'PYLINT_REPORT'
                                                }
                                            }
                                        }
                                        stage("Run Bandit Static Analysis") {
                                            steps{
                                                catchError(buildResult: 'SUCCESS', message: 'Bandit found issues', stageResult: 'UNSTABLE') {
                                                    sh(
                                                        label: "Running bandit",
                                                        script: '''mkdir -p reports
                                                                   bandit --format json --output reports/bandit-report.json --recursive uiucprescon/images || bandit -f html --recursive uiucprescon/images --output reports/bandit-report.html
                                                                   '''
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
                                        stage('Task Scanner'){
                                            steps{
                                                recordIssues(tools: [taskScanner(highTags: 'FIXME', includePattern: 'uiucprescon/**/*.py', normalTags: 'TODO')])
                                            }
                                        }
                                        stage("pyDocStyle"){
                                            steps{
                                                catchError(buildResult: 'SUCCESS', message: 'Did not pass all pyDocStyle tests', stageResult: 'UNSTABLE') {

                                                    tee('reports/pydocstyle-report.txt'){
                                                        sh(
                                                            label: "Run pydocstyle",
                                                            script: 'pydocstyle uiucprescon'
                                                        )
                                                    }
                                                }
                                            }
                                            post {
                                                always{
                                                    recordIssues(tools: [pyDocStyle(pattern: 'reports/pydocstyle-report.txt')])
                                                }
                                            }
                                        }
                                    }
                                    post{
                                        always{
                                            sh "coverage combine && coverage xml -o reports/coverage.xml"
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
                                                    [pattern: 'reports/pytest/junit-*.xml', type: 'INCLUDE'],
                                                    [pattern: '.pytest_cache/', type: 'INCLUDE'],
                                                    [pattern: 'tox/**/*.log', type: 'INCLUDE'],
                                                    [pattern: '.mypy_cache/', type: 'INCLUDE'],
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
                        stage("Sonarcloud Analysis"){

                            options{
                                lock("uiucprescon.images-sonarscanner")
                                retry(3)
                            }
                            when{
                                equals expected: true, actual: params.USE_SONARQUBE
                                beforeAgent true
                                beforeOptions true
                            }
                            steps{
                                unstash "COVERAGE_REPORT"
                                unstash "PYTEST_REPORT"
                                unstash "BANDIT_REPORT"
                                unstash "PYLINT_REPORT"
                                unstash "FLAKE8_REPORT"
                                script{
                                    withSonarQubeEnv(installationName:"sonarcloud", credentialsId: 'sonarcloud-uiucprescon.images') {
                                        if (env.CHANGE_ID){
                                            sh(
                                                label: "Running Sonar Scanner",
                                                script:"sonar-scanner -Dsonar.projectVersion=${props.Version} -Dsonar.buildString=\"${env.BUILD_TAG}\" -Dsonar.pullrequest.key=${env.CHANGE_ID} -Dsonar.pullrequest.base=${env.CHANGE_TARGET}"
                                                )
                                        } else {
                                            sh(
                                                label: "Running Sonar Scanner",
                                                script: "sonar-scanner -Dsonar.projectVersion=${props.Version} -Dsonar.buildString=\"${env.BUILD_TAG}\" -Dsonar.branch.name=${env.BRANCH_NAME}"
                                                )
                                        }
                                    }
                                    timeout(time: 1, unit: 'HOURS') {
                                        def sonarqube_result = waitForQualityGate(abortPipeline: false)
                                        if (sonarqube_result.status != 'OK') {
                                            unstable "SonarQube quality gate: ${sonarqube_result.status}"
                                        }
                                        def outstandingIssues = get_sonarqube_unresolved_issues(".scannerwork/report-task.txt")
                                        writeJSON file: 'reports/sonar-report.json', json: outstandingIssues
                                    }
                                }
                            }
                            post {
                                always{
                                    archiveArtifacts(
                                        allowEmptyArchive: true,
                                        artifacts: ".scannerwork/report-task.txt"
                                    )
                                    script{
                                        if(fileExists('reports/sonar-report.json')){
                                            stash includes: "reports/sonar-report.json", name: 'SONAR_REPORT'
                                            archiveArtifacts allowEmptyArchive: true, artifacts: 'reports/sonar-report.json'
                                            recordIssues(tools: [sonarQube(pattern: 'reports/sonar-report.json')])
                                        }
                                    }
                                }
                                cleanup{
                                    cleanWs(
                                        deleteDirs: true,
                                        patterns: [
                                            [pattern: '.scannerwork/', type: 'INCLUDE'],
                                            [pattern: 'logs/', type: 'INCLUDE'],
                                            [pattern: "reports/", type: 'INCLUDE'],
                                            [pattern: "	uiucprescon.images.dist-info/", type: 'INCLUDE'],
                                        ]
                                    )
                                }
                            }
                        }
                    }
                }
                stage("Run Tox test") {
                    when {
                       equals expected: true, actual: params.TEST_RUN_TOX
                    }
                    steps {
                        script{
                            def tox
                            node(){
                                checkout scm
                                tox = load("ci/jenkins/scripts/tox.groovy")
                            }
                            def windowsJobs = [:]
                            def linuxJobs = [:]
                            stage("Scanning Tox Environments"){
                                parallel(
                                    "Linux":{
                                        linuxJobs = tox.getToxTestsParallel(
                                                envNamePrefix: "Tox Linux",
                                                label: "linux && docker",
                                                dockerfile: 'ci/docker/python/linux/tox/Dockerfile',
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                                            )
                                    },
                                    "Windows":{
                                        windowsJobs = tox.getToxTestsParallel(
                                                envNamePrefix: "Tox Windows",
                                                label: "windows && docker",
                                                dockerfile: 'ci/docker/python/windows/tox/Dockerfile',
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE'
                                         )
                                    },
                                    failFast: true
                                )
                            }
                            parallel(windowsJobs + linuxJobs)
                        }
                    }
                }
            }
        }
        stage("Distribution Packaging") {
            when{
                anyOf{
                    equals expected: true, actual: params.BUILD_PACKAGES
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
                }
                beforeAgent true
            }
            stages{
                stage("Building Wheel and sdist"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                        }
                    }
                    steps{
                        sh(
                            label: "Build Python packages",
                            script: "python -m build ."
                        )
                    }
                    post {
                        success {
                            archiveArtifacts artifacts: "dist/*.whl,dist/*.tar.gz,dist/*.zip", fingerprint: true
                            stash includes: "dist/*.whl,dist/*.tar.gz,dist/*.zip", name: 'PYTHON_PACKAGES'
                            stash includes: "dist/*.whl", name: 'wheel'
                            stash includes: "dist/*.tar.gz,dist/*.zip", name: 'sdist'

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
                stage('Testing Python Package'){
                    when{
                        equals expected: true, actual: params.TEST_PACKAGES
                    }
                    steps{
                        script{
                            def packages
                            node(){
                                checkout scm
                                packages = load 'ci/jenkins/scripts/packaging.groovy'
                            }
                            def windowsTests = [:]
                            SUPPORTED_WINDOWS_VERSIONS.each{ pythonVersion ->
                                windowsTests["Windows - Python ${pythonVersion}: sdist"] = {
                                    packages.testPkg(
                                        agent: [
                                            dockerfile: [
                                                label: 'windows && docker',
                                                filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE'
                                            ]
                                        ],
                                        glob: 'dist/*.tar.gz,dist/*.zip',
                                        stash: 'PYTHON_PACKAGES',
                                        pythonVersion: pythonVersion
                                    )
                                }
                                windowsTests["Windows - Python ${pythonVersion}: wheel"] = {
                                    packages.testPkg(
                                        agent: [
                                            dockerfile: [
                                                label: 'windows && docker',
                                                filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE'
                                            ]
                                        ],
                                        glob: 'dist/*.whl',
                                        stash: 'PYTHON_PACKAGES',
                                        pythonVersion: pythonVersion
                                    )
                                }
                            }
                            def linuxTests = [:]
                            SUPPORTED_LINUX_VERSIONS.each{ pythonVersion ->
                                linuxTests["Linux - Python ${pythonVersion}: sdist"] = {
                                    packages.testPkg(
                                        agent: [
                                            dockerfile: [
                                                label: 'linux && docker',
                                                filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                                            ]
                                        ],
                                        glob: 'dist/*.tar.gz',
                                        stash: 'PYTHON_PACKAGES',
                                        pythonVersion: pythonVersion
                                    )
                                }
                                linuxTests["Linux - Python ${pythonVersion}: wheel"] = {
                                    packages.testPkg(
                                        agent: [
                                            dockerfile: [
                                                label: 'linux && docker',
                                                filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                                            ]
                                        ],
                                        glob: 'dist/*.whl',
                                        stash: 'PYTHON_PACKAGES',
                                        pythonVersion: pythonVersion
                                    )
                                }
                            }
                            def tests = linuxTests + windowsTests
                            def macTests = [:]

                            SUPPORTED_MAC_VERSIONS.each{ pythonVersion ->
                                macTests["Mac - Python ${pythonVersion}: sdist"] = {
                                    withEnv(['QT_QPA_PLATFORM=offscreen']) {
                                        packages.testPkg(
                                            agent: [
                                                label: "mac && python${pythonVersion}",
                                            ],
                                            glob: 'dist/*.tar.gz,dist/*.zip',
                                            stash: 'PYTHON_PACKAGES',
                                            pythonVersion: pythonVersion,
                                            toxExec: 'venv/bin/tox',
                                            testSetup: {
                                                checkout scm
                                                unstash 'PYTHON_PACKAGES'
                                                sh(
                                                    label:'Install Tox',
                                                    script: '''python3 -m venv venv
                                                               venv/bin/pip install pip --upgrade
                                                               venv/bin/pip install tox
                                                               '''
                                                )
                                            },
                                            testTeardown: {
                                                sh 'rm -r venv/'
                                            }
                                        )
                                    }
                                }
                                macTests["Mac - Python ${pythonVersion}: wheel"] = {
                                    withEnv(['QT_QPA_PLATFORM=offscreen']) {
                                        packages.testPkg(
                                            agent: [
                                                label: "mac && python${pythonVersion}",
                                            ],
                                            glob: 'dist/*.whl',
                                            stash: 'PYTHON_PACKAGES',
                                            pythonVersion: pythonVersion,
                                            toxExec: 'venv/bin/tox',
                                            testSetup: {
                                                checkout scm
                                                unstash 'PYTHON_PACKAGES'
                                                sh(
                                                    label:'Install Tox',
                                                    script: '''python3 -m venv venv
                                                               venv/bin/pip install pip --upgrade
                                                               venv/bin/pip install tox
                                                               '''
                                                )
                                            },
                                            testTeardown: {
                                                sh 'rm -r venv/'
                                            }

                                        )
                                    }
                                }
                            }
                            if(params.TEST_PACKAGES_ON_MAC == true){
                                tests = tests + macTests
                            }
                            parallel(tests)
                        }
                    }
                }
            }
        }
        stage('Deploy to Devpi'){
            when {
                allOf{
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    anyOf {
                        equals expected: 'master', actual: env.BRANCH_NAME
                        equals expected: 'dev', actual: env.BRANCH_NAME
                        tag '*'
                    }
                }
                beforeAgent true
            }
            agent none
            options{
                lock('uiucprescon.images-devpi')
            }
            stages{
                stage('Deploy to Devpi Staging') {
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/tox/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                          }
                    }
                    options{
                        retry(3)
                    }
                    steps {
                        timeout(5){
                            unstash 'DOCS_ARCHIVE'
                            script{
                                unstash 'PYTHON_PACKAGES'
                                def devpi = load('ci/jenkins/scripts/devpi.groovy')
                                devpi.upload(
                                    server: DEVPI_CONFIG.server,
                                    credentialsId: DEVPI_CONFIG.credentialsId,
                                    index: DEVPI_CONFIG.stagingIndex,
                                )
                            }
                        }
                    }
                    post{
                        cleanup{
                            cleanWs(
                                deleteDirs: true,
                                patterns: [
                                        [pattern: 'dist/', type: 'INCLUDE']
                                    ]
                            )
                        }
                    }
                }
                stage('Test DevPi Packages') {
                    steps{
                        script{
                            def devpi
                            node(''){
                                checkout scm
                                devpi = load('ci/jenkins/scripts/devpi.groovy')
                            }
                            def macPackages = [:]
                            SUPPORTED_MAC_VERSIONS.each{pythonVersion ->
                                macPackages["MacOS - Python ${pythonVersion}: wheel"] = {
                                    devpi.testDevpiPackage(
                                        agent: [
                                            label: "mac && python${pythonVersion}"
                                        ],
                                        devpi: [
                                            index: DEVPI_CONFIG.stagingIndex,
                                            server: DEVPI_CONFIG.server,
                                            credentialsId: DEVPI_CONFIG.credentialsId,
                                            devpiExec: 'venv/bin/devpi'
                                        ],
                                        package:[
                                            name: props.Name,
                                            version: props.Version,
                                            selector: 'whl'
                                        ],
                                        test:[
                                            setup: {
                                                sh(
                                                    label:'Installing Devpi client',
                                                    script: '''python3 -m venv venv
                                                                venv/bin/python -m pip install pip --upgrade
                                                                venv/bin/python -m pip install devpi_client
                                                                '''
                                                )
                                            },
                                            toxEnv: "py${pythonVersion}".replace('.',''),
                                            teardown: {
                                                sh( label: 'Remove Devpi client', script: 'rm -r venv')
                                            }
                                        ]
                                    )
                                }
                                macPackages["MacOS - Python ${pythonVersion}: sdist"]= {
                                    devpi.testDevpiPackage(
                                        agent: [
                                            label: "mac && python${pythonVersion}"
                                        ],
                                        devpi: [
                                            index: DEVPI_CONFIG.stagingIndex,
                                            server: DEVPI_CONFIG.server,
                                            credentialsId: DEVPI_CONFIG.credentialsId,
                                            devpiExec: 'venv/bin/devpi'
                                        ],
                                        package:[
                                            name: props.Name,
                                            version: props.Version,
                                            selector: 'tar.gz'
                                        ],
                                        test:[
                                            setup: {
                                                sh(
                                                    label:'Installing Devpi client',
                                                    script: '''python3 -m venv venv
                                                                venv/bin/python -m pip install pip --upgrade
                                                                venv/bin/python -m pip install devpi_client
                                                                '''
                                                )
                                            },
                                            toxEnv: "py${pythonVersion}".replace('.',''),
                                            teardown: {
                                                sh( label: 'Remove Devpi client', script: 'rm -r venv')
                                            }
                                        ]
                                    )
                                }
                            }
                            def windowsPackages = [:]
                            SUPPORTED_WINDOWS_VERSIONS.each{pythonVersion ->
                                windowsPackages["Windows - Python ${pythonVersion}: sdist"] = {
                                    devpi.testDevpiPackage(
                                        agent: [
                                            dockerfile: [
                                                filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE',
                                                label: 'windows && docker'
                                            ]
                                        ],
                                        dockerImageName:  "${currentBuild.fullProjectName}_devpi_with_msvc".replaceAll('-', '_').replaceAll('/', '_').replaceAll(' ', '').toLowerCase(),
                                        devpi: [
                                            index: DEVPI_CONFIG.stagingIndex,
                                            server: DEVPI_CONFIG.server,
                                            credentialsId: DEVPI_CONFIG.credentialsId,
                                        ],
                                        package:[
                                            name: props.Name,
                                            version: props.Version,
                                            selector: 'tar.gz'
                                        ],
                                        test:[
                                            toxEnv: "py${pythonVersion}".replace('.',''),
                                        ]
                                    )
                                }
                                windowsPackages["Test Python ${pythonVersion}: wheel Windows"] = {
                                    devpi.testDevpiPackage(
                                        agent: [
                                            dockerfile: [
                                                filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE',
                                                label: 'windows && docker'
                                            ]
                                        ],
                                        devpi: [
                                            index: DEVPI_CONFIG.stagingIndex,
                                            server: DEVPI_CONFIG.server,
                                            credentialsId: DEVPI_CONFIG.credentialsId,
                                        ],
                                        dockerImageName:  "${currentBuild.fullProjectName}_devpi_without_msvc".replaceAll('-', '_').replaceAll('/', '_').replaceAll(' ', '').toLowerCase(),
                                        package:[
                                            name: props.Name,
                                            version: props.Version,
                                            selector: 'whl'
                                        ],
                                        test:[
                                            toxEnv: "py${pythonVersion}".replace('.',''),
                                        ]
                                    )
                                }
                            }
                            def linuxPackages = [:]
                            SUPPORTED_LINUX_VERSIONS.each{pythonVersion ->
                                linuxPackages["Linux - Python ${pythonVersion}: sdist"] = {
                                    devpi.testDevpiPackage(
                                        agent: [
                                            dockerfile: [
                                                filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL',
                                                label: 'linux && docker'
                                            ]
                                        ],
                                        devpi: [
                                            index: DEVPI_CONFIG.stagingIndex,
                                            server: DEVPI_CONFIG.server,
                                            credentialsId: DEVPI_CONFIG.credentialsId,
                                        ],
                                        package:[
                                            name: props.Name,
                                            version: props.Version,
                                            selector: 'tar.gz'
                                        ],
                                        test:[
                                            toxEnv: "py${pythonVersion}".replace('.',''),
                                        ]
                                    )
                                }
                                linuxPackages["Linux - Python ${pythonVersion}: wheel"] = {
                                    devpi.testDevpiPackage(
                                        agent: [
                                            dockerfile: [
                                                filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL',
                                                label: 'linux && docker'
                                            ]
                                        ],
                                        devpi: [
                                            index: DEVPI_CONFIG.stagingIndex,
                                            server: DEVPI_CONFIG.server,
                                            credentialsId: DEVPI_CONFIG.credentialsId,
                                        ],
                                        package:[
                                            name: props.Name,
                                            version: props.Version,
                                            selector: 'whl'
                                        ],
                                        test:[
                                            toxEnv: "py${pythonVersion}".replace('.',''),
                                        ]
                                    )
                                }
                            }
                            def devpiPackagesTesting = windowsPackages + linuxPackages
                            if (params.BUILD_MAC_PACKAGES){
                                 devpiPackagesTesting = devpiPackagesTesting + macPackages
                            }

                            parallel(devpiPackagesTesting)
                        }
                    }
                }
                stage('Deploy to DevPi Production') {
                    when {
                        allOf{
                            equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
                            anyOf {
                                branch 'master'
                                tag '*'
                            }
                        }
                        beforeAgent true
                        beforeInput true
                    }
                    options{
                      timeout(time: 1, unit: 'DAYS')
                    }
                    input {
                      message 'Release to DevPi Production?'
                    }
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/tox/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                        }
                    }
                    steps {
                        script{
                            checkout scm
                            devpi = load 'ci/jenkins/scripts/devpi.groovy'
                            echo "Pushing to production/release index"
                            devpi.pushPackageToIndex(
                                pkgName: props.Name,
                                pkgVersion: props.Version,
                                server: DEVPI_CONFIG.server,
                                indexSource: "DS_Jenkins/${DEVPI_CONFIG.stagingIndex}",
                                indexDestination: 'production/release',
                                credentialsId: DEVPI_CONFIG.credentialsId
                            )
                        }
                    }
                }
            }
            post{
                success{
                    node('linux && docker') {
                        script{
                            if (!env.TAG_NAME?.trim()){
                                checkout scm
                                devpi = load 'ci/jenkins/scripts/devpi.groovy'
                                docker.build('uiucprescon.images:devpi','-f ./ci/docker/python/linux/tox/Dockerfile --build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL .').inside{
                                    devpi.pushPackageToIndex(
                                        pkgName: props.Name,
                                        pkgVersion: props.Version,
                                        server: DEVPI_CONFIG.server,
                                        indexSource: "DS_Jenkins/${DEVPI_CONFIG.stagingIndex}",
                                        indexDestination: "DS_Jenkins/${env.BRANCH_NAME}",
                                        credentialsId: DEVPI_CONFIG.credentialsId
                                    )
                                }
                            }
                        }
                    }
                }
                cleanup{
                    node('linux && docker') {
                        script{
                            checkout scm
                            devpi = load 'ci/jenkins/scripts/devpi.groovy'
                            docker.build('uiucprescon.images:devpi','-f ./ci/docker/python/linux/tox/Dockerfile --build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL .').inside{
                                devpi.removePackage(
                                    pkgName: props.Name,
                                    pkgVersion: props.Version,
                                    index: "DS_Jenkins/${DEVPI_CONFIG.stagingIndex}",
                                    server: DEVPI_CONFIG.server,
                                    credentialsId: DEVPI_CONFIG.credentialsId,

                                )
                            }
                        }
                    }
                }
            }
        }
        stage("Deploy"){
            parallel {
                stage('Deploy to pypi') {
                    agent{
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                        }
                    }
                    when{
                         allOf{
                            equals expected: true, actual: params.DEPLOY_PYPI
                            equals expected: true, actual: params.BUILD_PACKAGES

                        }
                        beforeAgent true
                        beforeInput true
                    }
                    options{
                        retry(3)
                    }
                    input {
                        message 'Upload to pypi server?'
                        parameters {
                            choice(
                                choices: PYPI_SERVERS,
                                description: 'Url to the pypi index to upload python packages.',
                                name: 'SERVER_URL'
                            )
                        }
                    }
                    steps{
                        unstash 'PYTHON_PACKAGES'
                        script{
                            def pypi = fileLoader.fromGit(
                                    'pypi',
                                    'https://github.com/UIUCLibrary/jenkins_helper_scripts.git',
                                    '2',
                                    null,
                                    ''
                                )
                            pypi.pypiUpload(
                                credentialsId: 'jenkins-nexus',
                                repositoryUrl: SERVER_URL,
                                glob: 'dist/*'
                                )
                        }
                    }
                    post{
                        cleanup{
                            cleanWs(
                                deleteDirs: true,
                                patterns: [
                                        [pattern: 'dist/', type: 'INCLUDE']
                                    ]
                            )
                        }
                    }
                }
                stage("Deploy Online Documentation") {
                    agent any
                    when{
                        equals expected: true, actual: params.DEPLOY_DOCS
                        beforeAgent true
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
                                        remoteDirectory: props.Name,
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

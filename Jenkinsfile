#!groovy
@Library(["devpi", "PythonHelpers"]) _


def CONFIGURATIONS = [
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
                            filename: 'ci/docker/python/linux/Dockerfile',
                            label: 'linux&&docker',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ],
                    test: [
                        dockerfile: [
                            filename: 'ci/docker/python/linux/Dockerfile',
                            label: 'linux&&docker',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ],
                    devpi: [
                        dockerfile: [
                            filename: 'ci/docker/python/linux/Dockerfile',
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
                            filename: 'ci/docker/python/linux/Dockerfile',
                            label: 'linux&&docker',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ],
                    test: [
                        dockerfile: [
                            filename: 'ci/docker/python/linux/Dockerfile',
                            label: 'linux&&docker',
                            additionalBuildArgs: '--build-arg PYTHON_VERSION=3.8 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        ]
                    ],
                    devpi: [
                        dockerfile: [
                            filename: 'ci/docker/python/linux/Dockerfile',
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
    options {
        buildDiscarder logRotator(artifactDaysToKeepStr: '10', artifactNumToKeepStr: '10')
        preserveStashes(buildCount: 5)
    }
    parameters {
        booleanParam(name: "RUN_CHECKS", defaultValue: true, description: "Run checks on code")
        booleanParam(name: "TEST_RUN_TOX", defaultValue: false, description: "Run Tox Tests")
        booleanParam(name: "USE_SONARQUBE", defaultValue: true, description: "Send data test data to SonarQube")
        booleanParam(name: "BUILD_PACKAGES", defaultValue: false, description: "Build Python packages")
        booleanParam(name: "DEPLOY_DEVPI", defaultValue: false, description: "Deploy to DevPi on https://devpi.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: "DEPLOY_DEVPI_PRODUCTION", defaultValue: false, description: "Deploy to https://devpi.library.illinois.edu/production/release")
        booleanParam(name: "DEPLOY_ADD_TAG", defaultValue: false, description: "Tag commit to current version")
        booleanParam(name: "DEPLOY_DOCS", defaultValue: false, description: "Update online documentation")
    }

    stages {
        stage("Getting Distribution Info"){
            agent {
                dockerfile {
                    filename 'ci/docker/python/linux/Dockerfile'
                    label 'linux && docker'
                    additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                 }
            }
            steps{
                sh "python setup.py dist_info"
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
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                         }
                    }
                    steps {
                        sh "python setup.py build -b build"
                    }
                }
                stage("Sphinx Documentation"){
                    agent{
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        }
                    }
                    environment{
                        PKG_NAME = get_package_name("DIST-INFO", "uiucprescon.images.dist-info/METADATA")
                        PKG_VERSION = get_package_version("DIST-INFO", "uiucprescon.images.dist-info/METADATA")
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
        stage("Checks"){
            when{
                equals expected: true, actual: params.RUN_CHECKS
            }
            stages{
                stage("Test") {
                    agent{
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        }
                    }
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
                                stage("Run Tox test") {
                                    when{
                                        equals expected: true, actual: params.TEST_RUN_TOX
                                    }
                                    steps {
                                          sh "tox --workdir tox -e py"
                                    }
                                    post {
                                        always {
                                            recordIssues(tools: [pep8(id: 'tox', name: 'Tox', pattern: '.tox/**/*.log')])
                                            archiveArtifacts artifacts: "tox/**/*.log", allowEmptyArchive: true
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
                                            sh(label: "Running pylint",
                                               script: '''mkdir -p reports
                                                          pylint uiucprescon  -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports/pylint.txt
                                                       '''

                                            )
                                            sh(
                                                script: 'pylint uiucprescon  -r n --msg-template="{path}:{module}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports/pylint_issues.txt',
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
                            }
                            post{
                                always{
                                    sh "coverage combine && coverage xml -o reports/coverage.xml && coverage html -d reports/coverage"
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
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                            args '--mount source=sonar-cache-uiucprescon-images,target=/home/user/.sonar/cache'
                        }
                    }
                    options{
                        lock("uiucprescon.images-sonarscanner")
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
                                unstash "DIST-INFO"
                                def props = readProperties(interpolate: true, file: "uiucprescon.images.dist-info/METADATA")
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
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        }
                    }
                    steps{
                        sh(
                            label: "Build Python packages",
                            script: "python -m pep517.build ."
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
                stage("Testing Packages"){
                    options{
                        timestamps()
                    }
                    matrix{
                        axes {
                            axis {
                                name 'PYTHON_VERSION'
                                values(
                                    '3.8',
                                    '3.7'
                                )
                            }
                            axis {
                                name 'PLATFORM'
                                values(
                                    "windows",
                                    "linux"
                                )
                            }
                        }
                        environment{
                            TOXENV="py${PYTHON_VERSION}".replaceAll('\\.', '')
                        }
                        stages{
                            stage("Testing wheel Packages"){
                                agent {
                                    dockerfile {
                                        filename "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.test.dockerfile.filename}"
                                        label "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.test.dockerfile.label}"
                                        additionalBuildArgs "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.test.dockerfile.additionalBuildArgs}"
                                     }
                                }
                                options {
                                    warnError('Testing Package failed')
                                }
                                steps{
                                    cleanWs(
                                        notFailBuild: true,
                                        deleteDirs: true,
                                        disableDeferredWipeout: true,
                                        patterns: [
                                                [pattern: '.git/**', type: 'EXCLUDE'],
                                                [pattern: 'tests/**', type: 'EXCLUDE'],
                                                [pattern: 'tox.ini', type: 'EXCLUDE'],
                                            ]
                                    )
                                    unstash "wheel"
                                    script{
                                        findFiles( glob: 'dist/**/*.whl').each{
                                            if(isUnix()){
                                                sh(
                                                    label: "Testing ${it}",
                                                    script: "tox --installpkg=${it.path} -vv"
                                                )
                                            } else {
                                                bat(
                                                    label: "Testing ${it}",
                                                    script: "tox --installpkg=${it.path} -vv"
                                                )
                                            }
                                        }
                                    }
                                }
                                post{
                                    unsuccessful {
                                        archiveArtifacts artifacts: ".tox/**/*.log"
                                    }
                                    cleanup{
                                        cleanWs(
                                            notFailBuild: true,
                                            deleteDirs: true,
                                            patterns: [
                                                    [pattern: 'dist', type: 'INCLUDE'],
                                                    [pattern: '**/__pycache__', type: 'INCLUDE'],
                                                    [pattern: 'build', type: 'INCLUDE'],
                                                    [pattern: '.tox', type: 'INCLUDE'],
                                                ]
                                        )
                                    }
                                }
                            }
                            stage("Testing sdist Packages"){
                                agent {
                                    dockerfile {
                                        filename "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.test.dockerfile.filename}"
                                        label "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.test.dockerfile.label}"
                                        additionalBuildArgs "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.test.dockerfile.additionalBuildArgs}"
                                     }
                                }
                                options {
                                    warnError('Testing Package failed')
                                }
                                steps{
                                    cleanWs(
                                        notFailBuild: true,
                                        deleteDirs: true,
                                        disableDeferredWipeout: true,
                                        patterns: [
                                                [pattern: '.git/**', type: 'EXCLUDE'],
                                                [pattern: 'tests/**', type: 'EXCLUDE'],
                                                [pattern: 'tox.ini', type: 'EXCLUDE'],
                                            ]
                                    )
                                    unstash "sdist"
                                    script{
                                        findFiles( glob: 'dist/*.tar.gz,dist/*.zip').each{
                                            if(isUnix()){
                                                sh(
                                                    label: "Testing ${it}",
                                                    script: "tox --installpkg=${it.path} -v"
                                                    )
                                            } else {
                                                bat(
                                                    label: "Testing ${it}",
                                                    script: "tox --installpkg=${it.path} -v"
                                                )
                                            }
                                        }
                                    }
                                }
                                post{
                                    unsuccessful {
                                        archiveArtifacts artifacts: ".tox/**/log/*.log"
                                    }
                                    cleanup{
                                        cleanWs(
                                            notFailBuild: true,
                                            deleteDirs: true,
                                            patterns: [
                                                    [pattern: 'dist', type: 'INCLUDE'],
                                                    [pattern: '**/__pycache__', type: 'INCLUDE'],
                                                    [pattern: 'build', type: 'INCLUDE'],
                                                    [pattern: '.tox', type: 'INCLUDE'],
                                                ]
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        stage("Deploy to Devpi"){
            when {
                allOf{
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    anyOf {
                        equals expected: "master", actual: env.BRANCH_NAME
                        equals expected: "dev", actual: env.BRANCH_NAME
                    }
                }
                beforeAgent true
                beforeOptions true
            }
            agent none
            environment{
                DEVPI = credentials("DS_devpi")
            }
            options{
                lock("uiucprescon.images-devpi")
            }
            stages{
                stage("Deploy to Devpi Staging") {
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                          }
                    }
                    steps {
                        timeout(5){
                            unstash "wheel"
                            unstash "sdist"
                            unstash "DOCS_ARCHIVE"
                            sh(
                                label: "Connecting to DevPi Server",
                                script: '''devpi use https://devpi.library.illinois.edu --clientdir ./devpi
                                           devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ./devpi
                                        '''
                            )
                            sh(
                                label: "Uploading to DevPi Staging",
                                script: """devpi use /${env.DEVPI_USR}/${env.BRANCH_NAME}_staging --clientdir ./devpi
                                           devpi upload --from-dir dist --clientdir ./devpi"""
                            )
                        }
                    }
                }
                stage("Test DevPi packages") {
                    matrix {
                        axes {
                            axis {
                                name 'PYTHON_VERSION'
                                values '3.7', '3.8'
                            }
                            axis {
                                name 'FORMAT'
                                values "wheel", 'sdist'
                            }
                            axis {
                                name 'PLATFORM'
                                values(
                                    "windows",
                                    "linux"
                                )
                            }
                        }
                        excludes{
                             exclude {
                                 axis {
                                     name 'PLATFORM'
                                     values 'linux'
                                 }
                                 axis {
                                     name 'FORMAT'
                                     values 'wheel'
                                 }
                             }
                        }
                        agent none
                        stages{
                            stage("Testing DevPi Package"){
                                agent {
                                  dockerfile {
                                    filename "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.devpi.dockerfile.filename}"
                                    additionalBuildArgs "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.devpi.dockerfile.additionalBuildArgs}"
                                    label "${CONFIGURATIONS[PYTHON_VERSION].os[PLATFORM].agents.devpi.dockerfile.label}"
                                  }
                                }
                                steps{
                                    unstash "DIST-INFO"
                                    script{
                                        def props = readProperties interpolate: true, file: "uiucprescon.images.dist-info/METADATA"

                                        if(isUnix()){
                                            sh(
                                                label: "Running tests on DevPi",
                                                script: """python --version
                                                           devpi use https://devpi.library.illinois.edu --clientdir certs
                                                           devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir certs
                                                           devpi use ${env.BRANCH_NAME}_staging --clientdir certs
                                                           devpi test --index ${env.BRANCH_NAME}_staging ${props.Name}==${props.Version} -s ${CONFIGURATIONS[PYTHON_VERSION].devpiSelector[FORMAT]} --clientdir certs -e ${CONFIGURATIONS[PYTHON_VERSION].tox_env} -v
                                                       """
                                            )
                                        } else {
                                            bat(
                                                label: "Running tests on DevPi",
                                                script: """python --version
                                                           devpi use https://devpi.library.illinois.edu --clientdir certs\\
                                                           devpi login %DEVPI_USR% --password %DEVPI_PSW% --clientdir certs\\
                                                           devpi use ${env.BRANCH_NAME}_staging --clientdir certs\\
                                                           devpi test --index ${env.BRANCH_NAME}_staging ${props.Name}==${props.Version} -s ${CONFIGURATIONS[PYTHON_VERSION].devpiSelector[FORMAT]} --clientdir certs\\ -e ${CONFIGURATIONS[PYTHON_VERSION].tox_env} -v
                                                           """
                                            )
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                stage("Deploy to DevPi Production") {
                    when {
                        allOf{
                            equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
                            branch "master"
                        }
                        beforeAgent true
                    }
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux&&docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        }
                    }
                    steps {
                        script {
                            unstash "DIST-INFO"
                            def props = readProperties interpolate: true, file: 'uiucprescon.images.dist-info/METADATA'
                            try{
                                timeout(30) {
                                    input "Release ${props.Name} ${props.Version} (https://devpi.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}_staging/${props.Name}/${props.Version}) to DevPi Production? "
                                }
                                sh "devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi  && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi && devpi use /DS_Jenkins/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi && devpi push --index ${env.DEVPI_USR}/${env.BRANCH_NAME}_staging ${props.Name}==${props.Version} production/release --clientdir ${WORKSPACE}/devpi"
                            } catch(err){
                                echo "User response timed out. Packages not deployed to DevPi Production."
                            }
                        }
                    }
                }
            }
            post{
                success{
                    node('linux && docker') {
                        checkout scm
                        script{
                            docker.build("uiucprescon.images:devpi",'-f ./ci/docker/python/linux/Dockerfile --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .').inside{
                                unstash "DIST-INFO"
                                def props = readProperties interpolate: true, file: 'uiucprescon.images.dist-info/METADATA'
                                sh(
                                    label: "Connecting to DevPi Server",
                                    script: 'devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi'
                                )
                                sh "devpi use /DS_Jenkins/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi"
                                sh "devpi push ${props.Name}==${props.Version} DS_Jenkins/${env.BRANCH_NAME} --clientdir ${WORKSPACE}/devpi"
                            }
                        }
                    }
                }
                cleanup{
                    node('linux && docker') {
                       script{
                            docker.build("uiucprescon.images:devpi",'-f ./ci/docker/python/linux/Dockerfile --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .').inside{
                                unstash "DIST-INFO"
                                def props = readProperties interpolate: true, file: 'uiucprescon.images.dist-info/METADATA'
                                sh(
                                    label: "Connecting to DevPi Server",
                                    script: 'devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi'
                                )
                                sh "devpi use /DS_Jenkins/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi"
                                sh "devpi remove -y ${props.Name}==${props.Version} --clientdir ${WORKSPACE}/devpi"
                            }
                       }
                    }
                }
            }
        }
        stage("Deploy"){
            parallel {
                stage("Tagging git Commit"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/Dockerfile'
                            label 'linux && docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                        }
                    }
                    when{
                        allOf{
                            equals expected: true, actual: params.DEPLOY_ADD_TAG
                        }
                        beforeAgent true
                        beforeInput true
                    }
                    options{
                        timeout(time: 1, unit: 'DAYS')
                        retry(3)
                    }
                    input {
                          message 'Add a version tag to git commit?'
                          parameters {
                                credentials credentialType: 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl', defaultValue: 'github.com', description: '', name: 'gitCreds', required: true
                          }
                    }
                    steps{
                        unstash "DIST-INFO"
                        script{
                            def props = readProperties interpolate: true, file: "uiucprescon.images.dist-info/METADATA"
                            def commitTag = input message: 'git commit', parameters: [string(defaultValue: "v${props.Version}", description: 'Version to use a a git tag', name: 'Tag', trim: false)]
                            withCredentials([usernamePassword(credentialsId: gitCreds, passwordVariable: 'password', usernameVariable: 'username')]) {
                                sh(label: "Tagging ${commitTag}",
                                   script: """git config --local credential.helper "!f() { echo username=\\$username; echo password=\\$password; }; f"
                                              git tag -a ${commitTag} -m 'Tagged by Jenkins'
                                              git push origin --tags
                                           """
                                )
                            }
                        }
                    }
                    post{
                        cleanup{
                            deleteDir()
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

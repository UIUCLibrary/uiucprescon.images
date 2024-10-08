library identifier: 'JenkinsPythonHelperLibrary@2024.1.2', retriever: modernSCM(
  [$class: 'GitSCMSource',
   remote: 'https://github.com/UIUCLibrary/JenkinsPythonHelperLibrary.git',
   ])


SUPPORTED_MAC_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']
SUPPORTED_LINUX_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']
SUPPORTED_WINDOWS_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']


def getPypiConfig() {
    node(){
        configFileProvider([configFile(fileId: 'pypi_config', variable: 'CONFIG_FILE')]) {
            def config = readJSON( file: CONFIG_FILE)
            return config['deployment']['indexes']
        }
    }
}
def parseBanditReport(htmlReport){
    script {
        try{
            def summary = createSummary icon: 'warning.gif', text: 'Bandit Security Issues Detected'
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
        def response = httpRequest url : props['serverUrl'] + "/api/issues/search?componentKeys=" + props['projectKey'] + '&resolved=no'
        def outstandingIssues = readJSON text: response.content
        return outstandingIssues
    }
}
def testPythonPackages(){
    script{
        def windowsTests = [:]
        if(params.INCLUDE_WINDOWS_X86_64 == true){
            SUPPORTED_WINDOWS_VERSIONS.each{ pythonVersion ->
                windowsTests["Windows - Python ${pythonVersion}: sdist"] = {
                    testPythonPkg(
                        agent: [
                            dockerfile: [
                                label: 'windows && docker',
                                filename: 'ci/docker/python/windows/tox/Dockerfile',
                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE'
                            ]
                        ],
                        retries: 3,
                        testSetup: {
                            checkout scm
                            unstash 'PYTHON_PACKAGES'
                        },
                        testCommand: {
                            findFiles(glob: 'dist/*.tar.gz').each{
                                bat(label: 'Running Tox', script: "tox --workdir %TEMP%\\tox --installpkg ${it.path} -e py${pythonVersion.replace('.', '')} -v")
                            }
                        },
                        post:[
                            cleanup: {
                                cleanWs(
                                    patterns: [
                                        [pattern: 'dist/', type: 'INCLUDE'],
                                        [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                    ],
                                    notFailBuild: true,
                                    deleteDirs: true
                                )
                            },
                        ]
                    )
                }
                windowsTests["Windows - Python ${pythonVersion}: wheel"] = {
                    testPythonPkg(
                        agent: [
                            dockerfile: [
                                label: 'windows && docker',
                                filename: 'ci/docker/python/windows/tox/Dockerfile',
                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE'
                            ]
                        ],
                        retries: 3,
                        testSetup: {
                             checkout scm
                             unstash 'PYTHON_PACKAGES'
                        },
                        testCommand: {
                             findFiles(glob: 'dist/*.whl').each{
                                 powershell(label: 'Running Tox', script: "tox --installpkg ${it.path} --workdir \$env:TEMP\\tox  -e py${pythonVersion.replace('.', '')}")
                             }

                        },
                        post:[
                            cleanup: {
                                cleanWs(
                                    patterns: [
                                            [pattern: 'dist/', type: 'INCLUDE'],
                                            [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                        ],
                                    notFailBuild: true,
                                    deleteDirs: true
                                )
                            },
                            success: {
                                archiveArtifacts artifacts: 'dist/*.whl'
                            }
                        ]
                    )
                }
            }
        }
        def linuxTests = [:]
        SUPPORTED_LINUX_VERSIONS.each{ pythonVersion ->
            def linuxArchitectures = []
            if(params.INCLUDE_LINUX_X86_64 == true){
                linuxArchitectures.add('x86_64')
            }
            if(params.INCLUDE_LINUX_ARM == true){
                linuxArchitectures.add('arm64')
            }
            linuxArchitectures.each{arch ->
                linuxTests["Linux ${arch} - Python ${pythonVersion}: sdist"] = {
                    testPythonPkg(
                        agent: [
                            dockerfile: [
                                label: "linux && docker && ${arch}",
                                filename: 'ci/docker/python/linux/tox/Dockerfile',
                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                args: '-v pipcache_packagevalidate:/.cache/pip',
                            ]
                        ],
                        retries: 3,
                        testSetup: {
                            checkout scm
                            unstash 'PYTHON_PACKAGES'
                        },
                        testCommand: {
                            findFiles(glob: 'dist/*.tar.gz').each{
                                sh(
                                    label: 'Running Tox',
                                    script: "tox --installpkg ${it.path} --workdir /tmp/tox -e py${pythonVersion.replace('.', '')}"
                                    )
                            }
                        },
                        post:[
                            cleanup: {
                                cleanWs(
                                    patterns: [
                                            [pattern: 'dist/', type: 'INCLUDE'],
                                            [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                        ],
                                    notFailBuild: true,
                                    deleteDirs: true
                                )
                            },
                        ]
                    )
                }
                linuxTests["Linux ${arch} - Python ${pythonVersion}: wheel"] = {
                    testPythonPkg(
                        agent: [
                            dockerfile: [
                                label: "linux && docker && ${arch}",
                                filename: 'ci/docker/python/linux/tox/Dockerfile',
                                additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                args: '-v pipcache_packagevalidate:/.cache/pip',
                            ]
                        ],
                        testSetup: {
                            checkout scm
                            unstash 'PYTHON_PACKAGES'
                        },
                        retries: 3,
                        testCommand: {
                            findFiles(glob: 'dist/*.whl').each{
                                timeout(5){
                                    sh(
                                        label: 'Running Tox',
                                        script: "tox --installpkg ${it.path} --workdir /tmp/tox -e py${pythonVersion.replace('.', '')}"
                                        )
                                }
                            }
                        },
                        post:[
                            cleanup: {
                                cleanWs(
                                    patterns: [
                                            [pattern: 'dist/', type: 'INCLUDE'],
                                            [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                        ],
                                    notFailBuild: true,
                                    deleteDirs: true
                                )
                            },
                            success: {
                                archiveArtifacts artifacts: 'dist/*.whl'
                            },
                        ]
                    )
                }
            }
        }
        def macTests = [:]
        SUPPORTED_MAC_VERSIONS.each{ pythonVersion ->
            def macArchitectures = []
            if(params.INCLUDE_MACOS_X86_64 == true){
                macArchitectures.add('x86_64')
            }
            if(params.INCLUDE_MACOS_ARM == true){
                macArchitectures.add('m1')
            }
            macArchitectures.each{ processorArchitecture ->
                if (nodesByLabel("mac && ${processorArchitecture} && python${pythonVersion}").size() > 0){
                    macTests["Mac ${processorArchitecture} - Python ${pythonVersion}: sdist"] = {
                        testPythonPkg(
                            agent: [
                                label: "mac && python${pythonVersion} && ${processorArchitecture}",
                            ],
                            testSetup: {
                                checkout scm
                                unstash 'PYTHON_PACKAGES'
                            },
                            testCommand: {
                                findFiles(glob: 'dist/*.tar.gz').each{
                                    sh(label: 'Running Tox',
                                       script: """python${pythonVersion} -m venv venv
                                       ./venv/bin/python -m pip install --upgrade pip
                                       ./venv/bin/pip install -r requirements/requirements_tox.txt
                                       ./venv/bin/tox --installpkg ${it.path} -e py${pythonVersion.replace('.', '')}"""
                                    )
                                }

                            },
                            post:[
                                cleanup: {
                                    cleanWs(
                                        patterns: [
                                                [pattern: 'dist/', type: 'INCLUDE'],
                                                [pattern: 'venv/', type: 'INCLUDE'],
                                                [pattern: '.tox/', type: 'INCLUDE'],
                                            ],
                                        notFailBuild: true,
                                        deleteDirs: true
                                    )
                                },
                            ]
                        )
                    }
                    macTests["Mac ${processorArchitecture} - Python ${pythonVersion}: wheel"] = {
                        testPythonPkg(
                            agent: [
                                label: "mac && python${pythonVersion} && ${processorArchitecture}",
                            ],
                            retries: 3,
                            testCommand: {
                                unstash 'PYTHON_PACKAGES'
                                findFiles(glob: 'dist/*.whl').each{
                                    sh(label: 'Running Tox',
                                       script: """python${pythonVersion} -m venv venv
                                                  . ./venv/bin/activate
                                                  python -m pip install --upgrade pip
                                                  pip install -r requirements/requirements_tox.txt
                                                  tox --installpkg ${it.path} -e py${pythonVersion.replace('.', '')}
                                               """
                                    )
                                }
                            },
                            post:[
                                cleanup: {
                                    cleanWs(
                                        patterns: [
                                                [pattern: 'dist/', type: 'INCLUDE'],
                                                [pattern: 'venv/', type: 'INCLUDE'],
                                                [pattern: '.tox/', type: 'INCLUDE'],
                                            ],
                                        notFailBuild: true,
                                        deleteDirs: true
                                    )
                                },
                                success: {
                                     archiveArtifacts artifacts: 'dist/*.whl'
                                }
                            ]
                        )
                    }
                }
            }
        }
        parallel(linuxTests + windowsTests + macTests)
    }
}

def startup(){
    parallel(
        [
            failFast: true,
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
        booleanParam(name: 'RUN_CHECKS', defaultValue: true, description: 'Run checks on code')
        booleanParam(name: 'TEST_RUN_TOX', defaultValue: false, description: 'Run Tox Tests')
        booleanParam(name: 'USE_SONARQUBE', defaultValue: true, description: 'Send data test data to SonarQube')
        credentials(name: 'SONARCLOUD_TOKEN', credentialType: 'org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl', defaultValue: 'sonarcloud_token', required: false)
        booleanParam(name: 'BUILD_PACKAGES', defaultValue: false, description: 'Build Python packages')

        booleanParam(name: 'INCLUDE_LINUX_ARM', defaultValue: false, description: 'Include ARM architecture for Linux')
        booleanParam(name: 'INCLUDE_LINUX_X86_64', defaultValue: true, description: 'Include x86_64 architecture for Linux')
        booleanParam(name: 'INCLUDE_MACOS_ARM', defaultValue: false, description: 'Include ARM(m1) architecture for Mac')
        booleanParam(name: 'INCLUDE_MACOS_X86_64', defaultValue: false, description: 'Include x86_64 architecture for Mac')
        booleanParam(name: 'INCLUDE_WINDOWS_X86_64', defaultValue: true, description: 'Include x86_64 architecture for Windows')

        booleanParam(name: 'TEST_PACKAGES', defaultValue: true, description: 'Test Python packages')
        booleanParam(name: 'DEPLOY_PYPI', defaultValue: false, description: 'Deploy to pypi')
        booleanParam(name: 'DEPLOY_DOCS', defaultValue: false, description: 'Update online documentation')
    }
    options {
        retry(conditions: [agent()], count: 2)
    }
    stages {
        stage('Building and Testing'){
            when{
                anyOf{
                    equals expected: true, actual: params.RUN_CHECKS
                    equals expected: true, actual: params.TEST_RUN_TOX
                }
            }
            stages{
                stage('Build') {
                    when{
                        anyOf{
                            equals expected: true, actual: params.RUN_CHECKS
                        }
                        beforeAgent true
                    }
                    stages {
                        stage('Sphinx Documentation'){
                            agent{
                                dockerfile {
                                    filename 'ci/docker/python/linux/jenkins/Dockerfile'
                                    label 'linux && docker && x86'
                                    additionalBuildArgs '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                                }
                            }
                            steps {
                                catchError(buildResult: 'UNSTABLE', message: 'Building documentation produced an error or a warning', stageResult: 'UNSTABLE') {
                                    sh(
                                        label: 'Building docs',
                                        script: '''mkdir -p logs
                                                   python -m sphinx docs build/docs/html -d build/docs/.doctrees -w logs/build_sphinx.log -W --keep-going
                                                   '''
                                        )
                                }
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
                                            [pattern: 'build/docs/', type: 'INCLUDE'],
                                            [pattern: 'dist/', type: 'INCLUDE'],
                                            [pattern: '**/__pycache__', type: 'INCLUDE'],
                                        ],
                                        deleteDirs: true
                                    )
                                }
                            }
                        }
                    }
                }
                stage('Checks'){
                    when{
                        equals expected: true, actual: params.RUN_CHECKS
                    }
                    stages{
                        stage('Code Quality'){
                            agent {
                                dockerfile {
                                    filename 'ci/docker/python/linux/jenkins/Dockerfile'
                                    label 'linux && docker && x86'
                                    additionalBuildArgs '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                                    args '--mount source=sonar-cache-uiucprescon-images,target=/home/user/.sonar/cache'
                                }
                            }
                            options {
                              retry(conditions: [agent()], count: 3)
                            }
                            stages{
                                stage('Test') {
                                    stages{
                                        stage('Running Tests'){
                                            parallel {
                                                stage('Run PyTest Unit Tests'){
                                                    steps{
                                                        catchError(buildResult: 'UNSTABLE', message: 'PyTest found issues', stageResult: 'UNSTABLE') {
                                                            sh 'coverage run --parallel-mode -m pytest --junitxml=reports/pytest/junit-pytest.xml'
                                                        }
                                                    }
                                                    post {
                                                        always {
                                                            junit 'reports/pytest/junit-pytest.xml'
                                                        }
                                                    }
                                                }
                                                stage('Run Doctest Tests'){
                                                    steps {
                                                        catchError(buildResult: 'SUCCESS', message: 'DocTest found issues', stageResult: 'UNSTABLE') {
                                                            sh(label:'Running Doctest',
                                                               script: '''mkdir -p logs
                                                                          python -m sphinx -b doctest docs build/docs -d build/docs/doctrees -w logs/doctest.log
                                                                '''
                                                            )
                                                        }
                                                    }
                                                    post{
                                                        always {
                                                            archiveArtifacts artifacts: 'logs/doctest.log'
                                                        }
                                                    }
                                                }
                                                stage('Run MyPy Static Analysis') {
                                                    steps{
                                                        catchError(buildResult: 'SUCCESS', message: 'MyPy found issues', stageResult: 'UNSTABLE') {
                                                            sh(label:'Running MyPy',
                                                               script: '''mkdir -p logs
                                                                          mypy -p uiucprescon --html-report reports/mypy/html | tee logs/mypy.log
                                                                          '''
                                                               )
                                                       }
                                                    }
                                                    post {
                                                        always {
                                                            archiveArtifacts 'logs/mypy.log'
                                                            recordIssues(tools: [myPy(pattern: 'logs/mypy.log')])
                                                            publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy/html/', reportFiles: 'index.html', reportName: 'MyPy HTML Report', reportTitles: ''])
                                                        }
                                                    }
                                                }
                                                stage('Run Flake8 Static Analysis') {
                                                    steps{
                                                        catchError(buildResult: 'SUCCESS', message: 'Flake8 found issues', stageResult: 'UNSTABLE') {
                                                            sh(label:'Running Flake8',
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
                                                        }
                                                    }
                                                }
                                                stage('Run Pylint Static Analysis') {
                                                    steps{
                                                        catchError(buildResult: 'SUCCESS', message: 'Pylint found issues', stageResult: 'UNSTABLE') {
                                                            tee('reports/pylint.txt'){
                                                                sh(label: 'Running pylint',
                                                                   script: '''mkdir -p reports
                                                                              pylint uiucprescon --persistent=n -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"
                                                                           '''
                                                                )
                                                            }
                                                            sh(
                                                                script: 'pylint uiucprescon --persistent=n  -r n --msg-template="{path}:{module}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports/pylint_issues.txt',
                                                                label: 'Running pylint for sonarqube',
                                                                returnStatus: true
                                                            )
                                                        }
                                                    }
                                                    post{
                                                        always{
                                                            archiveArtifacts allowEmptyArchive: true, artifacts: 'reports/pylint.txt'
                                                            recordIssues(tools: [pyLint(pattern: 'reports/pylint.txt')])
                                                        }
                                                    }
                                                }
                                                stage('Run Bandit Static Analysis') {
                                                    steps{
                                                        catchError(buildResult: 'SUCCESS', message: 'Bandit found issues', stageResult: 'UNSTABLE') {
                                                            sh(
                                                                label: 'Running bandit',
                                                                script: '''mkdir -p reports
                                                                           bandit --format json --output reports/bandit-report.json --recursive uiucprescon/images || bandit -f html --recursive uiucprescon/images --output reports/bandit-report.html
                                                                           '''
                                                            )
                                                        }
                                                    }
                                                    post {
                                                        always {
                                                            archiveArtifacts 'reports/bandit-report.json,reports/bandit-report.html'
                                                        }
                                                        unstable{
                                                            script{
                                                                if(fileExists('reports/bandit-report.html')){
                                                                    parseBanditReport('reports/bandit-report.html')
                                                                    addWarningBadge text: 'Bandit security issues detected', link: "${currentBuild.absoluteUrl}"
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
                                                stage('pyDocStyle'){
                                                    steps{
                                                        catchError(buildResult: 'SUCCESS', message: 'Did not pass all pyDocStyle tests', stageResult: 'UNSTABLE') {

                                                            tee('reports/pydocstyle-report.txt'){
                                                                sh(
                                                                    label: 'Run pydocstyle',
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
                                                    sh 'coverage combine && coverage xml -o reports/coverage.xml'
                                                    recordCoverage(tools: [[parser: 'COBERTURA', pattern: 'reports/coverage.xml']])
                                                    archiveArtifacts 'reports/coverage.xml'
                                                }
                                            }
                                        }
                                    }
                                }
                                stage('Sonarcloud Analysis'){

                                    options{
                                        lock('uiucprescon.images-sonarscanner')
                                        retry(3)
                                    }
                                    when{
                                        allOf{
                                            equals expected: true, actual: params.USE_SONARQUBE
                                            expression{
                                                try{
                                                    withCredentials([string(credentialsId: params.SONARCLOUD_TOKEN, variable: 'dddd')]) {
                                                        echo 'Found credentials for sonarqube'
                                                    }
                                                } catch(e){
                                                    return false
                                                }
                                                return true
                                            }
                                        }
                                    }
                                    steps{
                                        script{
                                            withSonarQubeEnv(installationName:'sonarcloud', credentialsId: params.SONARCLOUD_TOKEN) {
                                                if (env.CHANGE_ID){
                                                    sh(
                                                        label: 'Running Sonar Scanner',
                                                        script:"sonar-scanner -Dsonar.projectVersion=${props.Version} -Dsonar.buildString=\"${env.BUILD_TAG}\" -Dsonar.pullrequest.key=${env.CHANGE_ID} -Dsonar.pullrequest.base=${env.CHANGE_TARGET}"
                                                        )
                                                } else {
                                                    sh(
                                                        label: 'Running Sonar Scanner',
                                                        script: "sonar-scanner -Dsonar.projectVersion=${props.Version} -Dsonar.buildString=\"${env.BUILD_TAG}\" -Dsonar.branch.name=${env.BRANCH_NAME}"
                                                        )
                                                }
                                            }
                                            timeout(time: 1, unit: 'HOURS') {
                                                def sonarqube_result = waitForQualityGate(abortPipeline: false)
                                                if (sonarqube_result.status != 'OK') {
                                                    unstable "SonarQube quality gate: ${sonarqube_result.status}"
                                                }
                                                def outstandingIssues = get_sonarqube_unresolved_issues('.scannerwork/report-task.txt')
                                                writeJSON file: 'reports/sonar-report.json', json: outstandingIssues
                                            }
                                        }
                                    }
                                    post {
                                        always{
                                            archiveArtifacts(
                                                allowEmptyArchive: true,
                                                artifacts: '.scannerwork/report-task.txt'
                                            )
                                            script{
                                                if(fileExists('reports/sonar-report.json')){
                                                    archiveArtifacts allowEmptyArchive: true, artifacts: 'reports/sonar-report.json'
                                                    recordIssues(tools: [sonarQube(pattern: 'reports/sonar-report.json')])
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                            post{
                                cleanup{
                                    cleanWs(
                                        patterns: [
                                            [pattern: 'dist/', type: 'INCLUDE'],
                                            [pattern: 'venv/', type: 'INCLUDE'],
                                            [pattern: '.tox/', type: 'INCLUDE'],
                                            [pattern: 'build/', type: 'INCLUDE'],
                                            [pattern: 'coverage-sources.zip', type: 'INCLUDE'],
                                            [pattern: 'logs/', type: 'INCLUDE'],
                                            [pattern: 'reports/', type: 'INCLUDE'],
                                            [pattern: '*.egg-info/', type: 'INCLUDE'],
                                            [pattern: '.pytest_cache/', type: 'INCLUDE'],
                                            [pattern: '.scannerwork/', type: 'INCLUDE'],
                                            [pattern: 'logs/', type: 'INCLUDE'],
                                            [pattern: 'reports/', type: 'INCLUDE'],
                                            [pattern: '*.dist-info/', type: 'INCLUDE'],
                                            [pattern: '.mypy_cache/', type: 'INCLUDE'],
                                        ],
                                        deleteDirs: true,
                                    )
                                }
                            }
                        }
                    }
                }
                stage('Run Tox test') {
                    when {
                       equals expected: true, actual: params.TEST_RUN_TOX
                    }
                    steps {
                        script{
                            def windowsJobs = [:]
                            def linuxJobs = [:]
                            stage('Scanning Tox Environments'){
                                parallel(
                                    'Linux':{
                                        linuxJobs = getToxTestsParallel(
                                                envNamePrefix: 'Tox Linux',
                                                label: 'linux && docker && x86',
                                                dockerfile: 'ci/docker/python/linux/tox/Dockerfile',
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL',
                                                retry: 3
                                            )
                                    },
                                    'Windows':{
                                        windowsJobs = getToxTestsParallel(
                                                envNamePrefix: 'Tox Windows',
                                                label: 'windows && docker && x86',
                                                dockerfile: 'ci/docker/python/windows/tox/Dockerfile',
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE',
                                                retry: 2
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
        stage('Distribution Packaging') {
            when{
                equals expected: true, actual: params.BUILD_PACKAGES
                beforeAgent true
            }
            stages{
                stage('Building Source and Wheel formats'){
                    agent {
                        docker{
                            image 'python'
                            label 'linux && docker'
                          }
                    }
                    steps{
                        timeout(5){
                            withEnv(['PIP_NO_CACHE_DIR=off']) {
                                sh(label: 'Build Python Package',
                                   script: '''python -m venv venv --upgrade-deps
                                              . ./venv/bin/activate
                                              pip install build
                                              python -m build .
                                              '''
                                    )
                            }
                        }
                    }
                    post{
                        success{
                            archiveArtifacts artifacts: 'dist/*.whl,dist/*.tar.gz,dist/*.zip', fingerprint: true
                            stash includes: 'dist/*.whl,dist/*.tar.gz,dist/*.zip', name: 'PYTHON_PACKAGES'
                            stash includes: 'dist/*.whl', name: 'wheel'
                            stash includes: 'dist/*.tar.gz,dist/*.zip', name: 'sdist'
                        }
                        cleanup{
                            cleanWs(
                                deleteDirs: true,
                                patterns: [
                                    [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                    [pattern: 'venv/', type: 'INCLUDE'],
                                    [pattern: 'dist/', type: 'INCLUDE']
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
                        testPythonPackages()
                    }
                }
            }
        }
        stage('Deploy'){
            parallel {
                stage('Deploy to pypi') {
                    agent{
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux && docker && x86'
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
                                choices: getPypiConfig(),
                                description: 'Url to the pypi index to upload python packages.',
                                name: 'SERVER_URL'
                            )
                        }
                    }
                    steps{
                        unstash 'PYTHON_PACKAGES'
                        pypiUpload(
                            credentialsId: 'jenkins-nexus',
                            repositoryUrl: SERVER_URL,
                            glob: 'dist/*'
                        )
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
                 stage('Deploy Online Documentation') {
                    when{
                        equals expected: true, actual: params.DEPLOY_DOCS
                        beforeAgent true
                        beforeInput true
                    }
                    agent{
                        dockerfile {
                            filename 'ci/docker/python/linux/jenkins/Dockerfile'
                            label 'linux && docker && x86'
                            additionalBuildArgs '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'
                        }
                    }
                    options{
                        timeout(time: 1, unit: 'DAYS')
                    }
                    input{
                        message 'Update project documentation?'
                    }
                    steps{
                        unstash 'DOCS_ARCHIVE'
                        withCredentials([usernamePassword(credentialsId: 'dccdocs-server', passwordVariable: 'docsPassword', usernameVariable: 'docsUsername')]) {
                            sh 'python utils/upload_docs.py --username=$docsUsername --password=$docsPassword --subroute=uiucprescon.images build/docs/html apache-ns.library.illinois.edu'
                        }
                    }
                    post{
                        cleanup{
                            cleanWs(
                                deleteDirs: true,
                                patterns: [
                                    [pattern: 'build/', type: 'INCLUDE'],
                                    [pattern: 'dist/', type: 'INCLUDE'],
                                ]
                            )
                        }
                    }
                }
            }
        }
    }
}

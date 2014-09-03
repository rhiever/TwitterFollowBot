#!/bin/bash

THIS_SCRIPT=$(readlink -f $0)
THIS_DIR=$(dirname ${THIS_SCRIPT})

DATE_NOW=$(date +%Y-%m-%d_%H-%M-%S)
LOG_DIR=${THIS_DIR}/log

function setup_log_output {
    mkdir -p ${LOG_DIR}
    LOG_FILE=${LOG_DIR}/${DATE_NOW}.log
    ln -sf ${LOG_FILE} ${LOG_DIR}/latest
}

function setup_virtualenv {
    VENV_DIR=${THIS_DIR}/venv

    if [ ! -d "${VENV_DIR}" ]; then
        if [ -s "${THIS_DIR}/.python_version" ]; then
            virtualenv ${VENV_DIR} -p "$(cat ${THIS_DIR}/.python_version)" >> ${LOG_FILE}
        else
            virtualenv ${VENV_DIR} >> ${LOG_FILE}
        fi
    fi
    source ${THIS_DIR}/venv/bin/activate
}

function install_dependencies {
    pip install -r ${THIS_DIR}/requirements.txt >> ${LOG_FILE}
}

function source_settings_and_credentials {
    for ENV_FILE in settings.sh credentials.sh
    do
        if [ -s "${THIS_DIR}/${ENV_FILE}" ]; then
            source "${THIS_DIR}/${ENV_FILE}"
        fi
    done
}

function delete_old_logs {
    find ${LOG_DIR} -type f -iname '*.log' -mtime +30 -delete
}

function run_main_code {
    export PYTHONIOENCODING="utf-8"
    command=${THIS_DIR}/main.py
    # Line buffering, see http://unix.stackexchange.com/a/25378
    stdbuf -oL -eL run-one ${command} >> ${LOG_FILE} 2>&1
    RETCODE=$?
    if [ ${RETCODE} != 0 ]; then
        echo "$@ exited with code: ${RETCODE}"
        git remote -v
        tail -v -n 100 ${LOG_FILE}
        exit 2
    fi

    grep -n '^ERROR:' ${LOG_FILE}
}

setup_log_output
setup_virtualenv
install_dependencies
source_settings_and_credentials
run_main_code
delete_old_logs

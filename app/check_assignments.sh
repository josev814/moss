#!/bin/bash
# Sets the maximum number of times a given passage may appear before it is ignored.
MOSS_THRESHOLD="10"


# Define the script file and the checksum file
SCRIPT_FILE="$0"

# Calculate the current checksum of the script
SET_CHECKSUM=$(md5sum "$SCRIPT_FILE" | awk '{ print $1 }')
echo "Base Checksum: ${SET_CHECKSUM}"

# Activate the Python virtual environment
source /pyvenv/bin/activate

BASE_DIR='/assignments'
cd ${BASE_DIR}
while true
do
    current_checksum=$(md5sum "${SCRIPT_FILE}" | awk '{ print $1 }')
    if [[ "${SET_CHECKSUM}" != "$current_checksum" ]]
    then
        echo "script updated....exiting"
        exit
    fi

    for code_type in $(ls -A)
    do
        # skipping files in assignments directory
        # we only process directories
        if [[ -f "${code_type}" ]]
        then
            continue
        fi

        for assignment in $(ls -A "${code_type}")
        do
            cur_path="${BASE_DIR}/${code_type}/${assignment}"
            result_file="${cur_path}/moss_m${MOSS_THRESHOLD}.results"
            if [[ -f "${result_file}" ]]
            then
                #already tested
                echo "Skipping: ${cur_path}"
                continue
            fi
            entries=$(ls -A "${cur_path}" | awk -v base="${cur_path}" '{print base "/" $0}' | tr '\n' ' ')
            if [[ ${#entries} -eq 0 ]]
            then
                echo "Nothing to test in ${cur_path}"
                continue
            fi
            echo "Processing: ${cur_path}"
            echo "CMD: perl /app/moss.pl -l $code_type ${entries} > ${result_file}"
            perl /app/moss.pl -m ${MOSS_THRESHOLD} -l $code_type ${entries} > "${result_file}"
            result_html=$(grep -i -e '^http:' "${result_file}")
            if [[ -n "${result_html}" ]]
            then
                echo "Downloading Results"
                html_file="${cur_path}/moss_m${MOSS_THRESHOLD}.html"
                curl -L -o "${html_file}" "${result_html}"
                if [[ $? -eq 0 ]]
                then
                    echo '##### Downloaded HTML results #####'
                    echo "Open ${html_file} to view the results"
                    echo '##### Converting results to CSV #####'
                    python /app/html_result_to_csv.py
                    if [[ $? -eq 0 ]]
                    then
                        echo '##### Converted results to CSV #####'
                    fi
                fi
            fi
        done
    done
    sleep 60
done

#!./bin/python3

# EXPERIMENTAL
# Used for fully automated way of running powermetrics and local video files.

import os
import subprocess
import time

def main():
    start_time = time.time()
    print("Starting at = ", time.ctime(start_time))
    directory_path = os.getcwd()
    benchmarkFolder = "benchmarks"
    benchmarksPath = directory_path + '/' + benchmarkFolder
    benchmarkList = os.listdir(benchmarksPath)

    # Don't need hidden files in the list
    if '.DS_Store' in benchmarkList:
        benchmarkList.remove('.DS_Store')


    for benchmark in benchmarkList:

        outputFile = directory_path + '/powerLogs/' + benchmark + '.txt'

        cmd = "sudo powermetrics -i 100 --samplers cpu_power,gpu_power -a --hide-cpu-duty-cycle --show-usage-summary --show-extra-power-info -u " + outputFile
        pr = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print("Process spawned with PID: %s" % pr.pid)
        pgid = os.getpgid(pr.pid)
        print("Process spawned with Group ID: %s" % pgid)

        time.sleep(60)

        cmd = benchmarksPath + '/' + benchmark
        p = subprocess.run(cmd.split(), shell=False, check=True, capture_output=True, text=True)

        time.sleep(60)

        # Kill the powermetrics process
        os.system("sudo pkill -u root powermetrics")


    end_time = time.time()
    print("Ending at = ", time.ctime(end_time))
    print(f"It took {end_time-start_time:.2f} seconds to compute")


if __name__ == "__main__":
    main()

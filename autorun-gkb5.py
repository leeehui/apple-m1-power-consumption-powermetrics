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
    gkb5 = "/Users/abc/Downloads/Geekbench5.app/Contents/Resources/geekbench_aarch64"
    sections = {"single-core":1, "multi-core":2} # 1: single core 2: multi core
    workloads = [101, 201, 202, 203, 204, 205, 206, 207, 208, 209, 301, 302, 303, 305, 306, 307, 308, 309, 310, 312, 313] 
    sleep_time = 60
    iterations  = 200
    passwd = "tgb*963.1"
    
    for section, section_val in sections.items():
        for workload in workloads:
            print(f"running gkb{workload} {section} ...")
            outputFile = directory_path + '/powerLogs/' + str(workload) + "-" + section + '.txt'
            cmd = f"echo {passwd} | sudo -S powermetrics -i 100 --samplers cpu_power,gpu_power -a --hide-cpu-duty-cycle --show-usage-summary --show-extra-power-info -u {outputFile}"
            pr = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            print("Process spawned with PID: %s" % pr.pid)
            pgid = os.getpgid(pr.pid)
            print("Process spawned with Group ID: %s" % pgid)

            time.sleep(sleep_time)

            cmd = gkb5 + f" --section {section_val} --workload {workload} --no-upload --iteration=1"
            p = subprocess.run(cmd.split(), shell=False, check=True, capture_output=True, text=True)

            time.sleep(sleep_time)

            # Kill the powermetrics process
            os.system(f"echo {passwd} | sudo -S pkill -u root powermetrics")


    end_time = time.time()
    print("Ending at = ", time.ctime(end_time))
    print(f"It took {end_time-start_time:.2f} seconds to compute")


if __name__ == "__main__":
    main()

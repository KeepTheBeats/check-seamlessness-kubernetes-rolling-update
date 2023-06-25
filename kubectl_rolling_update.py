import os
import sys
import datetime
import csv
import subprocess

import common


def main():
    if len(sys.argv) < 4:
        print(
            "This program needs:\n (1) Deployment name as the first input parameter.\n (2) Namespace name as the second input parameter.\n (3) Node name as the third input parameter."
        )
        return

    deployName = sys.argv[1]
    nsName = sys.argv[2]
    nodeName = sys.argv[3]

    patchCmd = '''kubectl patch deployment {} -n {} --type strategic --patch '{{"spec": {{"template": {{"spec": {{"nodeName": "{}" }} }} }} }}' '''.format(
        deployName, nsName, nodeName)

    timeBefore = datetime.datetime.now()
    os.system(patchCmd)
    while True:
        podNum = subprocess.run(
            "kubectl get pod -o wide | grep {} | wc -l".format(deployName),
            shell=True,
            capture_output=True,
            text=True)
        print("Number of pods:", podNum.stdout)

        newRunningPodNum = subprocess.run(
            "kubectl get pod -o wide | grep {} | grep {} | grep Running | grep \"1/1\" | wc -l"
            .format(deployName, nodeName),
            shell=True,
            capture_output=True,
            text=True)
        print("Number of new running pods:", newRunningPodNum.stdout)

        if int(podNum.stdout) == 1 and int(newRunningPodNum.stdout) == 1:
            print("update finished")
            break

    timeAfter = datetime.datetime.now()

    with open(common.updateFileName, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile, delimiter=",")
        writer.writerow([str(timeBefore), str(timeAfter)])


if __name__ == '__main__':
    main()

import sys
import requests
import datetime
import csv

import common


# write data to csv file
def writeCsv(timeBefores, timeDiffs):
    # newline='' to avoid extra blank lines on Windows OS
    with open(common.checkFileName, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile, delimiter=",")
        for i in range(len(timeBefores)):
            writer.writerow([str(timeBefores[i]), timeDiffs[i]])


def main():
    if len(sys.argv) < 3:
        print(
            "This program needs:\n (1) the URL of the service to be checked as the first input parameter.\n (2) the expected HTTP status code as the second input parameter."
        )
        return

    svcUrl = sys.argv[1]
    expectedCode = int(sys.argv[2])

    timeBefores = []
    timeDiffs = []

    errDiff = common.errMark

    print("Start to check the service with URL: {}".format(svcUrl))
    try:
        # the program will check the service without any interval until receiving "Ctrl+C".
        while True:
            timeBefore = datetime.datetime.now()
            try:
                response = requests.get(svcUrl)
                timeAfter = datetime.datetime.now()
                timeDiff = (timeAfter - timeBefore).total_seconds()

                if response.status_code != expectedCode:
                    print(
                        "Error HTTP status code: {}\nresponse content: {}\nwe record the response time as {} seconds"
                        .format(response.status_code, response.text, errDiff))
                    timeDiff = errDiff

                print("Access at: {}, response time: {} seconds".format(
                    timeBefore, timeDiff))
                timeBefores.append(timeBefore)
                timeDiffs.append(timeDiff)

            except Exception as e:
                print("Access exception:", e)
                print("we record the response time as {} seconds".format(
                    errDiff))
                timeDiffs.append(errDiff)
    except KeyboardInterrupt as e:
        print("Ctrl+C received:", e)

    # write data into CSV file
    writeCsv(timeBefores, timeDiffs)


if __name__ == "__main__":
    main()

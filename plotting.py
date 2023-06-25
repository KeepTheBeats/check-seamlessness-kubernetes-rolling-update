import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import common


# read data from csv file
def readCsv():
    timeBefores = []
    timeDiffs = []
    with open(common.checkFileName, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=",")
        for row in reader:
            timeBefore = datetime.datetime.strptime(row[0],
                                                    "%Y-%m-%d %H:%M:%S.%f")
            timeDiff = float(row[1])
            timeBefores.append(timeBefore)
            timeDiffs.append(timeDiff)

    with open(common.updateFileName, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=",")
        row = next(reader)
        updateStartTime = datetime.datetime.strptime(row[0],
                                                     "%Y-%m-%d %H:%M:%S.%f")
        updateFinishTime = datetime.datetime.strptime(row[1],
                                                      "%Y-%m-%d %H:%M:%S.%f")

    return timeBefores, timeDiffs, updateStartTime, updateFinishTime


def plotResults(timeBefores, timeDiffs, updateStartTime, updateFinishTime):
    fig, ax = plt.subplots()

    # If we want to better use date time as the X values, we should use this mdates.date2num to convert it.
    formattedTimeBefores = mdates.date2num(timeBefores)

    ax.scatter(formattedTimeBefores, timeDiffs, marker='*', s=5, zorder=5)
    # ax.plot(timeBefores, timeDiffs)

    # configure the format of the date time on the x labels
    formatter = mdates.DateFormatter('%H:%M:%S.%f')
    ax.xaxis.set_major_formatter(formatter)

    # make the x ticks denser
    locator = mdates.AutoDateLocator()
    locator.intervald[mdates.SECONDLY] = [1]  # every second one tick
    ax.xaxis.set_major_locator(locator)

    ax.set_title('Response Time')
    ax.set_xlabel('Request Time Point')
    ax.set_ylabel('Response Time (s)')

    ax.grid(axis='y', linestyle='--')

    # # avoid the x label overlapped.
    fig.autofmt_xdate()

    # mark the update start time and update end time
    formattedUpdateStartTime = mdates.date2num(updateStartTime)
    formattedUpdateFinishTime = mdates.date2num(updateFinishTime)

    ax.axvline(x=formattedUpdateStartTime,
               color='blue',
               linestyle='--',
               zorder=1)
    ax.text(formattedUpdateStartTime,
            0.01,
            'Update Start',
            color='blue',
            ha='right')
    ax.axvline(x=formattedUpdateFinishTime,
               color='blue',
               linestyle='--',
               zorder=1)
    ax.text(formattedUpdateFinishTime,
            0.01,
            'Update Finish',
            color='blue',
            ha='left')

    # mark the value that service is unaccessible
    ax.axhline(y=common.errMark,
               color='red',
               linestyle='--',
               linewidth=1,
               zorder=1)
    ax.text(x=formattedTimeBefores[0],
            y=common.errMark,
            s='This value {} means that the service is unaccessible.'.format(
                common.errMark),
            color='red',
            ha='left')

    plt.show()


def main():
    timeBefores, timeDiffs, updateStartTime, updateFinishTime = readCsv()
    plotResults(timeBefores, timeDiffs, updateStartTime, updateFinishTime)


if __name__ == '__main__':
    main()

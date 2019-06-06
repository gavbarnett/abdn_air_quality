import matplotlib.pyplot as plt 
import math, json, argparse
from collections import OrderedDict
from datetime import datetime

aparser = argparse.ArgumentParser(description='Plot Luftdaten data from json')
aparser.add_argument(
    '-s', '--sensor', dest='sensor', action='store',
    help='s, format: 12345')
args = aparser.parse_args()

def main():
    json_file = './data/big_dump/'
    if (args.sensor): 
        sensor = args.sensor
    else:
        sensor = '13084'
    
    json_file = json_file + sensor + '.json'
    with open(json_file, "r") as f:
        d = json.load(f, object_pairs_hook=OrderedDict)
    humidity = []
    timestamp_h = []
    temperature = []
    timestamp_t = []
    P1 = []
    timestamp_P1 = []
    P2 = []
    timestamp_P2 = []
    P1P2 = []
    timestamp_P1P2 = []
    old_i = 0
    all_time = []
    for i in d[sensor]["readings"]:
        all_time.append(int(i))
    all_time.sort()
    for t in all_time:
        if ("humidity" in d[sensor]["readings"][str(t)]) and ("P2" in d[sensor]["readings"][str(t)]) and ("P1" in d[sensor]["readings"][str(t)]):
            humidity.append(d[sensor]["readings"][str(t)]["humidity"])
            temperature.append(d[sensor]["readings"][str(t)]["temperature"])
            P1.append(d[sensor]["readings"][str(t)]["P1"])
            P2.append(d[sensor]["readings"][str(t)]["P2"])
            timestamp_h.append(datetime.utcfromtimestamp(t))
        
    
    plt.figure(1)
    typeOfP1 = list(d[sensor]["info"]["P1"])[0]
    typeofHumidity = list(d[sensor]["info"]["humidity"])[0]
    plt.suptitle("LocationID[" + sensor + "]_" + typeOfP1 + "[" + d[sensor]["info"]["P1"][typeOfP1]+"]_" + typeofHumidity + "[" + d[sensor]["info"]["humidity"][typeofHumidity]+"]")
    plt.subplot(321)
    plt.plot(humidity, P1, 'ro', ms=1, alpha=.1, label='P1')
    #plt.plot(humidity, P2, 'bo', ms=1, alpha=.1, label='P2')    
    plt.yscale('log')
    plt.xscale('linear')
    axes = plt.gca()
    axes.set_xlim([0,100])
    axes.set_ylim([0.1,1000])
    plt.ylabel('PM (ug/m^3)')
    plt.xlabel('Rel. Humidity (%)')
    plt.legend()

    plt.subplot(322)
    plt.plot(humidity, P2, 'bo', ms=1, alpha=.1, label='P2')
    #plt.plot(temperature, P1, 'ro', ms=1, alpha=.1, label='P1')
    #plt.plot(temperature, P2, 'bo', ms=1, alpha=.1, label='P2')
    plt.yscale('log')
    plt.xscale('linear')
    axes = plt.gca()
    axes.set_xlim([0,100])
    axes.set_ylim([0.1,1000])
    plt.ylabel('PM (ug/m^3)')
    plt.xlabel('Rel. Humidity (%)')
    plt.legend()

    plt.subplot(323)
    plt.plot(humidity, temperature, 'ro', ms=1, alpha=.1)
    plt.yscale('linear')
    plt.xscale('linear')
    axes = plt.gca()
    axes.set_xlim([0,100])
    axes.set_ylim([-30,30])
    plt.ylabel('Temperature (C)')
    plt.xlabel('Rel. Humidity (%)')

    plt.subplot(324)
    plt.plot(P1, P2, 'go', ms=1, alpha=.1)
    plt.yscale('log')
    plt.xscale('log')
    axes = plt.gca()
    axes.set_xlim([0.1,1000])
    axes.set_ylim([0.1,1000])
    plt.ylabel('P1 (ug/m^3)')
    plt.xlabel('P2 (ug/m^3)')

    plt.subplot(325)
    plt.plot(timestamp_h, humidity, 'go', ms=1, alpha=.1)
    plt.plot(timestamp_h, humidity, 'go', ms=1, alpha=.1)
    plt.yscale('linear')
    #plt.xscale('linear')
    axes = plt.gca()
    axes.set_ylim([0,100])
    for tick in axes.get_xticklabels():
        tick.set_rotation(45)
    import matplotlib.dates as mdates
    plt.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.ylabel('Rel. Humidity (%)')
    plt.xlabel('Time')

    plt.subplot(326)
    plt.plot(timestamp_h, P1, 'go', ms=1, alpha=.1)
    plt.yscale('log')
    #plt.xscale('linear')
    axes = plt.gca()
    axes.set_ylim([0.1,1000])
    for tick in axes.get_xticklabels():
        tick.set_rotation(45)
    plt.ylabel('P1 (ug/m^3)')
    plt.xlabel('Time')
    
    plt.tight_layout()

    plt.show()

main()
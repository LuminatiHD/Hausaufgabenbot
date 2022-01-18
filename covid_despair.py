import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date, timedelta
import requests


def formatting(val):
    val = val.replace(" ", "")
    if int(val) > 1e6:
        val = f"{val[0:-6]}.{val[-6:-4]}M"
    elif int(val) > 1e3:
        val = f"{val[0:-3]}'{val[-3:]}"
    return val


def get_graph():
    sw_url = "https://www.worldometers.info/coronavirus////country/switzerland/"
    sw_sourcecode = requests.get(sw_url, "html-parser").text

    sw_daily_cases = sw_sourcecode \
        .split("<h3>Daily New Cases in Switzerland</h3>")[1] \
        .split("name: 'Daily Cases'")[1] \
        .split("data: [")[1] \
        .split("]")[0].split(",")

    sw_daily_cases = [int(i) if i != "null" else 0 for i in sw_daily_cases]

    start_date = date(2020, 2, 15)
    dates = [start_date + timedelta(i) for i in range(0, (date.today() - start_date).days)]

    fig = plt.figure()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=round(len(sw_daily_cases) / 8)))

    plt.title("Tägliche COVID-Zahlen Schweiz [2]")
    plt.xlim(start_date - timedelta(11), dates[-1])
    plt.ylim(0, max(sw_daily_cases) * 1.1)
    plt.grid()
    plt.plot(dates, sw_daily_cases)
    plt.gcf().autofmt_xdate()

    fig.savefig("graph.png")
    return "graph.png"


def get_cases():
    # ================================ SCHWEIZ =================================
    sw_url = "https://www.worldometers.info/coronavirus////country/switzerland/"
    sw_bag_url = "https://www.covid19.admin.ch/de/overview"
    sw_sourcecode = requests.get(sw_url, "html-parser").text

    sw_all_cases = sw_sourcecode\
        .split("<h1>Coronavirus Cases:</h1>\n""<div class=\""
               "maincounter-number\""">\n<span style=\"color:#aaa\">")[1]\
        .split(" </span>")[0].replace(",", "")

    sw_all_deaths = sw_sourcecode\
        .split("<h1>Deaths:</h1>\n<div class=""\"maincounter-number\">\n<span>")[1]\
        .split("</span>")[0].replace(",", "")

    sw_daily_cases = requests.get(sw_bag_url, "html-parser").text\
        .split("Laborbestätigte Fälle")[1]\
        .split("Differenz")[1]\
        .split("class=\"bag-key-value-list__entry-value\">")[1]\
        .split("</span")[0]

    sw_daily_deaths = requests.get(sw_bag_url, "html-parser").text\
        .split("Laborbestätigte Todesfälle")[1]\
        .split("Differenz")[1]\
        .split("class=\"bag-key-value-list__entry-value\">")[1]\
        .split("</span")[0]

    sw_stand = requests.get(sw_bag_url, "html-parser").text\
        .split("Quelle: BAG – Stand: ")[1]\
        .split(" <!----><!---->")[0]

    # ================================ GLOBAL =======================================
    gl_url = "https://www.worldometers.info/coronavirus/"
    gl_sourcecode = requests.get(gl_url, "html-parser").text

    gl_all_cases = gl_sourcecode\
        .split("<h1>Coronavirus Cases:</h1>\n""<div class=\""
               "maincounter-number\""">\n<span style=\"color:#aaa\">")[1]\
        .split(" </span>")[0].replace(",", "")

    gl_all_deaths = gl_sourcecode\
        .split("<h1>Deaths:</h1>\n<div class=""\"maincounter-number\">\n<span>")[1]\
        .split("</span>")[0].replace(",", ""
)
    gl_daily_cases = gl_sourcecode\
        .split("name: 'Daily Cases'")[1]\
        .split("data: [")[1]\
        .split("]")[0].split(",")

    gl_daily_deaths = gl_sourcecode\
        .split("name: 'Daily Deaths'")[1]\
        .split("data: [")[1] \
        .split("]")[0].split(",")

    for i in (sw_all_cases, sw_all_deaths, sw_daily_cases, sw_daily_deaths,
            gl_all_cases, gl_all_deaths, gl_daily_cases, gl_daily_deaths):
        if type(i) == list:
            if i[-1] == "0":
                i = formatting(i[-2])
            else:
                i = formatting(i[-1])
        else:
            i = formatting(i)
        yield i

    yield sw_stand

import base64
import requests
import datetime as dt
from covid import app
from matplotlib import pyplot as plt
from io import BytesIO

NATIONAL_URL = app.config["NATIONAL_URL"]
REGIONAL_URL = app.config["REGIONAL_URL"]
PROVINCIAL_URL = app.config["PROVINCIAL_URL"]
DATE_FMT = "%Y%m%d"


def parse_date(date_str):
    date_dt = dt.datetime.strptime(date_str, "%m/%d/%Y %H:%M %p")
    return dt.datetime.strftime(date_dt, DATE_FMT)


def get_overview(date_from, date_to, territory=""):
    data = {}
    if not territory:
        url = "{}?from={}&to={}".format(NATIONAL_URL, date_from, date_to)
    else:
        url = "{}?from={}&to={}&region={}".format(
            REGIONAL_URL, date_from, date_to, territory)
    app.logger.debug("Sending request to {}".format(url))
    response = requests.get(url)
    if response.status_code == 200:
        res_data = response.json()
        app.logger.debug("Got Response {}".format(res_data))
        data = res_data["data"]
    return data


def get_province_data(date_from, date_to, province):
    data = {}
    if not province:
        url = "{}?from={}&to={}".format(NATIONAL_URL, date_from, date_to)
    else:
        url = "{}?from={}&to={}&province={}".format(
            PROVINCIAL_URL, date_from, date_to, province)
    app.logger.debug("Sending request to {}".format(url))
    response = requests.get(url)
    if response.status_code == 200:
        res_data = response.json()
        app.logger.debug("Got Response {}".format(res_data))
        data = res_data["data"]
    return data


def plot_overview(data, territory=""):
    dates = []
    intensive_care = []
    hospitalized_w_symptoms = []
    total_cases = []
    healed = []
    fig, axs = plt.subplots(nrows=2, ncols=2, constrained_layout=True)
    for d in data:
        dates.append(dt.datetime.strptime(d["data"], "%Y%m%d"))
        intensive_care.append(d["terapia_intensiva"])
        hospitalized_w_symptoms.append(d["ricoverati_con_sintomi"])
        total_cases.append(d["totale_casi"])
        healed.append(d["dimessi_guariti"])
    axs[0, 0].plot(dates, intensive_care, 'tab:red')
    axs[0, 0].set_title('In intensive care {}'.format(territory))
    axs[0, 1].plot(dates, hospitalized_w_symptoms, 'tab:orange')
    axs[0, 1].set_title('Hospitalized with symptoms {}'.format(territory))
    axs[1, 0].plot(dates, total_cases)
    axs[1, 0].set_title('Total cases {}'.format(territory))
    axs[1, 1].plot(dates, healed, 'tab:green')
    axs[1, 1].set_title('Healed (dismissed) {}'.format(territory))
    for ax in axs.flat:
        ax.set(xlabel='Date', ylabel='# People')
    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=45)
        plt.xticks(size=6)
    for ax in axs.flat:
        ax.label_outer()
    # TODO: Make it concurrent-safe:
    #  use datetime and uuid() to serve the right plot to the right client
    figfile = BytesIO()
    plt.savefig(figfile, format='png', dpi=120)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png.decode('utf8')


def plot_total_in_province(data, province=""):
    dates = []
    total_cases = []
    fig, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=True)
    for d in data:
        dates.append(dt.datetime.strptime(d["data"], "%Y%m%d"))
        total_cases.append(d["totale_casi"])
    ax.plot(dates, total_cases, 'tab:red')
    ax.set(
        xlabel='Date', ylabel='# People',
        title='Total cases in {}'.format(province.upper()))
    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=45)
        plt.xticks(size=6)
    figfile = BytesIO()
    plt.savefig(figfile, format='png', dpi=120)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    plt.clf()
    return figdata_png.decode('utf8')

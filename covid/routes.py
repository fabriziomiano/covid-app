from covid import app
from flask import request, render_template
from covid.data import (
    get_overview, parse_date, plot_overview, get_province_data,
    plot_total_in_province
)


@app.route('/')
def home():
    return render_template(
        "layout.html",
        title="COVID-19 Outbreak in Italy",
        subtitle="A tool to visualize Coronavirus pandemic",
        helper="Use the menu to visualize national / regional / provincial data",
        pagetype="home"
    )


@app.route("/national")
def national():
    plot = ""
    error = ""
    try:
        if request.args.get("date_from") and request.args.get("date_from"):
            app.logger.debug(request.args)
            date_from = parse_date(request.args["date_from"])
            date_to = parse_date(request.args["date_to"])
            data = get_overview(date_from, date_to)
            plot = plot_overview(data)
        else:
            error = "Please provide time interval"
    except Exception as e:
        error = "{}".format(e)
    return render_template(
        "layout.html",
        title="National scenario",
        pagetype="national",
        plot=plot,
        error=error,
        action="national"
    )


@app.route("/regional")
def regional():
    region = ""
    plot = ""
    error = ""
    title = "Regional scenario"
    try:
        if request.args.get("date_from") and request.args.get("date_from"):
            app.logger.debug(request.args)
            date_from = parse_date(request.args["date_from"])
            date_to = parse_date(request.args["date_to"])
            region = request.args.get("territory")
            if not region:
                data = get_overview(date_from, date_to)
                plot = plot_overview(data)
            else:
                region = region.capitalize()
                data = get_overview(date_from, date_to, region)
                if not data:
                    error = "No data for the selected region: {}".format(region)
                else:
                    plot = plot_overview(data, region)
                    title += " - {}".format(region)
        else:
            error = "Please provide time interval"
    except Exception as e:
        error = "{}".format(e)
    return render_template(
        "layout.html",
        title=title,
        pagetype="regional",
        territory="Region",
        plot=plot,
        error=error,
        action="regional",
        region=region
    )


@app.route("/provincial")
def provincial():
    province = ""
    plot = ""
    error = ""
    title = "Provincial scenario"
    try:
        if request.args.get("date_from") and request.args.get("date_from"):
            app.logger.debug(request.args)
            date_from = parse_date(request.args["date_from"])
            date_to = parse_date(request.args["date_to"])
            province = request.args.get("territory")
            if not province:
                data = get_overview(date_from, date_to)
                plot = plot_overview(data)
            else:
                province = province.upper()
                data = get_province_data(date_from, date_to, province)
                if not data:
                    error = "No data for the selected province: {}".format(province)
                else:
                    plot = plot_total_in_province(data, province)
                    title += " - {}".format(province)
        else:
            error = "Please provide time interval"
    except Exception as e:
        error = "{}".format(e)
    return render_template(
        "layout.html",
        title=title,
        pagetype="provincial",
        territory="Province",
        plot=plot,
        error=error,
        action="provincial",
        province=province
    )

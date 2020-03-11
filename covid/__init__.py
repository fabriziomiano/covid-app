import os
from flask import Flask


app = Flask(__name__)
app.config["NATIONAL_URL"] = os.environ["NATIONAL_URL"]
app.config["REGIONAL_URL"] = os.environ["REGIONAL_URL"]
app.config["PROVINCIAL_URL"] = os.environ["PROVINCIAL_URL"]

from covid import routes

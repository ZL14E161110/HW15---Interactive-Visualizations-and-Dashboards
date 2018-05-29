import datetime as dt
import numpy as np
import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
from flask_sqlalchemy import SQLAlchemy
# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/belly_button_biodiversity.sqlite"
# #################################################
# # database setup
# #################################################
db = SQLAlchemy(app)

class Emoji(db.Model):
    __tablename__ = 'emoji'

    id = db.Column(db.Integer, primary_key=True)
    emoji_char = db.Column(db.String)
    emoji_id = db.Column(db.String)
    name = db.Column(db.String)
    score = db.Column(db.Integer)

    def __repr__(self):
        return '<Emoji %r>' % (self.name)

# Create database tables
@app.before_first_request
def setup():
    # Recreate database each time for demo
    # db.drop_all()
    db.create_all()

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """Return the dashboard homepage."""
    return render_template("index.html")

@app.route("/names")
def names():
    """List of sample names.
    Returns a list of sample names in the format
    [
        "BB_940",
        "BB_941",
        "BB_943",
        "BB_944",
        "BB_945",
        "BB_946",
        "BB_947",
        ...
    ]
    """

    # query for the top 10 emoji data
    results = db.session.query(Emoji.emoji_char, Emoji.score).\
        order_by(Emoji.score.desc()).\
        limit(10).all()

    # Select the top 10 query results
    emoji_char = [result[0] for result in results]
    scores = [int(result[1]) for result in results]

    # Generate the plot trace
    plot_trace = {
        "x": emoji_char,
        "y": scores,
        "type": "bar"
    }
    return jsonify(plot_trace)



@app.route("/otu")
def otu():
    """List of OTU descriptions.
    Returns a list of OTU descriptions in the following format
    [
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Bacteria",
        "Bacteria",
        "Bacteria",
        ...
    ]
    """


    # query for the emoji data using pandas
    query_statement = db.session.query(Emoji).\
    order_by(Emoji.score.desc()).\
    limit(10).statement
    df = pd.read_sql_query(query_statement, db.session.bind)
    
    # Format the data for Plotly
    plot_trace = {
            "x": df["emoji_id"].values.tolist(),
            "y": df["score"].values.tolist(),
            "type": "bar"
    }
    return jsonify(plot_trace)

@app.route("/metadata/<sample>")
@app.route("/metadata")
def metadata(sample="None"):
    """MetaData for a given sample.
    Args: Sample in the format: `BB_940`
    Returns a json dictionary of sample metadata in the format
    {
        AGE: 24,
        BBTYPE: "I",
        ETHNICITY: "Caucasian",
        GENDER: "F",
        LOCATION: "Beaufort/NC",
        SAMPLEID: 940
    }
    """
    # query for the top 10 emoji data
    results = db.session.query(Emoji.name, Emoji.score).\
        order_by(Emoji.score.desc()).\
        limit(10).all()
    df = pd.DataFrame(results, columns=['name', 'score'])

    # Format the data for Plotly
    plot_trace = {
            "x": df["name"].values.tolist(),
            "y": df["score"].values.tolist(),
            "type": "bar"
    }
    return jsonify(plot_trace)

@app.route("/wfreq/<sample>")
@app.route("/wfreq")
def wfreq(sample="None"):
    """Weekly Washing Frequency as a number.

    Args: Sample in the format: `BB_940`

    Returns an integer value for the weekly washing frequency `WFREQ`
    """
    # query for the top 10 emoji data
    results = db.session.query(Emoji.name, Emoji.score).\
        order_by(Emoji.score.desc()).\
        limit(10).all()
    df = pd.DataFrame(results, columns=['name', 'score'])

    # Format the data for Plotly
    plot_trace = {
            "x": df["name"].values.tolist(),
            "y": df["score"].values.tolist(),
            "type": "bar"
    }
    return jsonify(plot_trace)

@app.route("/samples/<sample>")
@app.route("/samples")
def samples(sample="None"):
    """OTU IDs and Sample Values for a given sample.
    Sort your Pandas DataFrame (OTU ID and Sample Value)
    in Descending Order by Sample Value
    Return a list of dictionaries containing sorted lists  for `otu_ids`
    and `sample_values`
    [
        {
            otu_ids: [
                1166,
                2858,
                481,
                ...
            ],
            sample_values: [
                163,
                126,
                113,
                ...
            ]
        }
    ]
    """
    # query for the top 10 emoji data
    results = db.session.query(Emoji.name, Emoji.score).\
        order_by(Emoji.score.desc()).\
        limit(10).all()
    df = pd.DataFrame(results, columns=['name', 'score'])

    # Format the data for Plotly
    plot_trace = {
            "x": df["name"].values.tolist(),
            "y": df["score"].values.tolist(),
            "type": "bar"
    }
    return jsonify(plot_trace)

if __name__ == '__main__':
    app.run(debug=True)

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
from sqlalchemy import create_engine
from sqlalchemy import inspect
from flask_sqlalchemy import SQLAlchemy

# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/belly_button_biodiversity.sqlite"
db = SQLAlchemy(app)
engine = create_engine("sqlite:///db/belly_button_biodiversity.sqlite")
# #################################################
# # table setup
# #################################################
class Otu(db.Model):
    """docstring for Otu"""
    __tablename__ = "otu"
    otu_id = db.Column(db.Integer, primary_key=True)
    lowest_taxonomic_unit_found = db.Column(db.String)


class Metadata(db.Model):
    __tablename__ = "samples_metadata"
    sampleid = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String)
    ethnicity = db.Column(db.String)
    gender = db.Column(db.String)
    age = db.Column(db.Integer)
    wfreq = db.Column(db.Float)
    bbtype = db.Column(db.String)
    location = db.Column(db.String)
    country012 = db.Column(db.String)
    zip012 = db.Column(db.Integer)
    country1319 = db.Column(db.String)
    zip1319 = db.Column(db.Integer)
    dog = db.Column(db.String)
    cat = db.Column(db.String)
    impsurface013 = db.Column(db.Integer)
    npp013 = db.Column(db.Float)
    mmaxtemp013 = db.Column(db.Float)
    pfc013 = db.Column(db.Float)
    impsurface1319 = db.Column(db.Integer)
    npp1319 = db.Column(db.Float)
    mmaxtemp1319 = db.Column(db.Float)
    pfc1319 = db.Column(db.Float)


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
    samplename = []
    # query for all the sample data
    inspector = inspect(engine)
    columns = iter(inspector.get_columns('samples'))
    next(columns)
    for column in columns:
        samplename.append(column['name'])
    return jsonify(samplename)



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

    # query for the otu data
    low_units_list = db.session.query(Otu.lowest_taxonomic_unit_found).all()
    low_units = [l[0] for l in low_units_list]

    return jsonify(low_units)


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
    # query for the sample metadata
    metadata_ls = []
    for i in db.session.query(Metadata.age, Metadata.bbtype, Metadata.ethnicity, Metadata.gender, Metadata.location, Metadata.sampleid).all():
        sample_item = {}

        sample_item['SAMPLEID'] = i[5]
        sample_item['AGE'] = i[0]
        sample_item['BBTYPE'] = i[1]
        sample_item['ETHNICITY'] = i[2]
        sample_item['GENDER'] = i[3]
        sample_item['LOCATION'] = i[4]

        metadata_ls.append(sample_item)

    for selection in metadata_ls:
        if sample[3:] == str(selection['SAMPLEID']):
            return jsonify(selection)

    return jsonify(metadata)
    
@app.route("/wfreq/<sample>")
@app.route("/wfreq")
def wfreq(sample="None"):
    """Weekly Washing Frequency as a number.

    Args: Sample in the format: `BB_940`

    Returns an integer value for the weekly washing frequency `WFREQ`
    """
    # query for the wfreq data
    wfreq_ls = []
    for i in db.session.query(Metadata.wfreq, Metadata.sampleid).all():
        wfreq_ls.append(i)
        if sample[3:] == str(i[1]):
            return jsonify(i[0])

    wfreq_ls = ["{}, {}".format(l[0], l[1]) for l in wfreq_ls]

    return jsonify(wfreq)

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
    # query OTU ID and Sample Values
    df = pd.read_sql('SELECT * FROM samples', engine).set_index('otu_id')

    otu_ids = df['BB_{}'.format(sample[3:])].sort_values(ascending=False).index.tolist()
    sample_values = df['BB_{}'.format(sample[3:])].sort_values(ascending=False).tolist()

    otu_ids = [int(i) for i in otu_ids]
    sample_values = [int(i) for i in sample_values]

    result = {'otu_ids': otu_ids, 'sample_values': sample_values}

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)

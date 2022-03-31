from codecs import getencoder
from flask import Flask, jsonify
from dotenv import load_dotenv
import os

from src.function import generateIndustryData, generateCompanyData, generateDataWithYahooAPI

load_dotenv()
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/industry")
def generate_industry():
    generateIndustryData()
    return jsonify({'message': 'done'}), 200


@app.route("/company")
def generate_company():
    generateCompanyData()
    return jsonify({'message': 'done'}), 200


@app.route("/finantial_statements")
def generate_finantial_statements():
    generateDataWithYahooAPI()
    return jsonify({'message': 'done'}), 200


if __name__ == "__main__":
    HOST = os.getenv("ANGE_HOST")
    PORT = os.getenv("ANGE_PORT")
    app.run(host=HOST, port=PORT)
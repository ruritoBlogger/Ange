from codecs import getencoder
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from src.function import generateIndustryData, generateCompanyData, generateDataWithYahooAPI

load_dotenv()
app = Flask(__name__)
CORS(app)

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


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

if __name__ == "__main__":
    HOST = os.getenv("ANGE_HOST")
    PORT = os.getenv("ANGE_PORT")
    app.run(host=HOST, port=PORT)
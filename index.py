from flask import Flask, jsonify
from src.function import generateIndustryData, generateCompanyData, generateDataWithYahooAPI
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
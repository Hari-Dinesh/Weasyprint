import logging
import ssl
from flask import Flask, request, jsonify, make_response
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from weasyprint import HTML
from PyPDF2 import PdfReader, PdfWriter
import io


# SSL context setup
ssl._create_default_https_context = ssl._create_unverified_context

# Flask app setup
app = Flask(__name__)

# Jinja2 environment setup
env = Environment(loader=FileSystemLoader('./templates'))

# Template mapping
template_mapping = {
    "sdipdf": "sdi.html"
}
data={
    "password": "05-07-2024",
    "replaceVariables": {
      "layoutCode": "layout3",
      "patientLastName": "C",
      "patientFirstName": "Wsdi",
      "patientName": "Wsdi C",
      "password": "05-07-2024",
      "accessionId": "QQQQ-190714",
      "patientGender": "male",
      "patientMobileNumber": "(124) 351-2352",
      "patientAge": "-",
      "patientAddress": "dfsgasdfsdaf, Housing board, Cold bay, Alaska, 99571",
      "patientId": 110386,
      "sampleCollectionTime": "15:45",
      "patientEmailId": "chinnasaicharan9640@gmail.com",
      "sampleResult": {
        "barcode": {
          "value": "QQQQ-190714"
        },
        "FT3": {
          "value": "Positive"
        },
        "FT4": {
          "value": "Positive"
        },
        "Qualitative Biomarker 2": {
          "value": "Positive"
        },
        "Qualitative Biomarker 1": {
          "value": "Negative"
        },
        "Q1": {
          "value": "detected"
        },
        "Q2": {
          "value": "not detected"
        },
        "Q3": {
          "value": "invalid"
        },
        "Q4": {
          "value": "valid"
        }
      },
      "sampleType": "Blood",
      "orderId": "GK7286",
      "sampleResultColor": "000000",
      "finalResultObject": [
        {
          "tableName": "pathogen",
          "rows": [
            {
              "testName": "Q",
              "resultValue": "detected",
              "rule": [
                {
                  "color": "#e8d5c7ff",
                  "units": "mg/dL",
                  "result": "DETECTED",
                  "value1": "12",
                  "value2": "50",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#F45863",
                "fontWeight": "normal",
                "qualitativeResultValue": "DETECTED",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Q1",
              "biomarkerDescription": "",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "DETECTED",
              "biomarkerNote": "",
              "expectedResults": "DETECTED"
            },
            {
              "testName": "Q",
              "resultValue": "not detected",
              "rule": [
                {
                  "color": "#e8d5c7ff",
                  "units": "mg/dL",
                  "result": "NON DETECTED",
                  "value1": "9",
                  "value2": "50",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#5a9759ff",
                "fontWeight": "normal",
                "qualitativeResultValue": "NOT DETECTED",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Q2",
              "biomarkerDescription": "",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "NOT DETECTED",
              "biomarkerNote": "",
              "expectedResults": "NON DETECTED"
            },
            {
              "testName": "Q",
              "resultValue": "invalid",
              "rule": [
                {
                  "color": "#e8d5c7ff",
                  "units": "mg/dL",
                  "result": "DETECTED",
                  "value1": "10",
                  "value2": "30",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#202020",
                "fontWeight": "normal",
                "qualitativeResultValue": "INVALID",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Q3",
              "biomarkerDescription": "",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "INVALID",
              "biomarkerNote": "",
              "expectedResults": "DETECTED"
            },
            {
              "testName": "Q",
              "resultValue": "valid",
              "rule": [
                {
                  "color": "#e8d5c7ff",
                  "units": "mg/dL",
                  "result": "INVALID",
                  "value1": "15",
                  "value2": "30",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#e8d5c7ff",
                "fontWeight": "normal",
                "qualitativeResultValue": "valid",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Q4",
              "biomarkerDescription": "",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "valid",
              "biomarkerNote": "",
              "expectedResults": "INVALID"
            }
          ]
        },
        {
          "tableName": "bacteria",
          "rows": [
            {
              "testName": "Q",
              "resultValue": "Positive",
              "rule": [
                {
                  "units": "pg/mL",
                  "value1": "2.4",
                  "value2": "4.2",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#F45863",
                "fontWeight": "bold",
                "qualitativeResultValue": "-",
                "borderColor": "#F45863"
              },
              "biomarkerName": "FT3",
              "biomarkerDescription": "",
              "reportFormat": "Quantitative",
              "qualitativeResultValue": "-",
              "biomarkerNote": "",
              "expectedResults": "Nil"
            },
            {
              "testName": "Q",
              "resultValue": "Positive",
              "rule": [
                {
                  "units": "pg/mL",
                  "value1": "8",
                  "value2": "18",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#F45863",
                "fontWeight": "bold",
                "qualitativeResultValue": "-",
                "borderColor": "#F45863"
              },
              "biomarkerName": "FT4",
              "biomarkerDescription": "",
              "reportFormat": "Quantitative",
              "qualitativeResultValue": "-",
              "biomarkerNote": "",
              "expectedResults": "Nil"
            }
          ]
        },
        {
          "tableName": "germs",
          "rows": [
            {
              "testName": "Q",
              "resultValue": "Positive",
              "rule": [
                {
                  "color": "#d0021bff",
                  "units": "mg/dL",
                  "result": "Negative",
                  "value1": "1",
                  "value2": "100",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#5a9759ff",
                "fontWeight": "normal",
                "qualitativeResultValue": "POSITIVE",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Qualitative Biomarker 2",
              "biomarkerDescription": "ljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrtese",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "POSITIVE",
              "biomarkerNote": "",
              "expectedResults": "Negative"
            },
            {
              "testName": "Q",
              "resultValue": "Positive",
              "rule": [
                {
                  "color": "#d0021bff",
                  "units": "mg/dL",
                  "result": "Negative",
                  "value1": "1",
                  "value2": "100",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#5a9759ff",
                "fontWeight": "normal",
                "qualitativeResultValue": "POSITIVE",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Qualitative Biomarker 2",
              "biomarkerDescription": "ljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrtese",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "POSITIVE",
              "biomarkerNote": "",
              "expectedResults": "Negative"
            },
            {
              "testName": "Q",
              "resultValue": "Negative",
              "rule": [
                {
                  "color": "#32ff32ff",
                  "units": "mg/dL",
                  "result": "positive",
                  "value1": "1",
                  "value2": "100",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#F45863",
                "fontWeight": "normal",
                "qualitativeResultValue": "NEGATIVE",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Qualitative Biomarker 1",
              "biomarkerDescription": "tgrefwdljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrtese",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "NEGATIVE",
              "biomarkerNote": "",
              "expectedResults": "Positive"
            },
           {
              "testName": "Q",
              "resultValue": "Positive",
              "rule": [
                {
                  "color": "#d0021bff",
                  "units": "mg/dL",
                  "result": "Negative",
                  "value1": "1",
                  "value2": "100",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#5a9759ff",
                "fontWeight": "normal",
                "qualitativeResultValue": "POSITIVE",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Qualitative Biomarker 2",
              "biomarkerDescription": "ljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrtese",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "POSITIVE",
              "biomarkerNote": "",
              "expectedResults": "Negative"
            },
            {
              "testName": "Q",
              "resultValue": "Positive",
              "rule": [
                {
                  "color": "#d0021bff",
                  "units": "mg/dL",
                  "result": "Negative",
                  "value1": "1",
                  "value2": "100",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#5a9759ff",
                "fontWeight": "normal",
                "qualitativeResultValue": "POSITIVE",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Qualitative Biomarker 2",
              "biomarkerDescription": "ljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrtese",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "POSITIVE",
              "biomarkerNote": "",
              "expectedResults": "Negative"
            },
            {
              "testName": "Q",
              "resultValue": "Negative",
              "rule": [
                {
                  "color": "#32ff32ff",
                  "units": "mg/dL",
                  "result": "positive",
                  "value1": "1",
                  "value2": "100",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#F45863",
                "fontWeight": "normal",
                "qualitativeResultValue": "NEGATIVE",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Qualitative Biomarker 1",
              "biomarkerDescription": "tgrefwdljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrtese",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "NEGATIVE",
              "biomarkerNote": "",
              "expectedResults": "Positive"
            },
            {
              "testName": "Q",
              "resultValue": "Positive",
              "rule": [
                {
                  "color": "#d0021bff",
                  "units": "mg/dL",
                  "result": "Negative",
                  "value1": "1",
                  "value2": "100",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#5a9759ff",
                "fontWeight": "normal",
                "qualitativeResultValue": "POSITIVE",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Qualitative Biomarker 2",
              "biomarkerDescription": "ljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrtese",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "POSITIVE",
              "biomarkerNote": "",
              "expectedResults": "Negative"
            },
            {
              "testName": "Q",
              "resultValue": "Positive",
              "rule": [
                {
                  "color": "#d0021bff",
                  "units": "mg/dL",
                  "result": "Negative",
                  "value1": "1",
                  "value2": "100",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#5a9759ff",
                "fontWeight": "normal",
                "qualitativeResultValue": "POSITIVE",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Qualitative Biomarker 2",
              "biomarkerDescription": "ljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrtese",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "POSITIVE",
              "biomarkerNote": "",
              "expectedResults": "Negative"
            },
            {
              "testName": "Q",
              "resultValue": "Negative",
              "rule": [
                {
                  "color": "#32ff32ff",
                  "units": "mg/dL",
                  "result": "positive",
                  "value1": "1",
                  "value2": "100",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#F45863",
                "fontWeight": "normal",
                "qualitativeResultValue": "NEGATIVE",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Qualitative Biomarker 1",
              "biomarkerDescription": "tgrefwdljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrtese",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "NEGATIVE",
              "biomarkerNote": "",
              "expectedResults": "Positive"
            },
           {
              "testName": "Q",
              "resultValue": "Positive",
              "rule": [
                {
                  "color": "#d0021bff",
                  "units": "mg/dL",
                  "result": "Negative",
                  "value1": "1",
                  "value2": "100",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#5a9759ff",
                "fontWeight": "normal",
                "qualitativeResultValue": "POSITIVE",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Qualitative Biomarker 2",
              "biomarkerDescription": "ljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrtese",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "POSITIVE",
              "biomarkerNote": "",
              "expectedResults": "Negative"
            },
            {
              "testName": "Q",
              "resultValue": "Positive",
              "rule": [
                {
                  "color": "#d0021bff",
                  "units": "mg/dL",
                  "result": "Negative",
                  "value1": "1",
                  "value2": "100",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#5a9759ff",
                "fontWeight": "normal",
                "qualitativeResultValue": "POSITIVE",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Qualitative Biomarker 2",
              "biomarkerDescription": "ljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrtese",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "POSITIVE",
              "biomarkerNote": "",
              "expectedResults": "Negative"
            },
            {
              "testName": "Q",
              "resultValue": "Negative",
              "rule": [
                {
                  "color": "#32ff32ff",
                  "units": "mg/dL",
                  "result": "positive",
                  "value1": "1",
                  "value2": "100",
                  "expression": "-"
                }
              ],
              "fontFormat": {
                "color": "#F45863",
                "fontWeight": "normal",
                "qualitativeResultValue": "NEGATIVE",
                "borderColor": "#F45863"
              },
              "biomarkerName": "Qualitative Biomarker 1",
              "biomarkerDescription": "tgrefwdljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrtese",
              "reportFormat": "Qualitative",
              "qualitativeResultValue": "NEGATIVE",
              "biomarkerNote": "",
              "expectedResults": "Positive"
            }
          
          ]
        }
      ],
      "testDetails": {
        "id": 41,
        "name": "Q",
        "code": "QQQQ",
        "sampleType": "blood",
        "sampleCollectionDeviceName": "tube",
        "sampleQuantity": "100",
        "description": "",
        "createdBy": 1,
        "isIntakeFormRequired": False,
        "formId": None,
        "isStateReportingRequired": False,
        "stateReporting": None,
        "isBulkImportRequired": False,
        "isActive": True,
        "biomarkerIds": [
          78,
          77,
          79,
          80,
          5,
          4,
          64,
          65
        ],
        "status": "completed",
        "chatId": None,
        "lastBarcodeCount": None,
        "resultingMode": "manual upload",
        "processOverView": None,
        "kitComponents": None,
        "kitImages": None,
        "questions": None,
        "videoUrl": None,
        "kitRedirectUrl": None,
        "normalPdfTemplatePath": None,
        "abnormalPdfTemplatePath": None,
        "testLayoutDetails": [
          {
            "layout": "layout2",
            "disclaimer": "<div><p><strong>Methodology: </strong>This Urinary TractInfection (UTI) molecular multiple pathogen detection testis as a Laboratory Developed Test(LDT). Utilizing multiplex realtime PCR (qPCR), it specifically identifies pathogens (as listed above) present in the patient's urine specimen. The patient's urine specimen undergoes treatmentfor RNA/DNAextraction and is then processed to detect the presence of various urinary pathogens outlined in the panel (refer to above list). This process employs specific primers/probes on a realtimePCR instrument. The results are compared to contrived positive controls, internal controls, and NegativeTemplateControls (QualityControl Samples) run alongside the patient's extracted urine sample or the molecular diagnosis of urinary infections. </p><ul><li>list1</li><li>list2</li><li>list3</li></ul><p><strong> Limitations: </strong>All molecular tests have limitations. If a patient receives a 'NOT DETECTED' or 'NEGATIVE' result, itmeans thatthe pathogens mentioned in thereportwere notdetected in the specimen atthe time of sample collection. However, it's importantto note thatthis resultdoes not rule outthe possibility thatthe patient's symptoms, experienced prior to this test, may be caused by pathogens notincluded in this panel. </p><ol><li>list1</li><li>list2</li><li>list</li></ol><p><strong>Eligibility for Testing:</strong>This test should be used for diagnostic use only and is limited to patients suspected of urinary infections by their healthcare provider. The eligibility determination ultimately rests on the clinician’s judgment. </p><p><strong> Conduct of the Test:</strong>This testis performed under strict compliance and guidelines ofAdvanced Genomics LLC, including the instruments, reagents, and other recommended procedures. This includes the safety protocols where all laboratory personnel are appropriately trained in qPCR techniques and use appropriate laboratory and personal protective equipment when handling this kit/test and use this test in accordance with the authorised labeling. </p><p> <strong>Result Reports for HealthcareProviders and Patients: </strong>We have a process for reporting test results to healthcare providers as appropriate. Result reports will be provided to healthcare providers and patients. </p><p> <strong>PerformanceData and Reporting: </strong>We collect information on the performance of the test and report any suspected occurrence of False positive or False negative results and significant deviations from the established performance characteristics of the test of which we become aware to concerned authorities. </p><p><strong> Record keeping: </strong>As an authorised laboratory we ensure all records associated with this test are maintained until otherwise notified. Such records are available to </p><ul><li>list1</li><li>list2</li><li>listefkemnjnejnfjnjenknfkneinfineinfineinfineifiernivirnvirninvinrincirninqbvhbehrbvhbhbhbvhbefhibvehjbrvhbie v hibihwbv hebhibvjj evbubvnrjnvubr</li></ul></div>",
            "biomarkerObj": [
              {
                "title": "pathogen",
                "biomarkerIds": [
                  77,
                  78,
                  79,
                  80
                ],
                "biomarkerDetails": [
                  {
                    "id": 77,
                    "name": "Q1",
                    "isActive": True,
                    "code": "Q1",
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": "",
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-06-06T15:03:11.687Z",
                    "createdBy": 1,
                    "biomarkerConfig": [
                      {
                        "id": 80,
                        "biomarkerId": 77,
                        "gender": "all",
                        "age": "0-100",
                        "rules": [
                          {
                            "color": "#e8d5c7ff",
                            "units": "mg/dL",
                            "result": "DETECTED",
                            "value1": "12",
                            "value2": "50",
                            "expression": "-"
                          }
                        ],
                        "expectedResults": "DETECTED",
                        "biomarkerNotes": "",
                        "isBiomarkerNoteAvailable": False,
                        "createdAt": "2024-06-06T15:03:58.814Z",
                        "updatedAt": "2024-06-06T15:03:58.814Z"
                      }
                    ]
                  },
                  {
                    "id": 78,
                    "name": "Q2",
                    "isActive": True,
                    "code": "Q2",
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": "",
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-06-06T15:04:36.190Z",
                    "createdBy": 1,
                    "biomarkerConfig": [
                      {
                        "id": 81,
                        "biomarkerId": 78,
                        "gender": "all",
                        "age": "0-100",
                        "rules": [
                          {
                            "color": "#e8d5c7ff",
                            "units": "mg/dL",
                            "result": "NON DETECTED",
                            "value1": "9",
                            "value2": "50",
                            "expression": "-"
                          }
                        ],
                        "expectedResults": "NON DETECTED",
                        "biomarkerNotes": "",
                        "isBiomarkerNoteAvailable": False,
                        "createdAt": "2024-06-06T15:05:04.731Z",
                        "updatedAt": "2024-06-06T15:05:04.731Z"
                      }
                    ]
                  },
                  {
                    "id": 79,
                    "name": "Q3",
                    "isActive": True,
                    "code": "Q3",
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": "",
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-06-06T15:05:24.313Z",
                    "createdBy": 1,
                    "biomarkerConfig": [
                      {
                        "id": 82,
                        "biomarkerId": 79,
                        "gender": "all",
                        "age": "0-100",
                        "rules": [
                          {
                            "color": "#e8d5c7ff",
                            "units": "mg/dL",
                            "result": "DETECTED",
                            "value1": "10",
                            "value2": "30",
                            "expression": "-"
                          }
                        ],
                        "expectedResults": "DETECTED",
                        "biomarkerNotes": "",
                        "isBiomarkerNoteAvailable": False,
                        "createdAt": "2024-06-06T15:05:49.374Z",
                        "updatedAt": "2024-06-06T15:39:57.125Z"
                      }
                    ]
                  },
                  {
                    "id": 80,
                    "name": "Q4",
                    "isActive": True,
                    "code": "Q4",
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": "",
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-06-06T15:06:05.489Z",
                    "createdBy": 1,
                    "biomarkerConfig": [
                      {
                        "id": 83,
                        "biomarkerId": 80,
                        "gender": "all",
                        "age": "0-100",
                        "rules": [
                          {
                            "color": "#e8d5c7ff",
                            "units": "mg/dL",
                            "result": "INVALID",
                            "value1": "15",
                            "value2": "30",
                            "expression": "-"
                          }
                        ],
                        "expectedResults": "INVALID",
                        "biomarkerNotes": "",
                        "isBiomarkerNoteAvailable": False,
                        "createdAt": "2024-06-06T15:06:28.973Z",
                        "updatedAt": "2024-06-06T15:41:37.957Z"
                      }
                    ]
                  }
                ]
              },
              {
                "title": "bacteria",
                "biomarkerIds": [
                  4,
                  5
                ],
                "biomarkerDetails": [
                  {
                    "id": 4,
                    "name": "FT3",
                    "isActive": True,
                    "code": "FT3",
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": "",
                    "reportFormat": "Quantitative",
                    "status": "completed",
                    "createdAt": "2024-01-30T06:53:40.136Z",
                    "createdBy": 1,
                    "biomarkerConfig": [
                      {
                        "id": 5,
                        "biomarkerId": 4,
                        "gender": "male",
                        "age": "0-100",
                        "rules": [
                          {
                            "units": "pg/mL",
                            "value1": "2.4",
                            "value2": "4.2",
                            "expression": "-"
                          }
                        ],
                        "expectedResults": "Nil",
                        "biomarkerNotes": "",
                        "isBiomarkerNoteAvailable": False,
                        "createdAt": "2024-01-30T06:54:49.870Z",
                        "updatedAt": "2024-04-12T06:08:01.628Z"
                      }
                    ]
                  },
                  {
                    "id": 5,
                    "name": "FT4",
                    "isActive": True,
                    "code": "FT4",
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": "",
                    "reportFormat": "Quantitative",
                    "status": "completed",
                    "createdAt": "2024-01-30T06:55:12.908Z",
                    "createdBy": 1,
                    "biomarkerConfig": [
                      {
                        "id": 6,
                        "biomarkerId": 5,
                        "gender": "male",
                        "age": "0-100",
                        "rules": [
                          {
                            "units": "pg/mL",
                            "value1": "8",
                            "value2": "18",
                            "expression": "-"
                          }
                        ],
                        "expectedResults": "Nil",
                        "biomarkerNotes": "",
                        "isBiomarkerNoteAvailable": False,
                        "createdAt": "2024-01-30T06:55:32.468Z",
                        "updatedAt": "2024-04-12T06:08:37.314Z"
                      }
                    ]
                  }
                ]
              },
              {
                "title": "germs",
                "biomarkerIds": [
                  65,
                  64
                ],
                "biomarkerDetails": [
                  {
                    "id": 65,
                    "name": "Qualitative Biomarker 2",
                    "isActive": True,
                    "code": "QAL2",
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": "ljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrtese",
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-05-10T10:14:41.045Z",
                    "createdBy": 1,
                    "biomarkerConfig": [
                      {
                        "id": 71,
                        "biomarkerId": 65,
                        "gender": "all",
                        "age": "0-100",
                        "rules": [
                          {
                            "color": "#d0021bff",
                            "units": "mg/dL",
                            "result": "Negative",
                            "value1": "1",
                            "value2": "100",
                            "expression": "-"
                          }
                        ],
                        "expectedResults": "Negative",
                        "biomarkerNotes": "",
                        "isBiomarkerNoteAvailable": False,
                        "createdAt": "2024-05-10T10:15:21.153Z",
                        "updatedAt": "2024-05-16T08:02:24.768Z"
                      }
                    ]
                  },
                  {
                    "id": 64,
                    "name": "Qualitative Biomarker 1",
                    "isActive": True,
                    "code": "QAB1",
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": "tgrefwdljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrteseljkhjguyfrtese",
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-05-10T10:11:05.732Z",
                    "createdBy": 1,
                    "biomarkerConfig": [
                      {
                        "id": 70,
                        "biomarkerId": 64,
                        "gender": "all",
                        "age": "0-100",
                        "rules": [
                          {
                            "color": "#32ff32ff",
                            "units": "mg/dL",
                            "result": "positive",
                            "value1": "1",
                            "value2": "100",
                            "expression": "-"
                          }
                        ],
                        "expectedResults": "Positive",
                        "biomarkerNotes": "",
                        "isBiomarkerNoteAvailable": False,
                        "createdAt": "2024-05-10T10:11:31.502Z",
                        "updatedAt": "2024-05-10T10:42:57.974Z"
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ],
        "icdCodes": [
          
        ],
        "isIcdCodeRequired": False,
        "createdAt": "2024-06-14T10:08:22.160Z",
        "updatedAt": "2024-06-14T10:13:51.524Z",
        "attachments": [
          
        ],
        "createdByDetails": {
          "id": 1,
          "prefix": None,
          "suffix": None,
          "firstName": "super",
          "middleName": None,
          "lastName": "admin",
          "mobileNumber": "0000000000",
          "secondaryMobileNumber": None,
          "mobileNumberCode": None,
          "faxNumber": None,
          "addressLine1": "plot no:30g,xyz colony",
          "addressLine2": None,
          "dateOfBirth": None,
          "zipcode": "99821",
          "state": "alaska",
          "city": "auke bay",
          "emailId": "superadmin@gmail.com",
          "npiNumber": None,
          "pTanNumber": None,
          "specialityType": None,
          "tinNumber": None,
          "designation": None,
          "gender": None,
          "roleId": 1,
          "roleObj": {
            "id": 1,
            "title": "Super Admin",
            "code": "superAdmin",
            "isSdiRole": True
          },
          "isSdiUser": True,
          "isPhysician": False,
          "taxonomyDetails": None,
          "isSameAddress": None,
          "isActive": True,
          "isEmailVerified": True,
          "isDeleted": False,
          "createdBy": 1,
          "isHybrid": False,
          "createdAt": "2022-09-29T20:14:23.529Z",
          "updatedAt": "2022-09-29T20:14:23.529Z"
        }
      },
      "testName": "Q",
      "testDescription": "-",
      "testDisclaimer": "<div><p><strong>Methodology: </strong>This Urinary TractInfection (UTI) molecular multiple pathogen detection testis as a Laboratory Developed Test(LDT). Utilizing multiplex2024-07-22T06:02:50.749262635Z  realtime PCR (qPCR), it specifically identifies pathogens (as listed above) present in the patient's urine specimen. The patient's urine specimen undergoes treatmentfor RNA/DNAextraction and is then processed to detect the presence of various urinary pathogens outlined in the panel (refer to above list). This process employs specific primers/probes on a realtimePCR instrument. The results are compared to contrived positive controls, internal controls, and NegativeTemplateControls (QualityControl Samples) run alongside the patient's extracted urine sample or the molecular diagnosis of urinary infections. </p><ul><li>list1</li><li>list2</li><li>list3</li></ul><p><strong> Limitations: </strong>All molecular tests have limitations. If a patient receives a 'NOT DETECTED' or 'NEGATIVE' result, itmeans thatthe pathogens mentioned in thereportwere notdetected in the specimen atthe time of sample collection. However, it's importantto note thatthis resultdoes not rule outthe possibility thatthe patient's symptoms, experienced prior to this test, may be caused by pathogens notincluded in this panel. </p><ol><li>list1</li><li>list2</li><li>list</li></ol><p><strong>Eligibility for Testing:</strong>This test should be used for diagnostic use only and is limited to patients suspected of urinary infections by their healthcare provider. The eligibility determination ultimately rests on the clinician’s judgment. </p><p><strong> Conduct of the Test:</strong>This testis performed under strict compliance and guidelines ofAdvanced Genomics LLC, including the instruments, reagents, and other recommended procedures. This includes the safety protocols where all laboratory personnel are appropriately trained in qPCR techniques and use appropriate laboratory and personal protective equipment when handling this kit/test and use this test in accordance with the authorised labeling. </p><p> <strong>Result Reports for HealthcareProviders and Patients: </strong>We have a process for reporting test results to healthcare providers as appropriate. Result reports will be provided to healthcare providers and patients. </p><p> <strong>PerformanceData and Reporting: </strong>We collect information on the performance of the test and report any suspected occurrence of False positive or False negative results and significant deviations from the established performance characteristics of the test of which we become aware to concerned authorities. </p><p><strong> Record keeping: </strong>As an authorised laboratory we ensure all records associated with this test are maintained until otherwise notified. Such records are available to </p><ul><li>list1</li><li>list2</li><li>listefkemnjnejnfjnjenknfkneinfineinfineinfineifiernivirnvirninvinrincirninqbvhbehrbvhbhbhbvhbefhibvehjbrvhbie v hibihwbv hebhibvjj evbubvnrjnvubr</li></ul></div>",
      "labCliaNumber": "1324123432",
      "labExternalId": "9999999999",
      "labAddress": "14-312, Housing board, Cold bay, Alaska, 99571",
      "labNumber": "(096) 403-3763",
      "labEmailId": "chinnasaicharan9640@gmail.com",
      "physicianLastName": "Mcmicken",
      "physicianFirstName": "Elizabeth",
      "physicianName": "Elizabeth Mcmicken",
      "physicianFaxNumber": "(803) 796-7839",
      "physicianAddress": "131 SUNSET CT, , WEST COLUMBIA, SC, 29169",
      "physicianNpiNumber": "1023538030",
      "physicianMobileNumber": "(803) 796-2222",
      "reportTemplatePath": None,
      "labDirector": "Shruthi S",
      "sampleReceivedTime": "10:16",
      "sampleReportedTime": "",
      "CHOLESTEROLValue": "-",
      "CHOLESTEROLColor": "",
      "CHOLESTEROLUnits": "",
      "CHOLESTEROLValue1": "",
      "CHOLESTEROLValue2": "",
      "CHOLESTEROLExpression": "",
      "CHOLESTEROLDescription": "",
      "CHOLESTEROLBorderColor": "",
      "LDLValue": "-",
      "LDLColor": "",
      "LDLUnits": "",
      "LDLValue1": "",
      "LDLValue2": "",
      "LDLExpression": "",
      "LDLDescription": "",
      "LDLBorderColor": "",
      "HDLValue": "-",
      "HDLColor": "",
      "HDLUnits": "",
      "HDLValue1": "",
      "HDLValue2": "",
      "HDLExpression": "",
      "HDLDescription": "",
      "HDLBorderColor": "",
      "TRIGLYCERIDEValue": "-",
      "TRIGLYCERIDEColor": "",
      "TRIGLYCERIDEUnits": "",
      "TRIGLYCERIDEValue1": "",
      "TRIGLYCERIDEValue2": "",
      "TRIGLYCERIDEExpression": "",
      "TRIGLYCERIDEDescription": "",
      "TRIGLYCERIDEBorderColor": "",
      "BilirubinValue": "-",
      "BilirubinColor": "",
      "BilirubinUnits": "",
      "BilirubinValue1": "",
      "BilirubinValue2": "",
      "BilirubinExpression": "",
      "BilirubinDescription": "",
      "BilirubinBorderColor": "",
      "CreatinineValue": "-",
      "CreatinineColor": "",
      "CreatinineUnits": "",
      "CreatinineValue1": "",
      "CreatinineValue2": "",
      "CreatinineExpression": "",
      "CreatinineDescription": "",
      "CreatinineBorderColor": "",
      "BUNValue": "-",
      "BUNColor": "",
      "BUNUnits": "",
      "BUNValue1": "",
      "BUNValue2": "",
      "BUNExpression": "",
      "BUNDescription": "",
      "BUNBorderColor": "",
      "HbA1CValue": "-",
      "HbA1CColor": "",
      "HbA1CUnits": "",
      "HbA1CValue1": "",
      "HbA1CValue2": "",
      "HbA1CExpression": "",
      "HbA1CDescription": "",
      "HbA1CBorderColor": "",
      "hsCRPValue": "-",
      "hsCRPColor": "",
      "hsCRPUnits": "",
      "hsCRPValue1": "",
      "hsCRPValue2": "",
      "hsCRPExpression": "",
      "hsCRPDescription": "",
      "hsCRPBorderColor": "",
      "VitaminDValue": "-",
      "VitaminDColor": "",
      "VitaminDUnits": "",
      "VitaminDValue1": "",
      "VitaminDValue2": "",
      "VitaminDExpression": "",
      "VitaminDDescription": "",
      "VitaminDBorderColor": "",
      "ALTValue": "-",
      "ALTColor": "",
      "ALTUnits": "",
      "ALTValue1": "",
      "ALTValue2": "",
      "ALTExpression": "",
      "ALTDescription": "",
      "ALTBorderColor": "",
      "ASTValue": "-",
      "ASTColor": "",
      "ASTUnits": "",
      "ASTValue1": "",
      "ASTValue2": "",
      "ASTExpression": "",
      "ASTDescription": "",
      "ASTBorderColor": "",
      "ALPValue": "-",
      "ALPColor": "",
      "ALPUnits": "",
      "ALPValue1": "",
      "ALPValue2": "",
      "ALPExpression": "",
      "ALPDescription": "",
      "ALPBorderColor": "",
      "TSHValue": "-",
      "TSHColor": "",
      "TSHUnits": "",
      "TSHValue1": "",
      "TSHValue2": "",
      "TSHExpression": "",
      "TSHDescription": "",
      "TSHBorderColor": "",
      "FT3Value": "-",
      "FT3Color": "",
      "FT3Units": "",
      "FT3Value1": "",
      "FT3Value2": "",
      "FT3Expression": "",
      "FT3Description": "",
      "FT3BorderColor": "",
      "FT4Value": "-",
      "FT4Color": "",
      "FT4Units": "",
      "FT4Value1": "",
      "FT4Value2": "",
      "FT4Expression": "",
      "FT4Description": "",
      "FT4BorderColor": "",
      "T3Value": "-",
      "T3Color": "",
      "T3Units": "",
      "T3Value1": "",
      "T3Value2": "",
      "T3Expression": "",
      "T3Description": "",
      "T3BorderColor": "",
      "T4Value": "-",
      "T4Color": "",
      "T4Units": "",
      "T4Value1": "",
      "T4Value2": "",
      "T4Expression": "",
      "T4Description": "",
      "T4BorderColor": "",
      "TPOValue": "-",
      "TPOColor": "",
      "TPOUnits": "",
      "TPOValue1": "",
      "TPOValue2": "",
      "TPOExpression": "",
      "TPODescription": "",
      "TPOBorderColor": "",
      "TestosteroneValue": "-",
      "TestosteroneColor": "",
      "TestosteroneUnits": "",
      "TestosteroneValue1": "",
      "TestosteroneValue2": "",
      "TestosteroneExpression": "",
      "TestosteroneDescription": "",
      "TestosteroneBorderColor": "",
      "FSHValue": "-",
      "FSHColor": "",
      "FSHUnits": "",
      "FSHValue1": "",
      "FSHValue2": "",
      "FSHExpression": "",
      "FSHDescription": "",
      "FSHBorderColor": "",
      "LHValue": "-",
      "LHColor": "",
      "LHUnits": "",
      "LHValue1": "",
      "LHValue2": "",
      "LHExpression": "",
      "LHDescription": "",
      "LHBorderColor": "",
      "SHBGValue": "-",
      "SHBGColor": "",
      "SHBGUnits": "",
      "SHBGValue1": "",
      "SHBGValue2": "",
      "SHBGExpression": "",
      "SHBGDescription": "",
      "SHBGBorderColor": "",
      "ProlactinValue": "-",
      "ProlactinColor": "",
      "ProlactinUnits": "",
      "ProlactinValue1": "",
      "ProlactinValue2": "",
      "ProlactinExpression": "",
      "ProlactinDescription": "",
      "ProlactinBorderColor": "",
      "AMHValue": "-",
      "AMHColor": "",
      "AMHUnits": "",
      "AMHValue1": "",
      "AMHValue2": "",
      "AMHExpression": "",
      "AMHDescription": "",
      "AMHBorderColor": "",
      "ProgesteroneValue": "-",
      "ProgesteroneColor": "",
      "ProgesteroneUnits": "",
      "ProgesteroneValue1": "",
      "ProgesteroneValue2": "",
      "ProgesteroneExpression": "",
      "ProgesteroneDescription": "",
      "ProgesteroneBorderColor": "",
      "DHEASValue": "-",
      "DHEASColor": "",
      "DHEASUnits": "",
      "DHEASValue1": "",
      "DHEASValue2": "",
      "DHEASExpression": "",
      "DHEASDescription": "",
      "DHEASBorderColor": "",
      "EstrogenValue": "-",
      "EstrogenColor": "",
      "EstrogenUnits": "",
      "EstrogenValue1": "",
      "EstrogenValue2": "",
      "EstrogenExpression": "",
      "EstrogenDescription": "",
      "EstrogenBorderColor": "",
      "EstradiolValue": "-",
      "EstradiolColor": "",
      "EstradiolUnits": "",
      "EstradiolValue1": "",
      "EstradiolValue2": "",
      "EstradiolExpression": "",
      "EstradiolDescription": "",
      "EstradiolBorderColor": "",
      "sampleReceivedDate": "06-14-2024",
      "patientDateOfBirth": "05-07-2024",
      "sampleCollectionDate": "06-14-2024",
      "sampleReportedDate": "07-22-2024"
    },
    "sampleId": 7247,
    "orderId": 7286,
    "source": "web",
    "sessionValueId": 5278,
    "testId": 41,
    "testCode": "QQQQ",
    "patientId": 110386,
    "shouldReply": True,
    "queueName": "pdfgeneratedresponsejobs",
    "themeColor": "#315824ff",
    "logo": "113/logo/fc649be9-85e2-4f35-a705-0de59493538d-download.jpeg"
  } 

data2={
    "password": "01-01-1970",
    "replaceVariables": {
      "layoutCode": "layout1",
      "patientLastName": "Female patient",
      "patientFirstName": "Wsdi",
      "patientName": "Wsdi Female patient",
      "password": "01-01-1970",
      "accessionId": "LAQ1-729444",
      "patientGender": "female",
      "patientMobileNumber": "(999) 999-9999",
      "patientAge": 54,
      "patientAddress": "EL PASO, , Canutillo, Texas, 79835",
      "patientId": 1268,
      "sampleCollectionTime": "12:05",
      "patientEmailId": "wsdifemalepatient@gmail.com",
      "sampleResult": {
        "barcode": {
          "value": "LAQ1-729444"
        },
        "TESTINGPDF  Qualitative 1": {
          "value": "POSITIVE"
        },
        "TESTINGPDF  Qualitative 2": {
          "value": "POSITIVE"
        },
        "TESTINGPDF  Qualitative 3": {
          "value": "NEGATIVE"
        },
        "TESTINGPDF  Qualitative 4": {
          "value": "NEGATIVE"
        },
        "TESTINGPDF  Qualitative 5": {
          "value": "POSITIVE"
        },
        "TESTINGPDF  Qualitative 6": {
          "value": "POSITIVE"
        },
        "TESTINGPDF  Qualitative 7": {
          "value": "NEGATIVE"
        },
        "TESTINGPDF  Qualitative 8": {
          "value": "NEGATIVE"
        },
        "TESTINGPDF  Qualitative 9": {
          "value": "POSITIVE"
        },
        "TESTINGPDF  Qualitative 10": {
          "value": "POSITIVE"
        },
        "TESTINGPDF  Qualitative 11": {
          "value": "NEGATIVE"
        },
        "TESTINGPDF  Qualitative 12": {
          "value": "NEGATIVE"
        },
        "TESTINGPDF  Qualitative 13": {
          "value": "POSITIVE"
        },
        "TESTINGPDF  Qualitative 14": {
          "value": "POSITIVE"
        },
        "TESTINGPDF  Qualitative 15": {
          "value": "NEGATIVE"
        },
        "TESTINGPDF  Qualitative 16": {
          "value": "NEGATIVE"
        },
        "TESTINGPDF  Qualitative 17": {
          "value": "POSITIVE"
        },
        "TESTINGPDF  Qualitative 18": {
          "value": "POSITIVE"
        },
        "TESTINGPDF  Qualitative 19": {
          "value": "NEGATIVE"
        },
        "TESTINGPDF  Qualitative 20": {
          "value": "NEGATIVE"
        },
        "TESTINGPDF  Qualitative 21": {
          "value": "POSITIVE"
        },
        "TESTINGPDF  Qualitative 22": {
          "value": "POSITIVE"
        },
        "TESTINGPDF  Qualitative 23": {
          "value": "NEGATIVE"
        },
        "TESTINGPDF  Qualitative 24": {
          "value": "NEGATIVE"
        },
        "TESTINGPDF  Qualitative 25": {
          "value": "POSITIVE"
        },
        "TESTINGPDF  Qualitative 26": {
          "value": "POSITIVE"
        }
      },
      "sampleType": "Blood",
      "orderId": "GK1513",
      "sampleResultColor": "000000",
      "finalResultObject": [
        {
          "testName": "qual lay1",
          "resultValue": "POSITIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#5a9759ff",
            "fontWeight": "normal",
            "qualitativeResultValue": "POSITIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 1",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "POSITIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "POSITIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#5a9759ff",
            "fontWeight": "normal",
            "qualitativeResultValue": "POSITIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 2",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "POSITIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "NEGATIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#F45863",
            "fontWeight": "normal",
            "qualitativeResultValue": "NEGATIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 3",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "NEGATIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "NEGATIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#F45863",
            "fontWeight": "normal",
            "qualitativeResultValue": "NEGATIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 4",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "NEGATIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "POSITIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#5a9759ff",
            "fontWeight": "normal",
            "qualitativeResultValue": "POSITIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 5",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "POSITIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "POSITIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#5a9759ff",
            "fontWeight": "normal",
            "qualitativeResultValue": "POSITIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 6",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "POSITIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "NEGATIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#F45863",
            "fontWeight": "normal",
            "qualitativeResultValue": "NEGATIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 7",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "NEGATIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "NEGATIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#F45863",
            "fontWeight": "normal",
            "qualitativeResultValue": "NEGATIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 8",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "NEGATIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "POSITIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#5a9759ff",
            "fontWeight": "normal",
            "qualitativeResultValue": "POSITIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 9",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "POSITIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "POSITIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#5a9759ff",
            "fontWeight": "normal",
            "qualitativeResultValue": "POSITIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 10",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "POSITIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "NEGATIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#F45863",
            "fontWeight": "normal",
            "qualitativeResultValue": "NEGATIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 11",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "NEGATIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "NEGATIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#F45863",
            "fontWeight": "normal",
            "qualitativeResultValue": "NEGATIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 12",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "NEGATIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "POSITIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#5a9759ff",
            "fontWeight": "normal",
            "qualitativeResultValue": "POSITIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 13",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "POSITIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "POSITIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#5a9759ff",
            "fontWeight": "normal",
            "qualitativeResultValue": "POSITIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 14",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "POSITIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "NEGATIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#F45863",
            "fontWeight": "normal",
            "qualitativeResultValue": "NEGATIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 15",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "NEGATIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "NEGATIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#F45863",
            "fontWeight": "normal",
            "qualitativeResultValue": "NEGATIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 16",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "NEGATIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "POSITIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#5a9759ff",
            "fontWeight": "normal",
            "qualitativeResultValue": "POSITIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 17",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "POSITIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "POSITIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#5a9759ff",
            "fontWeight": "normal",
            "qualitativeResultValue": "POSITIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 18",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "POSITIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "NEGATIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#F45863",
            "fontWeight": "normal",
            "qualitativeResultValue": "NEGATIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 19",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "NEGATIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "NEGATIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#F45863",
            "fontWeight": "normal",
            "qualitativeResultValue": "NEGATIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 20",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "NEGATIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "POSITIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#5a9759ff",
            "fontWeight": "normal",
            "qualitativeResultValue": "POSITIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 21",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "POSITIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "POSITIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#5a9759ff",
            "fontWeight": "normal",
            "qualitativeResultValue": "POSITIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 22",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "POSITIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "NEGATIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#F45863",
            "fontWeight": "normal",
            "qualitativeResultValue": "NEGATIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 23",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "NEGATIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "NEGATIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#F45863",
            "fontWeight": "normal",
            "qualitativeResultValue": "NEGATIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 24",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "NEGATIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "POSITIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#5a9759ff",
            "fontWeight": "normal",
            "qualitativeResultValue": "POSITIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 25",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "POSITIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        },
        {
          "testName": "qual lay1",
          "resultValue": "POSITIVE",
          "rule": [
            
          ],
          "fontFormat": {
            "color": "#5a9759ff",
            "fontWeight": "normal",
            "qualitativeResultValue": "POSITIVE",
            "borderColor": "#000000"
          },
          "biomarkerName": "TESTINGPDF  Qualitative 26",
          "biomarkerDescription": None,
          "reportFormat": "Qualitative",
          "qualitativeResultValue": "POSITIVE",
          "biomarkerNote": "",
          "expectedResults": ""
        }
      ],
      "testDetails": {
        "id": 112,
        "name": "qual lay1",
        "code": "LAQ1",
        "sampleType": "blood",
        "sampleCollectionDeviceName": "tube",
        "sampleQuantity": "1234",
        "description": None,
        "createdBy": 2,
        "isIntakeFormRequired": False,
        "formId": None,
        "isStateReportingRequired": False,
        "stateReporting": None,
        "isBulkImportRequired": False,
        "isActive": True,
        "biomarkerIds": [
          239,
          240,
          241,
          243,
          242,
          244,
          245,
          246,
          247,
          248,
          249,
          250,
          251,
          252,
          253,
          254,
          255,
          256,
          257,
          258,
          259,
          260,
          261,
          262,
          263,
          264
        ],
        "status": "completed",
        "chatId": None,
        "lastBarcodeCount": None,
        "resultingMode": "manual upload",
        "processOverView": None,
        "kitComponents": None,
        "kitImages": None,
        "questions": None,
        "videoUrl": None,
        "kitRedirectUrl": None,
        "normalPdfTemplatePath": None,
        "abnormalPdfTemplatePath": None,
        "testLayoutDetails": [
          {
            "layout": "layout1",
            "disclaimer": "<div><p>Methodology: Advanced Genomics Laboratory RPP (Respiratory Pathogen Panel) test is a laboratory developed test. It is a real time RT¬PCR which specifically detects pathogens listed on the report in patient's specimens. Patient's nasopharyngeal swab is treated to extract RNA/DNA and processed to detect the presence of various respiratory pathogens listed on the panel using specific primers on a real time PCR machine. The results are compared to contrive positive controls, Internal controls, and Negative Template Controls (Quality Control Samples) run alongside the patient’s samples for the diagnosis of respiratory infections. </p><p>Limitations: All molecular tests have limitations. If a patient is found 'NOT DETECTED or NEGATIVE' implies that he/she is not infected with the list of pathogens mentioned in the report at the sample collection time. On the other hand, this does not discount the fact that the patient having symptoms before this test may be due to the pathogens beyond the scope of Advanced Genomics Laboratory RPP Panel. </p><p>Laboratory Statement: This test was performed, validated and performance characteristics have been determined by Advanced Genomics, 10750 Hammerly Blvd #120, Houston, TX 77043, CLIA(#45D0292474), Laboratory Director, Dr. Alexis McBrayer. This test is used for clinical purposes (see Eligibility for testing). Its use should not be regarded as investigational or for research and tests only the listed pathogens on the report. Hence, we strongly recommend undergoing this test when the patient experiences symptoms consistent with infectious respiratory disease etiology with the clinician's advice and prescription. This laboratory is certified under Clinical Laboratory Improvements and Amendments of 1988 (CLIA 88) as qualified to perform high complexity clinical laboratory testing. This test has not been cleared or approved by the FDA. The FDA has determined that such approval is not necessary, provided that the laboratory both (1) maintains its good standing as a clinical testing laboratory with all mandatory accrediting bodies, and (2) continually demonstrates that its testing protocols and procedures achieve a high degree of analytical accuracy. Medication Recommendations/pharmacy guidance are given for information purpose only. The final prescription is given by the physician will be given based on patient’s clinical history and correlation. Advanced Genomics Laboratory is not responsible for adverse drug reactions if the patient takes medications based on the guidelines provided without physician's prescription. Final medications are under physician's discretion.</p><p>Eligibility for Testing: This test is prescription use only and is limited to patients suspected of respiratory infections by their healthcare provider. The eligibility determination ultimately rests on the clinician's judgment. </p><p>Conduct of the Test: This test is performed under strict compliance and guidelines of Advanced Genomics Laboratory R&D team, including the use of instruments, reagents, and other recommended procedures. This includes the safety protocols where all laboratory personnel are appropriately trained in RT qPCR techniques and use appropriate laboratory and personal protective equipment when handling this kit/test and use this test in accordance with the authorized labeling. </p><p>Result Reports for Healthcare Providers and Patients: We have a process for reporting test results to healthcare providers as appropriate. Result reports will be provided to healthcare providers and patients. </p><p>Performance Data and Reporting: We collect information on the performance of the test and report any suspected occurrence of False positive or False negative results and significant deviations from the established performance characteristics of the test of which we become aware to concerned authorities. </p><p></p></div>",
            "biomarkerObj": [
              {
                "title": "",
                "biomarkerIds": [
                  239,
                  240,
                  241,
                  243,
                  242,
                  244,
                  245,
                  246,
                  247,
                  248,
                  249,
                  250,
                  251,
                  252,
                  253,
                  254,
                  255,
                  256,
                  257,
                  258,
                  259,
                  260,
                  261,
                  262,
                  263,
                  264
                ],
                "biomarkerDetails": [
                  {
                    "id": 239,
                    "name": "TESTINGPDF  Qualitative 1",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.469Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 240,
                    "name": "TESTINGPDF  Qualitative 2",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.501Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 241,
                    "name": "TESTINGPDF  Qualitative 3",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.541Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 242,
                    "name": "TESTINGPDF  Qualitative 4",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.561Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 243,
                    "name": "TESTINGPDF  Qualitative 5",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.594Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 244,
                    "name": "TESTINGPDF  Qualitative 6",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.633Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 245,
                    "name": "TESTINGPDF  Qualitative 7",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.648Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 246,
                    "name": "TESTINGPDF  Qualitative 8",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.668Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 247,
                    "name": "TESTINGPDF  Qualitative 9",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.682Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 248,
                    "name": "TESTINGPDF  Qualitative 10",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.690Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 249,
                    "name": "TESTINGPDF  Qualitative 11",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.722Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 250,
                    "name": "TESTINGPDF  Qualitative 12",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.743Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 251,
                    "name": "TESTINGPDF  Qualitative 13",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.749Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 252,
                    "name": "TESTINGPDF  Qualitative 14",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.765Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 253,
                    "name": "TESTINGPDF  Qualitative 15",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.772Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 254,
                    "name": "TESTINGPDF  Qualitative 16",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.817Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 255,
                    "name": "TESTINGPDF  Qualitative 17",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.819Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 256,
                    "name": "TESTINGPDF  Qualitative 18",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.833Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 257,
                    "name": "TESTINGPDF  Qualitative 19",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.851Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 258,
                    "name": "TESTINGPDF  Qualitative 20",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.872Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 259,
                    "name": "TESTINGPDF  Qualitative 21",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.887Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 260,
                    "name": "TESTINGPDF  Qualitative 22",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.902Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 261,
                    "name": "TESTINGPDF  Qualitative 23",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.919Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 262,
                    "name": "TESTINGPDF  Qualitative 24",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.932Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 263,
                    "name": "TESTINGPDF  Qualitative 25",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.955Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  },
                  {
                    "id": 264,
                    "name": "TESTINGPDF  Qualitative 26",
                    "isActive": True,
                    "code": None,
                    "sampleType": "blood",
                    "sampleCollectionDeviceName": "tube",
                    "description": None,
                    "reportFormat": "Qualitative",
                    "status": "completed",
                    "createdAt": "2024-08-09T06:22:05.982Z",
                    "createdBy": None,
                    "isConfigurationRequired": False
                  }
                ]
              }
            ]
          }
        ],
        "icdCodes": [
          
        ],
        "isIcdCodeRequired": False,
        "createdAt": "2024-08-09T06:23:01.727Z",
        "updatedAt": "2024-08-09T06:23:43.459Z",
        "attachments": [
          
        ],
        "createdByDetails": {
          "id": 2,
          "prefix": None,
          "suffix": None,
          "firstName": "super",
          "middleName": "",
          "lastName": "super",
          "mobileNumber": "0000000000",
          "secondaryMobileNumber": None,
          "mobileNumberCode": "super",
          "faxNumber": "",
          "addressLine1": "plot no:30g,xyz colony",
          "addressLine2": "",
          "dateOfBirth": None,
          "zipcode": "99821",
          "state": "alaska",
          "city": "auke bay",
          "emailId": "superadmin@gmail.com",
          "npiNumber": "",
          "pTanNumber": None,
          "specialityType": None,
          "tinNumber": None,
          "designation": "md",
          "gender": None,
          "roleId": 1,
          "roleObj": {
            "id": 1,
            "title": "Super Admin",
            "code": "superAdmin",
            "isSdiRole": True
          },
          "isSdiUser": True,
          "isPhysician": False,
          "taxonomyDetails": None,
          "isSameAddress": None,
          "isActive": True,
          "isEmailVerified": True,
          "isDeleted": False,
          "createdBy": 1,
          "isHybrid": False,
          "createdAt": "2022-09-29T20:14:23.529Z",
          "updatedAt": "2022-10-01T07:31:27.488Z"
        }
      },
      "testName": "qual lay1",
      "testDescription": "-",
      "testDisclaimer": "<div><p>Methodology: Advanced Genomics Laboratory RPP (Respiratory Pathogen Panel) test is a laboratory developed test. It is a real time RT¬PCR which specifically detects pathogens listed on the report in patient's specimens. Patient's nasopharyngeal swab is treated to extract RNA/DNA and processed to detect the presence of various respiratory pathogens listed on the panel using specific primers on a real time PCR machine. The results are compared to contrive positive controls, Internal controls, and Negative Template Controls (Quality Control Samples) run alongside the patient’s samples for the diagnosis of respiratory infections. </p><p>Limitations: All molecular tests have limitations. If a patient is found 'NOT DETECTED or NEGATIVE' implies that he/she is not infected with the list of pathogens mentioned in the report at the sample collection time. On the other hand, this does not discount the fact that the patient having symptoms before this test may be due to the pathogens beyond the scope of Advanced Genomics Laboratory RPP Panel. </p><p>Laboratory Statement: This test was performed, validated and performance characteristics have been determined by Advanced Genomics, 10750 Hammerly Blvd #120, Houston, TX 77043, CLIA(#45D0292474), Laboratory Director, Dr. Alexis McBrayer. This test is used for clinical purposes (see Eligibility for testing). Its use should not be regarded as investigational or for research and tests only the listed pathogens on the report. Hence, we strongly recommend undergoing this test when the patient experiences symptoms consistent with infectious respiratory disease etiology with the clinician's advice and prescription. This laboratory is certified under Clinical Laboratory Improvements and Amendments of 1988 (CLIA 88) as qualified to perform high complexity clinical laboratory testing. This test has not been cleared or approved by the FDA. The FDA has determined that such approval is not necessary, provided that the laboratory both (1) maintains its good standing as a clinical testing laboratory with all mandatory accrediting bodies, and (2) continually demonstrates that its testing protocols and procedures achieve a high degree of analytical accuracy. Medication Recommendations/pharmacy guidance are given for information purpose only. The final prescription is given by the physician will be given based on patient’s clinical history and correlation. Advanced Genomics Laboratory is not responsible for adverse drug reactions if the patient takes medications based on the guidelines provided without physician's prescription. Final medications are under physician's discretion.</p><p>Eligibility for Testing: This test is prescription use only and is limited to patients suspected of respiratory infections by their healthcare provider. The eligibility determination ultimately rests on the clinician's judgment. </p><p>Conduct of the Test: This test is performed under strict compliance and guidelines of Advanced Genomics Laboratory R&D team, including the use of instruments, reagents, and other recommended procedures. This includes the safety protocols where all laboratory personnel are appropriately trained in RT qPCR techniques and use appropriate laboratory and personal protective equipment when handling this kit/test and use this test in accordance with the authorized labeling. </p><p>Result Reports for Healthcare Providers and Patients: We have a process for reporting test results to healthcare providers as appropriate. Result reports will be provided to healthcare providers and patients. </p><p>Performance Data and Reporting: We collect information on the performance of the test and report any suspected occurrence of False positive or False negative results and significant deviations from the established performance characteristics of the test of which we become aware to concerned authorities. </p><p></p></div>",
      "labCliaNumber": "05D2274791",
      "labExternalId": "CLF-90008537",
      "labAddress": "12636 Hoover Street, , Garden grove, California, 92841",
      "labNumber": "(714) 868-5000",
      "labEmailId": "support@wisdi.org",
      "physicianLastName": "Patel",
      "physicianFirstName": "Kuntal",
      "physicianName": "Kuntal Patel",
      "physicianFaxNumber": "-",
      "physicianAddress": "142 E MAIN ST, , SPARTANBURG, SC, 29306",
      "physicianNpiNumber": "1467826875",
      "physicianMobileNumber": "(864) 237-5501",
      "reportTemplatePath": None,
      "labDirector": "Dr. fan M.d",
      "sampleReceivedTime": "06:39",
      "sampleReportedTime": "",
      "sampleReceivedDate": "08-09-2024",
      "patientDateOfBirth": "01-01-1970",
      "sampleCollectionDate": "08-09-2024",
      "sampleReportedDate": "08-09-2024",
      "themeColor": "#f17013ff",
      "logo": "https://tericsoftsdigkv2.blob.core.windows.net/lab-attachments/1712121115/logo/52fc2080-fca4-444b-b1f5-510520886a5c-1.jpeg"
    },
    "sampleId": 1594,
    "orderId": 1513,
    "source": "web",
    "sessionValueId": 942,
    "testId": 112,
    "testCode": "LAQ1",
    "patientId": 1268,
    "shouldReply": True,
    "queueName": "pdfgeneratedresponsejobs",
    "themeColor": "#f17013ff",
    "logo": "1712121115/logo/52fc2080-fca4-444b-b1f5-510520886a5c-1.jpeg"
  }


@app.route('/')
def index():
    
    template = env.get_template('sdi.html')
        
    # Render the template with data
    rendered_html = template.render(data=data2).encode(encoding="UTF-8")
    return rendered_html

@app.route('/print', methods=['POST'])
def print_pdf():
    try:
        request_data = request.get_json()
        if not request_data:
            logging.error("No JSON data provided in request.")
            return jsonify(error="No JSON data provided in request."), 400

        logging.info("Request data received: %s", request_data)
        
        # Load the template
        template = env.get_template('sdi.html')
        
        print(request_data.get("password"))
        # Render the template with data
        rendered_html = template.render(data=request_data).encode(encoding="UTF-8")
        
        # Create a PDF from the rendered HTML
        pdf = HTML(string=rendered_html, encoding="UTF-8").write_pdf()
        
        # Encrypt the PDF
        pdf_reader = PdfReader(io.BytesIO(pdf))
        pdf_writer = PdfWriter()

        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])
        
        password = request_data.get("password")
        if not password:
            logging.error("Password not provided in request data.")
            return jsonify(error="Password not provided in request data."), 400

        pdf_writer.encrypt(password)
        
        encrypted_pdf_stream = io.BytesIO()
        pdf_writer.write(encrypted_pdf_stream)
        encrypted_pdf_stream.seek(0)

        # Prepare response for encrypted PDF
        encrypted_pdf_response = make_response(encrypted_pdf_stream.getvalue())
        encrypted_pdf_response.headers['Content-Type'] = 'application/pdf'
        encrypted_pdf_response.headers['Content-Disposition'] = 'inline; filename=sdi_encrypted.pdf'

        logging.info("PDF successfully created and encrypted.")
        return encrypted_pdf_response

    except TemplateNotFound:
        logging.error("Template not found.")
        return jsonify(error="Template not found."), 404
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return jsonify(error="An internal error occurred."), 500



@app.route('/print-testing')
def print_pdf2():
    try:
        # request_data = request.get_json()
        
        # Load the template
        template = env.get_template('sdi.html')
        
        # Render the template with data
        rendered_html = template.render(data=data2).encode(encoding="UTF-8")
        
        # Create a PDF from the rendered HTML
        pdf = HTML(string=rendered_html, encoding="UTF-8").write_pdf()
        
        # Save the normal PDF locally
        with open("sdi.pdf", "wb") as f:
            f.write(pdf)
        
        # Encrypt the PDF
        pdf_reader = PdfReader(io.BytesIO(pdf))
        pdf_writer = PdfWriter()

        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])
        
        password = "your_password"  # Set your password here
        pdf_writer.encrypt(password)
        
        encrypted_pdf_stream = io.BytesIO()
        pdf_writer.write(encrypted_pdf_stream)
        encrypted_pdf_stream.seek(0)
        
        # Save the encrypted PDF locally
        with open("sdi_encrypted.pdf", "wb") as f:
            f.write(encrypted_pdf_stream.getvalue())

        return jsonify(message="PDFs generated and saved locally."), 200

    except TemplateNotFound:
        logging.error("Template not found.")
        return jsonify(error="Template not found."), 404
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify(error="An internal error occurred."), 500



@app.route('/ping', methods=["GET"])
def ping():
    return "Ping pong python print service"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

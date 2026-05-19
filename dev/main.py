import os
from datetime import date
from functools import wraps
from flask import Flask, render_template, redirect, url_for, flash, Response, jsonify, request, send_from_directory
import psycopg
import openpyxl
import pandas as pd
from sqlalchemy import create_engine, inspect
from flask_login import login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid
from openpyxl.styles import Font
from flask import send_file
import io
# from weasyprint import HTML
import boto3
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')



@app.route('/')
def home():
    return render_template("index.html")


if __name__ == "__main__":
    # app.run(debug=app.config.get("DEBUG", False), port=5002)
    app.run(host="0.0.0.0", port=5002, debug=app.config.get("DEBUG", False))

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
from dev.db.db_create import create_db, create_table
from dev.db.db_client import DBClient

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

create_db()
create_table()


def get_cottage_info():
    db_client = DBClient()
    row = db_client.get_cottage_info_from_db()
    return {
            "cottage_id": row[0],
            "nickname": row[1],
            "nightly_rate": row[2],
            "capacity": row[3],
            "status": row[4]
        }

@app.route('/api/cottage-info', methods=['GET'])
def fetch_cottage_info():
    cottage_info = get_cottage_info()
    return jsonify({
        "message": "Cottage info returned successfully",
        "cottage_info": cottage_info
    })


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/submit_booking", methods=["GET", "POST"])
def submit_booking():
    if request.method == "POST":
        booking_details = []
        full_name = request.form["name"]
        email = request.form["email"]
        checkin_date = request.form["checkin"]
        checkout_date = request.form["checkout"]
        number_of_guests = request.form["guests"]
        special_requests = request.form["special-requests"]
        total_price = request.form["total_price"]
        cottage_nickname = request.form["cottage_nickname"]
        booking_details.extend([full_name, email, checkin_date, checkout_date,
                                number_of_guests, special_requests, total_price, 'confirmed'])
        db_client = DBClient()
        new_booking = db_client.add_booking_to_db(booking_details)
        return render_template("confirmation.html", booking_details=new_booking,
                               cottage_nickname=cottage_nickname)


if __name__ == "__main__":
    # app.run(debug=app.config.get("DEBUG", False), port=5002)
    app.run(host="0.0.0.0", port=5002, debug=app.config.get("DEBUG", False))

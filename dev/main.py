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
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


def init_db():
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


@app.get("/api/availability")
def get_availability():
    checkin = datetime.strptime(
        request.args["checkin"],
        "%Y-%m-%d"
    ).date()

    checkout = datetime.strptime(
        request.args["checkout"],
        "%Y-%m-%d"
    ).date()

    db_client = DBClient()
    results = db_client.get_availability(
        checkin,
        checkout
    )

    return jsonify(results)


def get_booking(booking_id):
    db_client = DBClient()
    row = db_client.get_booking(booking_id)
    return {
        "booking_id": row[0],
        "full_name": row[1],
        "email": row[2],
        "checkin_date": row[3],
        "checkout_date": row[4],
        "number_of_guests": row[5],
        "special_requests": row[6],
        "total_price": row[7],
        "status": row[8]
    }


@app.route('/api/add_reservation', methods=['POST'])
def add_reservation():
    db_client = DBClient()
    try:
        # print("Raw request data:", request.data)
        data = request.get_json(force=True)
        # print("Parsed data:", data)

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        reservation_details = []
        full_name = data['full_name']
        email = data['email']
        checkin = data['checkin']
        checkout = data['checkout']
        number_of_guests = data['number_of_guests']
        special_requests = data['special_requests']
        price = data['price']
        status = data['status']

        reservation_details.extend([full_name, email, checkin, checkout, number_of_guests,
                                    special_requests, price, status])


        new_reservation = db_client.add_booking_to_db(reservation_details)


        return jsonify({"message": "Booking added successfully",
                        "booking": {
                            "id": new_reservation[0],
                            "full_name": new_reservation[1],
                            "email": new_reservation[2],
                            "checkin": new_reservation[3],
                            "checkout": new_reservation[4],
                            "number_of_guests": new_reservation[5],
                            "special_requests": new_reservation[6],
                            "price": new_reservation[7],
                            "status": new_reservation[8]
                        }
                        }), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/api/get_reservation_by_booking_id/<int:booking_id>', methods=['GET'])
def fetch_booking(booking_id):
    booking = get_booking(booking_id)
    return jsonify({
        "message": "Booking returned successfully",
        "booking": booking
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
        if isinstance(new_booking[0], int):
            return render_template("confirmation.html", booking_details=new_booking,
                                   cottage_nickname=cottage_nickname)
        else:
            flash("1 or more dates not available")
            return redirect(url_for('home'))


if __name__ == "__main__":
    init_db()
    # app.run(debug=app.config.get("DEBUG", False), port=5002)
    app.run(host="0.0.0.0", port=5002, debug=app.config.get("DEBUG", False))

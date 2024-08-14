from flask import Blueprint, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def hello_world():
    return redirect(url_for('static', filename='./index.html'))
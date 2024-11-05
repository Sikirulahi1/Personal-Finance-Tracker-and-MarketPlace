from flask import Flask, Blueprint, render_template

marketplace = Blueprint('marketplace', __name__, template_folder = 'templates')

@marketplace.route('/')
def index():
    return render_template('marketplace/index.html')
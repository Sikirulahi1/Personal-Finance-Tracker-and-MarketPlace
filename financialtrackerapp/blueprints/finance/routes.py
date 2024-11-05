from flask import Flask, Blueprint, render_template

finance = Blueprint('finance', __name__, template_folder = 'templates')

@finance.route('/')
def index():
    return render_template('finance/index.html')
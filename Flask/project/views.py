from flask import Blueprint,render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/contact')
def contact():
    return render_template("contact.html")

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/index')
@login_required
def index():
    return render_template("index.html", user=current_user)
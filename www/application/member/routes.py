import os
from flask import Blueprint, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory, render_template
from flask import current_app
from flask_login import login_required, current_user

from application.member.content import get_content

app = current_app

# Blueprint Configuration
member_bp = Blueprint('member_bp', __name__, template_folder='templates')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@member_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

# >>> for f in request.files.getlist('photo'):

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # check directory
            target_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], current_user.name)
            if not os.path.exists(target_path):
                os.makedirs(target_path)

            # save file
            file.save(os.path.join(target_path, filename))

            # return redirect(url_for('member_bp.download_file', name=filename))
            return redirect(url_for('member_bp.dashboard'))
    return render_template('upload.html')


@member_bp.route('/upload/<name>')
@login_required
def download_file(name):
    return send_from_directory(os.path.join(app.config["UPLOAD_FOLDER"], current_user.name), name)


@member_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard.html',
        title='Tableau de bord',
        current_user=current_user,
        body="Votre contenu est ci-dessous :",
        content=get_content(current_user)
    )

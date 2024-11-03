from flask import render_template
from app.modules.socialmodule import socialmodule_bp


@socialmodule_bp.route('/socialmodule', methods=['GET'])
def index():
    return render_template('socialmodule/index.html')

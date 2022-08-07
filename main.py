from flask import *
from flask_bootstrap import Bootstrap
from PIL import Image
from colorthief import ColorThief
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
Bootstrap(app)

save_dir1 = os.path.join('static/assets/images')


@app.route('/', methods=['GET', 'POST'])
def home():
    current_image = "static/assets/images/mountain-01.jpg"
    ct = ColorThief(current_image)
    palette = ct.get_palette(color_count=11)

    if request.method == 'POST':

        if request.files['file'].filename == '':
            flash('No file selected')
            return redirect(url_for('home', image=current_image, colors=palette))
        else:
            data = request.files['file']
            data.save(os.path.join(save_dir1, secure_filename(data.filename)))
            num_colors = int(request.form['num_colors'])
            ct = ColorThief(f"static/assets/images/{data.filename}")
            new_img = f"static/assets/images/{data.filename}"
            palette = ct.get_palette(color_count=num_colors)
            return render_template('index.html', image=new_img, colors=palette)

    return render_template('index.html', image=current_image, colors=palette)


if __name__ == "__main__":
    app.run(debug=True)

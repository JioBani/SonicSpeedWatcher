from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def index():
        return render_template('view_data.html')

@app.route('/view_data')
def view_data():
        return render_template('view_data.html')

@app.route('/setting')
def setting():
        return render_template('setting.html')

@app.route('/view_with_image' , methods=['GET', 'POST'])
def view_with_image():
        return render_template('view_with_image.html')

@app.route('/test')
def test():
        return render_template('test.html')


if __name__ == "__main__":
        app.run(host='0.0.0.0', port=8080)
from flask import Flask, render_template, request
app = Flask(__name__)

#. 루트
@app.route('/')
def index():
        return render_template('view_data.html')

#.데이터 리스트 조회
@app.route('/view_data')
def view_data():
        return render_template('view_data.html')

#. 데이터 및 이미지 조회
@app.route('/view_with_image' , methods=['GET', 'POST'])
def view_with_image():
        #. form 에서 가져온 데이터를 바탕으로 사진의 경로를 보내줌
        if(request.method == 'POST'):
                print(request.form['enterTime'])
                if( request.form['isSpeeding']):
                        isSpeeding = "과속"
                else:
                        isSpeeding = ""

                return render_template(
                        'view_with_image.html',
                        enterTime = request.form['enterTime'],
                        exitTime = request.form['exitTime'],
                        passingTime = request.form['passingTime'],
                        velocity = request.form['velocity'],
                        imagePath = request.form['imagePath'],
                        isSpeeding = isSpeeding
                                       )
        else:
                return render_template('view_with_image.html')

#. 전광판
@app.route('/velocity')
def velocity():
        return render_template('velocity.html')

#. 데이터 통계
@app.route('/statistics')
def statistics():
        return render_template('statistics.html')

@app.route('/test')
def test():
        return render_template('test.html')


if __name__ == "__main__":
        app.run(host='0.0.0.0', port=8080)
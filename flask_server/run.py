from web import app
import os

# docker build . -t flask_app_dev
# docker run -p 5000:5000 -e DEBUG=1 flask_app_dev
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=os.environ.get('DEBUG') == '1')

from application.log_parser import app
import application.log_parser.api

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
from flask import Flask


tankServer = Flask(__name__)

@tankServer.route("/")
def main():
    return "Deez nuts"

if __name__ == "__main__":
    tankServer.run(debug=True, host="0.0.0.0", port=5000)

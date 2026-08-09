from flask import Flask, render_template, request, jsonify
from static.py import CMD as cmd
from static.py import Input as inp
import os

app = Flask(__name__)
db = inp.Database(os.getcwd())
db.create_table()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/adjust-brightness', methods=['POST'])
def adjust_brightness():
  brightness_level = request.form.get('brightness-level')
  cli = cmd.Cli(brightness_level=brightness_level)
  # check if the input is valid input
  if not cli:
    return jsonify(
      {
        "status": 500
      }
    )

  # check if there is a recorded sudo password
  passwd = db.get_password()
  if passwd is None:
    return jsonify(
      {
        "status": 404
      }
    )
  if db.get_password and cli:
    password =  db.get_password()[0]
    cli.change_the_brightness(password=password)
    return jsonify({
      "status": 200
    })

@app.route('/rec_sudo', methods=['POST'])
def rec_sudo():
  user_password = request.form.get('user-password')
  valid = inp.Input_validator(brightness_level=1).valid_sudo(password=user_password)
  if not (valid):
      return jsonify({
        "status": "error", 
        "message": "Incorrect sudo password!"
      })

  db.reg_password(user_password)
  return jsonify({
    "status": 200
  })
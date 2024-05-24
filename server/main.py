"""
Module 3: Flask App
"""
from flask import Flask, jsonify, request, abort, url_for, redirect, make_response
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from flask_cors import CORS
from user import User
from db import DB

app = Flask(__name__)
CORS(app, origins="*")
AUTH = Auth()
database = DB()


@app.route("/", methods=["GET"])
def message():
    """
    simple endpoint
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_users():
    """
    endpoint to register user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    user = AUTH.register_user(email=email, password=password)
    if user:
        return jsonify({"email": email,
                    "message": f"User {email} created"}), 200
    else:
        return jsonify({"email": f"User {email} exists"}), 200


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    login endpoint to implement sessions
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        res = make_response(jsonify({"email": email,
                      "message": f"logged in {session_id}"}))
        res.set_cookie("session_id", session_id)
        return res
    else:
        return jsonify({"res": "Email or password incorrect"})


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def log_out():
    """
    delete session
    """
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for("message"))


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """
    profile function
    """
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """
    """
    email = request.form.get("email")
    if email is None:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """
    update password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    if email is None:
        abort(403)
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email,
                        "message": "Password updated"}), 200
    except ValueError:
        abort(403)

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorized(error) -> str:
    """
    Not authorized
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    User forbidden
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    email = "koomemc@gmail.com"
    user = User(email=email, hashed_password="123444")
    result = database.find_user(email=email)
    print(result)
    app.run(host="0.0.0.0", port="5000")

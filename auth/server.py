import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

server.router("/login", methods=["POST"])


def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email = %s", (auth.email,)
    )
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.email != email and auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.email, os.environ.get("JWT_SECRET"), True)
    else:
        return "user not found", 404


server.router("/validate", methods=["POST"])


def validate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "missing token", 401
    token = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return "expired token", 401
    except jwt.InvalidTokenError:
        return "invalid token", 401
    return decoded, 200


def createJWT(email, secret, is_admin):
    payload = {
        "email": email,
        "admin": is_admin,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)

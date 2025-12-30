# from flask import Flask, render_template, request, redirect, url_for,jsonify
# import pyodbc

# app = Flask(__name__)

# # Database connection string
# conn_str = (
#     "Driver={ODBC Driver 17 for SQL Server};"
#     "Server=SRMUMATBU10;"
#     "Database=YEDP2024;"
#     "Trusted_Connection=yes;"
# )
# # conn_str = (
# #     "Driver={ODBC Driver 17 for SQL Server};"
# #     "Server=SRMUMATBU10;"        # your SQL Server name or IP
# #     "Database=YEDP2024;"         # your database name
# #     "UID=your_username;"         # SQL Server login username
# #     "PWD=your_password;"         # SQL Server login password
# # )
# def get_connection():
#     return pyodbc.connect(conn_str)

# # -------------------
# # READ (Get all records)
# # -------------------
# @app.route("/admins", methods=["GET"])
# def get_admins():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM AdminInfo")
#     rows = cursor.fetchall()
#     conn.close()

#     data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
#     return jsonify(data)

# # -------------------
# # READ (Get single record by ID)
# # -------------------
# @app.route("/admins/<int:id>", methods=["GET"])
# def get_admin(id):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM AdminInfo WHERE ID = ?", (id,))
#     row = cursor.fetchone()
#     conn.close()

#     if row:
#         data = dict(zip([column[0] for column in cursor.description], row))
#         return jsonify(data)
#     else:
#         return jsonify({"error": "not found"}), 404

# # -------------------
# # CREATE (Insert new record)
# # -------------------
# @app.route("/create", methods=["GET", "POST"])
# def create_admin():
#     if request.method == "POST":
#         # Handle form submission
#         name = request.form["AdminName"]
#         email = request.form["Email"]
#         password = request.form["Password"]

#         conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             "INSERT INTO AdminInfo (Name, Email, Password) VALUES (?, ?, ?)",
#             (name, email, password)
#         )
#         conn.commit()
#         conn.close()

#         return "Admin created successfully!"
#     else:
#         # Show the form
#         return render_template("create.html")

# # -------------------
# # UPDATE (Modify existing record)
# # -------------------
# @app.route("/update/<int:id>", methods=["GET", "POST"])
# def update_admin(id):
#     conn = get_connection()
#     cursor = conn.cursor()

#     if request.method == "POST":
#         # Handle form submission
#         name = request.form["AdminName"]
#         email = request.form["Email"]
#         password = request.form["Password"]

#         cursor.execute(
#             "UPDATE AdminInfo SET Name = ?, Email = ?, Password = ? WHERE ID = ?",
#             (name, email, password, id)
#         )
#         conn.commit()
#         conn.close()

#         return "Admin updated successfully!"
#     else:
#         # Load existing record to pre-fill the form
#         cursor.execute("SELECT Name, Email, Password FROM AdminInfo WHERE ID = ?", (id,))
#         row = cursor.fetchone()
#         conn.close()

#         if row:
#             return render_template(
#                 "update.html",
#                 id=id,
#                 name=row[0],
#                 email=row[1],
#                 password=row[2]
#             )
#         else:
#             return "Admin not found", 404

# # -------------------
# # DELETE (Remove record)
# # -------------------
# @app.route("/delete/<int:id>", methods=["GET", "POST"])
# def delete_admin(id):
#     conn = get_connection()
#     cursor = conn.cursor()

#     if request.method == "POST":
#         # Perform the delete
#         cursor.execute("DELETE FROM AdminInfo WHERE ID = ?", (id,))
#         conn.commit()
#         conn.close()
#         return "Admin deleted successfully!"
#     else:
#         # Show a confirmation form
#         cursor.execute("SELECT Name, Email FROM AdminInfo WHERE ID = ?", (id,))
#         row = cursor.fetchone()
#         conn.close()

#         if row:
#             return render_template("delete.html", id=id, name=row[0], email=row[1])
#         else:
#             return "Admin not found", 404

# if __name__ == "__main__":
#     app.run(debug=True)








from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import pyodbc
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key_here"   # Needed for session management

# Database connection string
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=SRMUMATBU10;"
    "Database=YEDP2024;"
    "Trusted_Connection=yes;"
)

def get_connection():
    return pyodbc.connect(conn_str)

# -------------------
# CREATE (Insert new record with hashed password)
# -------------------
@app.route("/create", methods=["GET", "POST"])
def create_admin():
    if request.method == "POST":
        name = request.form["AdminName"]
        email = request.form["Email"]
        password = request.form["Password"]

        # Hash the password before storing
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        print(hashed_pw)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO AdminInfo (Name, Email, Password) VALUES (?, ?, ?)",
            (name, email, hashed_pw.decode("utf-8"))
        )
        conn.commit()
        conn.close()

        return "Admin created successfully with hashed password!"
    else:
        return render_template("create.html")

# -------------------
# LOGIN (Authentication)
# -------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["Email"]
        password = request.form["Password"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Name, Email, Password FROM AdminInfo WHERE Email = ?", (email,))
        row = cursor.fetchone()
        conn.close()

        if row:
            stored_hash = row[3]  # Password column
            if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                session["admin_id"] = row[0]
                session["admin_name"] = row[1]
                return f"Welcome {row[1]}! You are logged in."
            else:
                return "Invalid password", 401
        else:
            return "Admin not found", 404
    else:
        return render_template("login.html")

# -------------------
# LOGOUT
# -------------------
@app.route("/logout")
def logout():
    session.clear()
    return "Logged out successfully!"

# -------------------
# PROTECTED ROUTE EXAMPLE
# -------------------
@app.route("/dashboard")
def dashboard():
    if "admin_id" in session:
        return f"Hello {session['admin_name']}, welcome to your dashboard!"
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)





# That string contains:
# Algorithm version ($2b$)
# Cost factor (12 → how slow hashing is)
# Salt (random data)
# Hashed password (result of mixing password + salt)

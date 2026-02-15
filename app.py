from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL connection using Render DATABASE_URL
def get_db():
    DATABASE_URL = os.environ.get("DATABASE_URL")

    con = psycopg2.connect(DATABASE_URL)
    return con


# Home page
@app.route('/')
def index():
    return render_template('index.html')


# ADD student
@app.route('/register', methods=['POST'])
def add():
    name = request.form.get('name')
    dept = request.form.get('dept')

    con = get_db()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO users (name, dept) VALUES (%s, %s)",
        (name, dept)
    )

    con.commit()
    cur.close()
    con.close()

    return """
    <script>
        alert('Data inserted successfully!');
        window.location.href='/';
    </script>
    """


# VIEW students
@app.route('/view')
def view():
    con = get_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM users")
    data = cur.fetchall()

    cur.close()
    con.close()

    html = """
    <html>
    <body>
    <h2>Student Details</h2>
    <table border="1" cellpadding="10">
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Department</th>
        <th>Action</th>
      </tr>
    """

    for row in data:
        html += f"""
        <tr>
          <td>{row[0]}</td>
          <td>{row[1]}</td>
          <td>{row[2]}</td>
          <td>
            <a href="/delete/{row[0]}">
              <button>Delete</button>
            </a>
          </td>
        </tr>
        """

    html += """
    </table>
    <br>
    <a href="/">Back</a>
    </body>
    </html>
    """

    return html


# DELETE student
@app.route('/delete/<int:id>')
def delete(id):
    con = get_db()
    cur = con.cursor()

    cur.execute("DELETE FROM users WHERE id=%s", (id,))

    con.commit()
    cur.close()
    con.close()

    return """
    <script>
        alert('Record deleted successfully!');
        window.location.href='/view';
    </script>
    """


if __name__ == '__main__':
    app.run(debug=True)

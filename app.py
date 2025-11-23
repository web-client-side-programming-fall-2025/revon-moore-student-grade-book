from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# In-memory storage
students = []
grades = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/students", methods=["GET", "POST"])
def students_page():
    if request.method == "POST":
        name = request.form.get("student_name")
        if name and name not in students:
            students.append(name)
            grades[name] = []
        return redirect("/students")

    return render_template("students.html", students=students)


@app.route("/averages", methods=["GET", "POST"])
def averages_page():
    if request.method == "POST":
        student = request.form.get("student")
        grade = request.form.get("grade")

        if student in students:
            try:
                grade_value = float(grade)
                grades[student].append(grade_value)
            except ValueError:
                pass

        return redirect("/averages")

    student_avg = {
        s: (sum(grades[s]) / len(grades[s]) if grades[s] else 0)
        for s in students
    }

    return render_template(
        "averages.html",
        students=students,
        student_avg=student_avg
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

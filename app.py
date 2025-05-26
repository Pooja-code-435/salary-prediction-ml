from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load models and encoders
with open("rf_salary_model.pkl", "rb") as file:
    salary_model = pickle.load(file)

with open("lb_salary.pkl", "rb") as file:
    lb_salary = pickle.load(file)

with open("lb1_salary.pkl", "rb") as file:
    lb1_salary = pickle.load(file)

# Prediction function
def salaryPrediction(Age=33, Gender="Female", Education_Level="Bachelor's Degree", Job_Title="Software Engineer", Years_of_Experience=3):
    lst = []

    # Convert age and experience to numeric
    Age = float(Age)
    Years_of_Experience = float(Years_of_Experience)
    lst.append(Age)

    # Encode gender
    if Gender == "Female":
        lst.append(0)
    elif Gender == "Male":
        lst.append(1)
    else:
        lst.append(2)

    # Encode education and job
    Education_Level = lb1_salary.transform([Education_Level])
    lst.extend(list(Education_Level))

    Job_Title = lb_salary.transform([Job_Title])
    lst.extend(list(Job_Title))

    lst.append(Years_of_Experience)

    # Predict salary
    result = salary_model.predict([lst])
    return result[0]

# Routes
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # Get form data
        age = request.form.get("age")
        gender = request.form.get("gender")
        education = request.form.get("education")
        job = request.form.get("job")
        experience = request.form.get("experience")

        # Make prediction
        result = salaryPrediction(
            Age=age,
            Gender=gender,
            Education_Level=education,
            Job_Title=job,
            Years_of_Experience=experience
        )
        print(result)
        # Render result
        return render_template("predict.html", prediction=result)

    # If GET request, show the form
    return render_template("predict.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8000)

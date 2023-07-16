import json
import requests
from flask import Flask, render_template, request, send_file
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import time


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['csvfile']
        if file:
            filename = file.filename
            file.save(filename)
            cleaned_emails = process_csv_file(filename)
            save_to_text_file(cleaned_emails)
            return send_file("email_data.txt", as_attachment=True)

        
    return render_template('index.html')


def process_csv_file(filename):
    api_key = ""  # Replace with your actual API key
    url_template = "https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}"
    cleaned_emails = []

    with open(filename, "r") as file:
        reader = file.readlines()
        for line in reader:
            email = line.strip()
            url = url_template.format(api_key=api_key, email=email)

            response = requests.get(url)
            print(f"Email: {email}")
            print(f"Status code: {response.status_code}")
            print()
            # ...

            # Check if the email is valid
            if response.status_code == 200:
                response_content = response.content.decode("utf-8")  # Decode the response content

                # Extract the desired values from the decoded response content
                json_data = json.loads(response_content)
                email = json_data["email"]
                deliverability = json_data["deliverability"]
                quality_score = json_data["quality_score"]

                # Check if the email has deliverability "DELIVERABLE"
                if deliverability == "DELIVERABLE":
                    # Print or save the values as needed
                    print(f"Email: {email}")
                    print(f"Deliverability: {deliverability}")
                    print(f"Quality Score: {quality_score}")
                    print()

                    # Add the email to the cleaned_emails list if it is valid
                    cleaned_emails.append(email)
            time.sleep(2)

            # ...
    
    return cleaned_emails


def save_to_text_file(cleaned_emails):
    with open("email_data.txt", "w") as file:
        for email in cleaned_emails:
            file.write(f"{email},\n")


if __name__ == '__main__':
    app.run(debug=True)

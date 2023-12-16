import json
import requests
from flask import Flask, render_template, request, send_file
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import time
import re
import csv


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['csvfile']
        if file:
            filename = file.filename
            file.save(filename)
            cleaned_emails = process_csv_file(filename)
            save_to_csv_file(cleaned_emails)
            return send_file("email_data.txt", as_attachment=True)

        
    return render_template('index.html')

#VALIDADOR POR API#
#def process_csv_file(filename): #
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

#VALIDADOR LOCAL#
def is_valid_email(email):
    # Basic email format validation using a regular expression
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def process_csv_file(filename):
    cleaned_emails = []

    with open(filename, "r") as file:
        reader = file.readlines()
        for line in reader:
            email = line.strip()

            # Check if the email is valid based on basic format validation
            if is_valid_email(email):
                # Perform additional checks if needed
                # For example, check if the domain exists, etc.

                # Print or save the values as needed
                print(f"Email: {email}")
                print(f"Deliverability: VALID")
                print("Quality Score: N/A")  # Since there is no API, quality score is not available
                print()

                # Add the email to the cleaned_emails list if it is valid
                cleaned_emails.append(email)
            else:
                print(f"Email: {email}")
                print(f"Deliverability: INVALID")
                print("Quality Score: N/A")
                print()

    return cleaned_emails


##def save_to_text_file(cleaned_emails):
    with open("email_data.txt", "w") as file:
        for email in cleaned_emails:
            file.write(f"{email},\n")

#GENERA CSV#
def save_to_csv_file(cleaned_emails, output_filename="email_data.csv"):
    with open(output_filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Email", "Deliverability", "Quality Score"])  # Header row

        for email in cleaned_emails:
            # Assuming you have additional information like deliverability and quality score
            # If not, adjust accordingly
            writer.writerow([email, "DELIVERABLE", "N/A"])



if __name__ == '__main__':
    app.run(debug=True)

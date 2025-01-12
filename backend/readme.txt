How to Run this program:

Step 1: Set Up the Environment
	1.	Install Python
Ensure that Python 3.9.6 is installed on your system. You can download it from Python’s official website.
Verify the installation by running:

python --version


	2.	Install a Virtual Environment (Recommended)
To avoid conflicts with other Python packages, create and activate a virtual environment:
	•	Create the virtual environment:

python -m venv myenv


	•	Activate the virtual environment:
	•	On Windows:

myenv\Scripts\activate


	•	On Mac/Linux:

source myenv/bin/activate


	3.	Clone or Download the Project
Obtain the project files by either cloning the repository:

git clone https://github.com/SanSynyster/django-petition-platform.git

Or downloading the files directly as a zip and extracting them.

	4.	Navigate to the Project Directory
Open a terminal/command prompt and navigate to the project’s backend folder:

cd /path/to/django-petition-platform/backend


	5.	Install Dependencies
Install the required dependencies listed in the requirements.txt file:

pip install -r requirements.txt



This ensures all CSS, JavaScript, and other static files are ready to be served.

==============================================================================


STEP 2: Set Up the Database
	1.	Configure the Database
The MongoDB Atlas URI is already configured in settings.py. 
Make Sure the dependenciesare installed.
Make Sure your Device is connected to the internet.

==============================================================================

Step 3: Run the Server
	1.	Activate the Virtual Environment
Ensure that your virtual environment is active. If not, activate it using the following command:

source myenv/bin/activate  # For macOS/Linux
myenv\Scripts\activate     # For Windows


	2.	Start the Django Development Server
Run the following command to start the development server:

python manage.py runserver


	3.	Verify the Server is Running
After running the command, you should see output similar to this:

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 3.2, using settings 'backend.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

** please ignore if it says : You have 1 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): myapp.
Run 'python manage.py migrate' to apply them. **

The server will be running at http://127.0.0.1:8000/ (or localhost:8000).

	4.	Access the Application
	•	Open a browser and navigate to http://127.0.0.1:8000/.
	•	You should see the homepage of the project or the admin login page, depending on your configuration.
	5.	Test Admin Access
	•	Go to http://127.0.0.1:8000/admin/.
	•	Log in using the superuser credentials you created in Step 2.

===========================================================================================

The admin email is admin@petition.parliament.sr, and the password is admin123.

===========================================================================================

Step 4: Testing the Application
	1.	Test the Admin Dashboard
	•	Navigate to the admin panel: http://127.0.0.1:8000/admin/.
	•	Log in using the superuser credentials : admin@petition.parliament.sr : admin123
	•	Verify you can view and manage models such as Petitioner, Petition, and Signature.
	2.	Test User Registration
	•	Navigate to the registration page: http://127.0.0.1:8000/register/.
	•	Fill in the form with a valid email, password, and BioID.
    •   You can use the QR code scanner by your Webcam, just simply show the QR code on your mobile screen in front of the webcam.
	•	Submit the form and verify successful registration by checking for flash messages or navigating to the admin panel to view the newly created user.
	3.	Test User Login
	•	Navigate to the login page: http://127.0.0.1:8000/login/.
	•	Enter valid credentials for a registered user.
	•	Verify successful login by checking for flash messages or being redirected to the user dashboard.
	4.	Test User Dashboard
	•	After logging in, navigate to the user dashboard.
	•	Verify the display of petitions available for signing.
	•	Test signing a petition and ensure it updates the signatures count correctly.
	5.	Test Petition Creation
	•	Log in as a registered user.
	•	Navigate to the petition creation page: http://127.0.0.1:8000/create-petition/.
	•	Fill in the title and content fields, then submit.
	•	Verify the petition appears in the dashboard and admin panel.
	6.	Test Admin Functionality
	•	Log in as the Admin.
	•	Navigate to the admin dashboard: http://127.0.0.1:8000/admin-dashboard/.
	•	Verify analytics such as Total Petitions, Open Petitions, and Closed Petitions.
	•	Test closing a petition by providing a response, and verify the status updates correctly.
	7.	Test API Endpoints 
	•	Test API endpoints for petitions, signing petitions, and filtering:
	•	/api/get-petitions/
	•	/api/sign-petition/<petition_id>/
	•	/api/get-filtered-petitions/
	•	Use tools like Postman or cURL to verify responses.
	8.	Verify CSS and Frontend
	•	Check the visual appearance of the application.
	•	Ensure animations, colors, and styles are consistent across all pages.
	9.	Handle Edge Cases
	•	Test invalid inputs (e.g., invalid credentials, missing fields).
	•	Verify that error messages are displayed correctly.
	•	Check functionality with edge-case scenarios, such as no petitions available.






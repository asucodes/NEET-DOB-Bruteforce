# NEET-DOB-Bruteforce xyzsdd

# Purpose: To automate the process of entering DOB to check result of a user with known application number. 


# Intend: for educational purpose only. I do not promote any malicious usecase of this script for purpose of bully or monetary business.  

This python script uses selenium libraries to bruteforce extract Date and Birth and result of a applicant with known Application Number. 
The script runs on https://neet.ntaonline.in/frontend/web/scorecard/index or any website of NTA using similar interface. 

# Step 1>

Install Chrome for Developers from https://googlechromelabs.github.io/chrome-for-testing/ , you need to install a chrome binary which might look like this on the page

| chrome |	win64 |	https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.36/win64/chrome-win64.zip |	200 |

and chrome driver for the same, it might look like: 

| chromedriver | win64	| https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.36/win64/chromedriver-win64.zip | 

# Step 2>

Once installed in a folder with known path, navigate to ntaresultcheck.py script downloaded from github and replace path of both chrome and chrome driver with the path where you have installed your setup. The code which requires replacement might look like: 

chrome_binary_path = r"D:\asu\chrome-win64\chrome.exe"

 Correct path to your ChromeDriver executable
chrome_driver_path = r"D:\asu\chromedriver-win64\chromedriver.exe" 

# Step 3>

Once you have updated ntaresultcheck.py , go to win powershell  / cmd and type:

pip install selenium

NOTE: If you dont have python installed on your computer this might not work. To install python type:

Download the Installer:

Go to the official Python website.
Click on the "Download Python" button. The website will suggest the best version for your operating system.
Run the Installer:

Locate the downloaded installer (usually in your Downloads folder) and double-click it.
In the installer window, check the box that says "Add Python to PATH." This is important for running Python from the command line.
Click "Install Now."
Verify the Installation:

Open Command Prompt (search for "cmd" in the Start menu).
Type python --version and press Enter. You should see the version of Python you installed.

# Step 4> 

This is the final step. Once everything is done you can go to ntaresultcheck.py and at the bottom of the code you can replace brute_force_dates("240410136941") with the application number of your choice. Save it and run the python file by typing: "python  ntaresultcheck.py" in the terminal. This should start checking every DOB from 2003 Jan 1 tto 2007 Dec 31 until a match is found. The script will stop automatically once a match is found.




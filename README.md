# uwoGradeScraper
 A simple web scraper that notifies the user when the student's grades have been updated on the student center.

Requirements:

pip install beautifulsoup4

pip install requests

pip install win10toast

win10toast is not required if you do not wish to recieve windows 10 toast notifications when grades are updated. The user can change what the program does when it detects a change by changing the contents of actionWhenChange.py. This will run once whenever a change is detected. 

Start by updating info.txt with the user's credentials, delay between checks, and how many courses the student has on their student center for the entire year.

Run the program by running scraper.py.

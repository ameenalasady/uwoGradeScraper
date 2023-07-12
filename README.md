# Grade Scraper

A program that scrapes a student's grades from the university's student center (specific to Western University).

## Features

- Scrape grades for the any term

- Have grades saved to a log file
- View grades in the terminal
- Option to receive notifications when grades are updated

  - Discord

  - Windows 10 toast notifications
  - Easily updated to include more actions

Here is a screenshot of what the program looks like:

![Screenshot of my project](./images/Screenshot_1.png)

## Requirements

- beautifulsoup4

- requests
- pwinput
- win10toast (optional, for Windows 10 toast notifications)
- discord (optional, for Discord notifications)
- colorama (optional, for colored terminal output)
- selenium
- ChromeDriver (GeckoDriver also works but requires slight code adjustments)

## How to Use

1. Install the required packages by running `pip install -r requirements.txt`

2. Get the Chrome WebDriver [here](https://chromedriver.chromium.org/downloads). Make sure that the WebDriver version that you get matches the version of your Chrome installation.

3. Update the path to your WebDriver executable in `scraper.py`.

4. Update `info.json` with the student's login credentials.

5. Run the script using `python scraper.py`

6. Input how long you want the script to sleep between checks when prompted by `scraper.py`.

7. Complete your Duo 2FA when prompted, it is recommended to tick the "remember me for 8 hours" box in Duo when completing your 2FA. This allows the script to restart autonomously when it faces an error.

8. Select which term you want to track changes for (tracking more than one term at the same time is not currently supported).

9. Select which courses you want to track changes for. Enter nothing to track all.

10. Your grades will be printed to the terminal and, if enabled, sent as a notification to your Discord server and/or displayed as a Windows 10 toast notification when a change is detected.

## Notes

- This program has only been tested on Windows 10.

- The university's student center website and login process may change, which could break this program. Please open an issue if you encounter any problems.

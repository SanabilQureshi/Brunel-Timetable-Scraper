# Brunel Timetable Scraper

## Overview

After a year of dealing with a fast, but not easily navigable timetable website for my university - I built an automated Python web scraper that extracts timetable data and converts it into a standard ICS calendar file that can be imported in many popular providers such as Google/Outlook Calendar. 

The tool leverages Selenium WebDriver to automate browser interactions with the Brunel timetable system, parses the HTML content using BeautifulSoup, and generates a .ICS calendar file with all your scheduled events. Details about the lecture, location, timing are all placed in the relevant fields so that one can easily check which room/building to go to.

---

## Key Features

- **Automated Authentication**: Logs into the Brunel timetable system with provided credentials without manual intervention
- **Comprehensive Data Extraction**: Scrapes timetable data across 51 consecutive weeks for full academic year coverage
- **Smart Parsing Logic**: Intelligently identifies and extracts event details (name, time, location, description)
- **ICS Calendar Generation**: Produces standard-compliant ICS files compatible with all major calendar applications
- **Headless Operation**: Runs efficiently in the background without opening visible browser windows
- **Robust Error Handling**: Implements parsing logic that gracefully handles variations in timetable formatting

---

## Technology Stack

- **Python 3** as the core programming language
- **Selenium WebDriver** for browser automation and web interactions
- **BeautifulSoup** for robust HTML parsing and data extraction
- **ICS Library** for generating calendar files in standard format
- **Firefox GeckoDriver** for headless browser control

---

## How It Works

The scraper follows a precise sequence to extract and convert timetable data:

1. **Browser Initialisation**: Launches a headless Firefox instance with Selenium WebDriver
2. **Authentication Flow**: Navigates to Brunel's timetable login page and authenticates with provided credentials
3. **Navigation Sequence**: Automatically clicks through the interface to access the student timetable
4. **View Configuration**: Selects list view and appropriate week settings for optimal data extraction
5. **Data Extraction Loop**: Iterates through 51 weeks of timetable data:
   - Retrieves HTML content for each week
   - Parses content with BeautifulSoup to identify timetable entries
   - Extracts event details (name, start/end times, location, description)
   - Converts data into ICS event format
6. **File Generation**: Compiles all events into a single ICS calendar file
7. **Cleanup**: Properly closes the browser instance and releases resources

---

## Quick Start

```bash
# 1. Clone and navigate to project
git clone https://github.com/SanabilQureshi/Brunel-Timetable-Scraper && cd Brunel-Timetable-Scraper

# 2. Install Python dependencies
pip install selenium beautifulsoup4 ics html5lib

# 3. Download and configure geckodriver
# - Download from https://github.com/mozilla/geckodriver/releases
# - Update the 'gecko_path' variable in scraper.py with your geckodriver path

# 4. Configure credentials
# Update the demo credentials in scraper.py with your actual Brunel credentials:
# driver.find_element_by_xpath('//*[@id="tUserName"]').send_keys('YOUR_USERNAME')
# driver.find_element_by_xpath('//*[@id="tPassword"]').send_keys('YOUR_PASSWORD')

# 5. Run the scraper
python scraper.py
```

The output will be saved as `My_Timetable.ics` which can be imported into any calendar application that supports the ICS format (Google Calendar, Outlook, Apple Calendar, etc.).

---

## Project Structure

```
Brunel-Timetable-Scraper/
├── scraper.py              # Main scraping script with full automation logic
├── My_Timetable_15_Nov.ics # Generated ICS calendar file (example output)
└── README.md               # This documentation file
```

---

## Implementation Details

### Core Components

- **Selenium WebDriver**: Handles all browser automation tasks including navigation, authentication, and UI interactions
- **HTML Parsing Engine**: BeautifulSoup processes HTML content to extract structured timetable data
- **Date Processing Logic**: Handle date calculations and time parsing for accurate event scheduling
- **ICS Generator**: Converts parsed timetable data into standard calendar format with proper timezone handling

### Technical Highlights

- **Headless Browser Operation**: Firefox runs without GUI for efficient background processing
- **Precise XPath Navigation**: Uses specific XPath selectors to reliably interact with the timetable interface
- **Parsing Logic**: Handles variations in timetable formatting across different weeks
- **Memory Efficient Processing**: Processes one week at a time to maintain low memory footprint

---

## Future Improvements

- **Enhanced Error Handling**: Add comprehensive exception handling for network failures and parsing errors
- **Configuration File Support**: Move credentials and settings to external configuration file
- **Email Integration**: Automatically email generated ICS files to users
- **Web Interface**: Create a simple web UI for non-technical users
- **Docker Containerisation**: Package the application for easy deployment
- **Schedule Updates**: Implement incremental updates to refresh calendar with timetable changes

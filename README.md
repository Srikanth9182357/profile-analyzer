GitHub Profile Analyzer (Django)

A web-based application developed using Django that allows users to analyze GitHub profiles without the need for authentication (username and password). The application fetches data directly from GitHub's public API to provide detailed insights into any public GitHub profile, including repositories, followers, contributions, and more.

Features

Profile Overview: Displays general information such as the number of repositories, followers, following, and bio of the GitHub user.

Repository Details: Lists all public repositories with information such as repository name, description, language used, and creation date.

Contribution Graph: Visualizes the user's contributions, such as commits, pull requests, and issues, over time.

Top Languages: Displays the most used programming languages across the user’s repositories.

Followers & Following: Shows the user’s followers and people they are following.

No Authentication Needed: The app does not require a username and password, making it simple to use.

Project Structure

The project follows a standard Django structure, with a focus on separating concerns using views, URLs, templates, and settings.

github-profile-analyzer/
├── manage.py
├── github_analyzer/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py        # Contains views to handle GitHub API requests and render data
│   ├── urls.py         # Defines the URL patterns and routes
│   ├── templates/
│   │   └── github_analyzer/
│   │       ├── base.html   # Base template with shared layout
│   │       ├── home.html   # Home page template
│   │       ├── profile.html # Profile details page template
│   └── settings.py      # Settings file with project configuration
├── db.sqlite3           # Database file (if needed for caching or user data)
└── requirements.txt     # List of Python dependencies

Installation
Prerequisites

Ensure that you have the following installed:

Python (>=3.6)

Django (>=3.0)

Requests (to make API calls to GitHub)

Step-by-Step Installation

Clone the Repository

git clone https://github.com/your-username/github-profile-analyzer.git
cd github-profile-analyzer


Create a Virtual Environment

python -m venv venv


Activate the Virtual Environment

On Windows:

venv\Scripts\activate


On macOS/Linux:

source venv/bin/activate


Install Required Dependencies

pip install -r requirements.txt


Run the Development Server

python manage.py runserver


Access the Application

Visit the application in your browser:

http://127.0.0.1:8000

Usage
Homepage

On the home page, you can input a GitHub username and click Analyze to fetch data about the user's public profile.

Profile Details

The profile page will display various insights including:

Basic profile information (e.g., name, bio, location).

A list of repositories.

Contribution graph.

Top used programming languages.

A list of followers and following.

No Authentication

The application does not require GitHub username and password. It simply uses GitHub's public API to retrieve profile data based on the username you provide.

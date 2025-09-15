import urllib.request
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.platypus import Image
import io

# GitHub API base URL
GITHUB_API_URL = "https://api.github.com/users/"

def fetch_json(url):
    """Helper function to fetch JSON from GitHub API"""
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
    except Exception as e:
        print("Error fetching:", e)
    return None

def home(request):
    """Render home page with search form"""
    return render(request, "analyzer/home.html")

def analyze_github(request):
    """
    Fetch and analyze GitHub user data
    """
    if request.method == "POST":
        username = request.POST.get("username")
        
        if not username:
            return render(request, "analyzer/home.html", {"error": "Please enter a GitHub username"})

        # Fetch profile data
        profile_data = fetch_json(f"{GITHUB_API_URL}{username}")
        repos_data = fetch_json(f"{GITHUB_API_URL}{username}/repos")

        if not profile_data:
            return render(request, "analyzer/home.html", {"error": "User not found"})

        if repos_data is None:
            repos_data = []
            
        #  Process repository details
        repo_details = []
        for repo in repos_data:
            repo_details.append({
                "name": repo.get("name"),
                "html_url": repo.get("html_url"),
                "description": repo.get("description"),
                "language": repo.get("language"),
                "stargazers_count": repo.get("stargazers_count", 0),
                "forks_count": repo.get("forks_count", 0),
                "watchers": repo.get("watchers_count", 0),
                "open_issues": repo.get("open_issues_count", 0),
                "license": repo.get("license", {}).get("name") if repo.get("license") else "No license",
                "updated_at": repo.get("updated_at"),
            })
            
            
        # Analysis: total repos, stars, forks, languages
        total_repos = len(repos_data)
        total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
        total_forks = sum(repo.get("forks_count", 0) for repo in repos_data)

        # Count languages
        languages = {}
        for repo in repos_data:
            lang = repo.get("language")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
                
        lang_labels = list(languages.keys())
        lang_counts = list(languages.values())
        
        #context Dict
        context = {
            "profile": profile_data,
            "repos": repo_details,
            "total_repos": total_repos,
            "total_stars": total_stars,
            "total_forks": total_forks,
            "languages": languages,
            "lang_labels": json.dumps(lang_labels),  # send as JSON
            "lang_counts": json.dumps(lang_counts),
            
        }
        request.session["report_data"] = context  # save in session for export
        return render(request, "analyzer/result.html", context)
    return render(request, "analyzer/home.html")


def export_pdf(request):
    """Export analyzed GitHub report to PDF"""
    data = request.session.get("report_data")
    if not data:
        return HttpResponse("No data available to export. Please analyze a profile first.")

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="github_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("📊 GitHub Analysis Report", styles['Title']))
    elements.append(Spacer(1, 12))

    # User Profile
    profile = data["profile"]
    elements.append(Paragraph(f"<b>Name:</b> {profile.get('name', 'N/A')}", styles['Normal']))
    elements.append(Paragraph(f"<b>Username:</b> {profile.get('login', '')}", styles['Normal']))
    elements.append(Paragraph(f"<b>Followers:</b> {profile.get('followers', 0)} | <b>Following:</b> {profile.get('following', 0)}", styles['Normal']))
    elements.append(Paragraph(f"<b>Total Repositories:</b> {data['total_repos']}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Stats
    elements.append(Paragraph("<b>Repository Stats</b>", styles['Heading2']))
    elements.append(Paragraph(f"⭐ Stars: {data['total_stars']}", styles['Normal']))
    elements.append(Paragraph(f"🍴 Forks: {data['total_forks']}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Languages
    elements.append(Paragraph("<b>Languages Used</b>", styles['Heading2']))
    lang_table = [["Language", "Count"]]
    for lang, count in data["languages"].items():
        lang_table.append([lang, count])

    table = Table(lang_table)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))
    
    # Repositories (Detailed)
    elements.append(Paragraph("<b>Repositories (Detailed)</b>", styles['Heading2']))
    elements.append(Spacer(1, 6))

    for repo in data["repos"]:
        elements.append(Paragraph(f"🔗 <b>{repo['name']}</b>", styles['Heading3']))
        
        if repo['description']:
            elements.append(Paragraph(f"<b>Description:</b> {repo['description']}", styles['Normal']))
        else:
            elements.append(Paragraph("<b>Description:</b> No description available", styles['Normal']))
        
        repo_info = f"""
        <b>Language:</b> {repo['language'] or 'N/A'}  
        ⭐ Stars: {repo['stargazers_count']} | 🍴 Forks: {repo['forks_count']} | 👀 Watchers: {repo['watchers']}  
        🐞 Open Issues: {repo['open_issues']} | 📜 License: {repo['license']}  
        ⏳ Last Updated: {repo['updated_at']}
        """
        elements.append(Paragraph(repo_info, styles['Normal']))
        elements.append(Spacer(1, 12))

        
    # ---- Add Language Pie Chart ----
    if data["languages"]:
        plt.figure(figsize=(4, 4))
        plt.pie(
            data["languages"].values(),
            labels=data["languages"].keys(),
            autopct='%1.1f%%',
            startangle=140
        )
        plt.title("Languages Usage")

        img_buf = io.BytesIO()
        plt.savefig(img_buf, format="PNG")
        plt.close()
        img_buf.seek(0)

        elements.append(Paragraph("<b>Languages Distribution</b>", styles['Heading2']))
        elements.append(Image(img_buf, width=300, height=300))
        elements.append(Spacer(1, 12))
   

    doc.build(elements)
    return response
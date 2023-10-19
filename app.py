from flask import Flask, request, render_template, jsonify
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from flask_ngrok import run_with_ngrok
app = Flask(__name__)
run_with_ngrok(app)
def extract_information(url):
    try:
        response = requests.get(url)
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        emails = set(re.findall(email_pattern, content))  # Use a set to remove duplicates

        # Extract mobile numbers (assuming Indian mobile numbers)
        mobile_pattern = r'\b(?:\+91|0)?[ -.]?[789]\d{9}\b'
        mobile_pattern = r'\b(?:\+\d{1,3}\s?)?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}\b'
        mobiles = set(re.findall(mobile_pattern, content))  # Use a set to remove duplicates

        # Extract social media links and store them
        
        social_links = set()
        base_url = urlparse(url).scheme + "://" + urlparse(url).netloc
        for a in soup.find_all('a', href=True):
            link = a['href']
            
            # Add more social media platforms as needed
            if 'twitter.com' in link:
                social_links.add(link)
            if 'facebook.com' in link:
                social_links.add(link)
            if 'youtube.com' in link:
                social_links.add(link)
            if 'linkedin.com' in link:
                social_links.add(link)
            

        return list(emails), list(mobiles), list(social_links)  # Convert sets to lists

    except Exception as e:
        return [], [], []


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    emails, mobiles, social_links = extract_information(url)

    return jsonify({'email': emails, 'mobile': mobiles, 'social': social_links})

if __name__ == '__main__':
    app.run(debug=True)

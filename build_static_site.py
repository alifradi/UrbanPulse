#!/usr/bin/env python
"""
Static site builder for UrbanPulse Django project
This script generates a static version of the UrbanPulse website for Netlify deployment
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Configuration
BUILD_DIR = "build"
STATIC_DIR = "static"
TEMPLATES_DIR = "core/templates/core"
STATIC_ASSETS_DIR = "core/static/core"
PAGES = [
    {"template": "home.html", "output": "index.html"},
    {"template": "investment.html", "output": "investment/index.html"},
    {"template": "hazards.html", "output": "hazards/index.html"},
    {"template": "contact.html", "output": "contact/index.html"},
    {"template": "team.html", "output": "team/index.html"},
    {"template": "contributions.html", "output": "contributions/index.html"},
    {"template": "services.html", "output": "services/index.html"},
]

def main():
    """Main build function"""
    print("Starting UrbanPulse static site build...")
    
    # Create build directory
    if os.path.exists(BUILD_DIR):
        print(f"Cleaning existing {BUILD_DIR} directory...")
        shutil.rmtree(BUILD_DIR)
    
    os.makedirs(BUILD_DIR, exist_ok=True)
    
    # Create directories for pages
    for page in PAGES:
        if "/" in page["output"]:
            directory = os.path.join(BUILD_DIR, os.path.dirname(page["output"]))
            os.makedirs(directory, exist_ok=True)
    
    # Copy static assets
    if os.path.exists(STATIC_ASSETS_DIR):
        print("Copying static assets...")
        shutil.copytree(
            STATIC_ASSETS_DIR,
            os.path.join(BUILD_DIR, "static"),
            dirs_exist_ok=True
        )
    else:
        print(f"Warning: Static assets directory {STATIC_ASSETS_DIR} not found")
    
    # Copy media files if they exist
    if os.path.exists("media"):
        print("Copying media files...")
        shutil.copytree(
            "media",
            os.path.join(BUILD_DIR, "media"),
            dirs_exist_ok=True
        )
    
    # Process templates
    print("Processing templates...")
    try:
        from jinja2 import Environment, FileSystemLoader
        
        # Set up Jinja environment
        env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        
        # Process each page
        for page in PAGES:
            try:
                template = env.get_template(page["template"])
                output_path = os.path.join(BUILD_DIR, page["output"])
                
                # Render template with mock context
                context = get_mock_context_for_template(page["template"])
                rendered_content = template.render(**context)
                
                # Write to output file
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(rendered_content)
                
                print(f"Generated {output_path}")
            except Exception as e:
                print(f"Error processing {page['template']}: {str(e)}")
    
    except ImportError:
        print("Jinja2 not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "jinja2"])
        print("Please run the script again.")
        return
    
    print("Static site build complete! Files are in the 'build' directory.")

def get_mock_context_for_template(template_name):
    """Generate mock context data for templates"""
    # Base context used across all templates
    base_context = {
        "STATIC_URL": "/static/",
        "MEDIA_URL": "/media/",
    }
    
    # Template-specific context
    template_contexts = {
        "home.html": {
            "page_title": "UrbanPulse - Urban Data Analytics",
            "featured_insights": [
                {"title": "Population Growth Trends", "description": "Analysis of urban population changes"},
                {"title": "Business Opportunity Index", "description": "Top locations for new businesses"},
                {"title": "Safety Score Map", "description": "Comprehensive safety metrics by neighborhood"}
            ]
        },
        "investment.html": {
            "page_title": "Investment Opportunities - UrbanPulse",
            "opportunities": [
                {"name": "Downtown Development", "score": 87, "roi": "12-15%"},
                {"name": "Westside Commercial", "score": 92, "roi": "10-14%"},
                {"name": "North District Mixed-Use", "score": 78, "roi": "8-11%"}
            ]
        },
        "hazards.html": {
            "page_title": "Hazard Analysis - UrbanPulse",
            "hazard_reports": [
                {"title": "Flood Risk Assessment", "date": "April 2025"},
                {"title": "Seismic Activity Report", "date": "March 2025"},
                {"title": "Air Quality Index", "date": "May 2025"}
            ]
        },
        "contact.html": {
            "page_title": "Contact Us - UrbanPulse",
            "form_action": "#"  # Static form handling
        },
        "team.html": {
            "page_title": "Our Team - UrbanPulse",
            "team_members": [
                {"name": "Sarah Johnson", "position": "CEO", "image": "team/ceo.jpg"},
                {"name": "Michael Chen", "position": "CTO", "image": "team/cto.jpg"},
                {"name": "Elena Rodriguez", "position": "CSO", "image": "team/cso.jpg"}
            ]
        },
        "contributions.html": {
            "page_title": "Recent Contributions - UrbanPulse",
            "contributions": [
                {"title": "Urban Infrastructure Resilience", "date": "March 2025"},
                {"title": "Quantifying Urban Sustainability", "date": "January 2025"}
            ]
        },
        "services.html": {
            "page_title": "Services & Partnerships - UrbanPulse",
            "services": [
                {"name": "Data Insights & Analytics", "icon": "graph-up-arrow"},
                {"name": "Investment Opportunity Analysis", "icon": "building-check"},
                {"name": "Hazard & Sustainability Assessment", "icon": "shield-check"}
            ]
        }
    }
    
    # Merge base context with template-specific context
    context = base_context.copy()
    if template_name in template_contexts:
        context.update(template_contexts[template_name])
    
    return context

if __name__ == "__main__":
    main()

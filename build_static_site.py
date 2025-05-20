#!/usr/bin/env python
"""
Static site builder for UrbanPulse Django project
This script generates a static version of the UrbanPulse website for Netlify deployment
"""

import os
import shutil
import sys 
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Configuration
BUILD_DIR = "build"
TEMPLATES_DIR = "core/templates/core"
STATIC_ASSETS_DIR = "core/static/core" # Make sure this path is correct
PAGES = [
    {"template": "home.html", "output": "index.html", "name": "home"},
    {"template": "investment.html", "output": "investment/index.html", "name": "investment"},
    {"template": "hazards.html", "output": "hazards/index.html", "name": "hazards"},
    {"template": "contact.html", "output": "contact/index.html", "name": "contact"},
    {"template": "team.html", "output": "team/index.html", "name": "team"},
    {"template": "contributions.html", "output": "contributions/index.html", "name": "contributions"},
    {"template": "services.html", "output": "services/index.html", "name": "services"},
]

def get_mock_context_for_template(template_name, current_page_name_from_build):
    """
    Generate mock context data for templates.
    Ensures page_title (for HTML title tag) and other critical variables are always present.
    """
    base_context = {
        "STATIC_URL": "/static/",
        "MEDIA_URL": "/media/",
        "current_page_name": current_page_name_from_build,
    }
    
    # Define specific data for each template
    # Ensure all keys accessed in templates are present here, or have fallbacks in the template
    # (though we are trying to remove |default filters for debugging)
    template_specific_data = {
        "home.html": {
            "page_title": "UrbanPulse - Urban Data Analytics", # For the <title> tag in base.html
            "hero_title": "Urban Data Intelligence for Smarter Investments", # For the H1 in home.html
            "featured_insights": [
                {"title": "Buildings Analyzed", "value": "14,382", "icon": "bi-building"},
                {"title": "Cities Covered", "value": "237", "icon": "bi-geo-alt"},
                {"title": "Business Opportunities", "value": "3,845", "icon": "bi-shop"},
                {"title": "Data Accuracy", "value": "98.7%", "icon": "bi-check-circle"}
            ]
        },
        "investment.html": {
            "page_title": "Investment Opportunities - UrbanPulse",
            "opportunities": [ 
                {"id": "prop1", "name": "Downtown Office Building", "image_slug": "property1.jpg", "type": "Commercial", "address": "123 Main St, Downtown", "safety_score": 4.0, "description": "Modern office building...", "price": "$2,450,000"},
                {"id": "prop2", "name": "East Side Mixed-Use", "image_slug": "property2.jpg", "type": "Mixed Use", "address": "456 Park Ave, East Side", "safety_score": 4.5, "description": "Newly renovated mixed-use...", "price": "$3,750,000"},
            ]
            # Add other necessary variables for investment.html, ensuring no default filter is needed if possible
        },
        "hazards.html": {
            "page_title": "Hazard Analysis & Sustainability - UrbanPulse",
            "hazard_reports": [ 
                 {"score_grade": "A", "district_name": "Downtown District", "summary": "Leading sustainability...", "green_buildings_pct": 85, "solar_capacity_mw": 12.5, "ev_stations_count": 245, "public_transit_rating": "Excellent", "waste_recycling_pct": 78, "full_report_link": "#"},
                 {"score_grade": "B", "district_name": "North District", "summary": "Strong sustainability...", "green_buildings_pct": 72, "solar_capacity_mw": 8.3, "ev_stations_count": 178, "public_transit_rating": "Good", "waste_recycling_pct": 65, "full_report_link": "#"},
            ]
        },
        "contact.html": {
            "page_title": "Contact Us - UrbanPulse",
            "form_action": "#" # For static site, form submission needs a service
        },
        "team.html": {
            "page_title": "Our Team - UrbanPulse",
            "team_members": [
                {"name": "Ali Fradi", "position": "Co-Founder", "image_slug": "team/ali_fr.jpeg", "diploma": "M.Sc in Applied Mathematics, Polytechnique Montreal, Canada", "bio": "Former data consultant with 5+ years of experience...", "linkedin_url": "https://www.linkedin.com/in/ali-frady/", "github_url": "https://github.com/alifradi"},
                {"name": "Kais Riani", "position": "Co-Founder", "image_slug": "team/kais_r.jpg", "diploma": "Ph.D. in Computer and Information Sciences, University of Michigan, USA", "bio": "Computer vision and machine learning engineer...", "linkedin_url": "https://www.linkedin.com/in/kais-riani/", "github_url": "#"},
                {"name": "Yakin Hajlaoui", "position": "Co-Founder", "image_slug": "team/yakin_h.jpg", "diploma": "Ph.D. in Applied Mathematics, Polytechnique Montreal, Canada", "bio": "Expert in mathematical modeling for different problems...", "linkedin_url": "https://www.linkedin.com/in/yakin-hajlaoui/", "twitter_url": "#"}
            ]
        },
        "contributions.html": {
            "page_title": "Recent Contributions - UrbanPulse",
            "contributions": [
                {"title": "Predictive Analytics for Urban Infrastructure Resilience", "publication_info": "Journal of Urban Technology, Vol. 38, Issue 2", "description": "This paper presents a novel framework...", "author_image_slug": "team/cto.jpg", "author_name": "Michael Chen, CTO", "date": "March 2025", "link": "#"},
                {"title": "Quantifying Urban Sustainability: A Comprehensive Metrics Framework", "publication_info": "Sustainable Cities and Society, Vol. 92", "description": "This research introduces a new framework...", "author_image_slug": "team/cso.jpg", "author_name": "Elena Rodriguez, CSO", "date": "January 2025", "link": "#"}
            ]
        },
        "services.html": {
            "page_title": "Services & Partnerships - UrbanPulse",
            "services": [ 
                {"name": "Data Insights & Analytics", "icon": "graph-up-arrow", "description": "Comprehensive analysis of urban data...", "points": ["Population analysis", "Infrastructure assessment"], "link":"/investment/", "name_short":"Data Insights"},
                {"name": "Investment Opportunity Analysis", "icon": "building-check", "description": "Data-driven identification and evaluation...", "points": ["Property evaluation", "Market trend analysis"], "link":"/investment/", "name_short":"Investment Analysis"},
            ]
        }
    }
    
    context = base_context.copy()
    
    if template_name in template_specific_data:
        context.update(template_specific_data[template_name])
    
    # Fallback for page_title if not set in template_specific_data
    if "page_title" not in context:
        generic_title = current_page_name_from_build.replace('_', ' ').title()
        context["page_title"] = f"{generic_title} - UrbanPulse"
        if template_name == "home.html" and "page_title" not in template_specific_data.get("home.html", {}): # Double check for home.html
             context["page_title"] = "UrbanPulse - Urban Data Analytics"


    return context

def main():
    """Main build function"""
    print("Starting UrbanPulse static site build...")
    
    if not os.path.isdir(TEMPLATES_DIR):
        print(f"Error: Templates directory '{TEMPLATES_DIR}' not found. Please check the path.")
        sys.exit(1)

    if os.path.exists(BUILD_DIR):
        print(f"Cleaning existing '{BUILD_DIR}' directory...")
        shutil.rmtree(BUILD_DIR)
    
    os.makedirs(BUILD_DIR, exist_ok=True)
    
    for page_config in PAGES:
        output_path = Path(BUILD_DIR) / page_config["output"]
        if output_path.parent != Path(BUILD_DIR): # Check if output is in a subdirectory
            output_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {output_path.parent}")
    
    static_output_dir = Path(BUILD_DIR) / "static"
    if os.path.exists(STATIC_ASSETS_DIR):
        print(f"Copying static assets from '{STATIC_ASSETS_DIR}' to '{static_output_dir}'...")
        shutil.copytree(
            STATIC_ASSETS_DIR,
            static_output_dir,
            dirs_exist_ok=True
        )
    else:
        print(f"Warning: Static assets directory '{STATIC_ASSETS_DIR}' not found. Skipping static asset copy.")
    
    media_input_dir = "media" 
    media_output_dir = Path(BUILD_DIR) / "media"
    if os.path.exists(media_input_dir):
        print(f"Copying media files from '{media_input_dir}' to '{media_output_dir}'...")
        shutil.copytree(
            media_input_dir,
            media_output_dir,
            dirs_exist_ok=True
        )
    else:
        print(f"Info: Media directory '{media_input_dir}' not found. Skipping media file copy.")
    
    print("Processing templates...")
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    
    for page_config in PAGES:
        try:
            template = env.get_template(page_config["template"])
            output_file_path = Path(BUILD_DIR) / page_config["output"]
            
            context = get_mock_context_for_template(page_config["template"], page_config["name"])
            rendered_content = template.render(**context)
            
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(rendered_content)
            
            print(f"Generated {output_file_path}")
        except Exception as e:
            print(f"Error processing template '{page_config['template']}' to '{page_config['output']}': {str(e)}")
            # To make Netlify build fail on error, uncomment the next line
            # sys.exit(1) 


    print(f"Static site build complete! Files are in the '{BUILD_DIR}' directory.")

if __name__ == "__main__":
    main()

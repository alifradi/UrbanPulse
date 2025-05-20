#!/usr/bin/env python
"""
Static site builder for UrbanPulse Django project
This script generates a static version of the UrbanPulse website for Netlify deployment
"""

import os
import shutil
import sys 
import json # For tojson filter
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Configuration
BUILD_DIR = "build"
TEMPLATES_DIR = "core/templates/core"
STATIC_ASSETS_DIR = "core/static/core" 
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
    Ensures all variables are explicitly provided.
    """
    base_context = {
        "STATIC_URL": "/static/",
        "MEDIA_URL": "/media/",
        "current_page_name": current_page_name_from_build,
    }
    
    template_specific_data = {
        "home.html": {
            "page_title": "UrbanPulse - Urban Data Analytics",
            "hero_title": "Urban Data Intelligence for Smarter Investments",
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
                {"id": "prop1", "name": "Downtown Office Building", "image_slug": "property1.jpg", "type": "Commercial", "address": "123 Main St, Downtown", "safety_score": 4.0, "description": "Modern office building with high occupancy rate and excellent transit access.", "price": "$2,450,000", "lat": 40.7128, "lng": -74.0060},
                {"id": "prop2", "name": "East Side Mixed-Use", "image_slug": "property2.jpg", "type": "Mixed Use", "address": "456 Park Ave, East Side", "safety_score": 4.5, "description": "Newly renovated mixed-use property with retail space and luxury apartments.", "price": "$3,750,000", "lat": 40.7200, "lng": -73.9800},
                {"id": "prop3", "name": "North District Residential", "image_slug": "property3.jpg", "type": "Residential", "address": "789 Oak St, North", "safety_score": 3.0, "description": "Spacious residential complex in a growing neighborhood.", "price": "$1,200,000", "lat": 40.7300, "lng": -74.0100},
            ]
            # Add other fields for comparison table if needed: size, business_potential, roi_estimate, sustainability, hazard_risk, last_inspection
        },
        "hazards.html": {
            "page_title": "Hazard Analysis & Sustainability - UrbanPulse",
            "hazard_reports": [ 
                 {"score_grade": "A", "district_name": "Downtown District", "summary": "Leading sustainability with extensive green building adoption and renewable energy integration.", "green_buildings_pct": 85, "solar_capacity_mw": 12.5, "ev_stations_count": 245, "public_transit_rating": "Excellent", "waste_recycling_pct": 78, "full_report_link": "#"},
                 {"score_grade": "B", "district_name": "North District", "summary": "Strong sustainability performance with ongoing improvements in renewable energy and transportation.", "green_buildings_pct": 72, "solar_capacity_mw": 8.3, "ev_stations_count": 178, "public_transit_rating": "Good", "waste_recycling_pct": 65, "full_report_link": "#"},
                 {"score_grade": "C", "district_name": "Industrial Zone", "summary": "Moderate sustainability with significant improvement opportunities in emissions and energy efficiency.", "green_buildings_pct": 45, "solar_capacity_mw": 5.1, "ev_stations_count": 62, "public_transit_rating": "Limited", "waste_recycling_pct": 52, "full_report_link": "#"},
            ]
            # Ensure all variables used in hazards.html (like those for charts, tables) are provided
        },
        "contact.html": {
            "page_title": "Contact Us - UrbanPulse",
            "form_action": "#" 
        },
        "team.html": {
            "page_title": "Our Team - UrbanPulse",
            "team_members": [
                {"name": "Ali Fradi", "position": "Co-Founder", "image_slug": "team/ali_fr.jpeg", "diploma": "M.Sc in Applied Mathematics, Polytechnique Montreal, Canada", "bio": "Former data consultant with 5+ years of experience in operational research, applied mathematics, and data engineering. Worked for financial institutions, agriculture and industries in different positions.", "linkedin_url": "https://www.linkedin.com/in/ali-frady/", "github_url": "https://github.com/alifradi", "twitter_url": ""},
                {"name": "Kais Riani", "position": "Co-Founder", "image_slug": "team/kais_r.jpg", "diploma": "Ph.D. in Computer and Information Sciences, University of Michigan, USA", "bio": "Computer vision and machine learning engineer. Worked on urban planning and data science projects with several companies for almost 4+ years.", "linkedin_url": "https://www.linkedin.com/in/kais-riani/", "github_url": "#", "twitter_url": ""},
                {"name": "Yakin Hajlaoui", "position": "Co-Founder", "image_slug": "team/yakin_h.jpg", "diploma": "Ph.D. in Applied Mathematics, Polytechnique Montreal, Canada", "bio": "Expert in mathematical modeling for different problems. Worked for mining companies, financial institutions and startups for 4+ years.", "linkedin_url": "https://www.linkedin.com/in/yakin-hajlaoui/", "github_url": "", "twitter_url": "#"}
            ]
        },
        "contributions.html": {
            "page_title": "Recent Contributions - UrbanPulse",
            "contributions": [
                {"title": "Predictive Analytics for Urban Infrastructure Resilience", "publication_info": "Journal of Urban Technology, Vol. 38, Issue 2", "description": "This paper presents a novel framework for predicting infrastructure vulnerabilities in urban environments using machine learning and historical maintenance data. The model achieved 87% accuracy in identifying potential failure points before they occurred.", "author_image_slug": "team/cto.jpg", "author_name": "Michael Chen, CTO", "date": "March 2025", "link": "#"},
                {"title": "Quantifying Urban Sustainability: A Comprehensive Metrics Framework", "publication_info": "Sustainable Cities and Society, Vol. 92", "description": "This research introduces a new framework for measuring urban sustainability across multiple dimensions, including energy usage, transportation efficiency, green space, and social equity indicators.", "author_image_slug": "team/cso.jpg", "author_name": "Elena Rodriguez, CSO", "date": "January 2025", "link": "#"}
            ]
        },
        "services.html": {
            "page_title": "Services & Partnerships - UrbanPulse",
            "services": [ 
                {"name": "Data Insights & Analytics", "icon": "graph-up-arrow", "description": "Comprehensive analysis of urban data to reveal patterns, trends, and opportunities across cities and neighborhoods.", "points": ["Population and demographic analysis", "Infrastructure condition assessment", "Business activity and economic indicators"], "link":"/investment/", "name_short":"Data Insights"},
                {"name": "Investment Opportunity Analysis", "icon": "building-check", "description": "Data-driven identification and evaluation of urban investment opportunities with comprehensive risk and return assessment.", "points": ["Property and location evaluation", "Market trend analysis and forecasting", "Comparative ROI modeling"], "link":"/investment/", "name_short":"Investment Analysis"},
                {"name": "Hazard & Sustainability Assessment", "icon": "shield-check", "description": "Comprehensive analysis of environmental risks, hazards, and sustainability metrics for urban areas and properties.", "points": ["Environmental risk mapping", "Climate resilience evaluation", "Green energy installation analysis"], "link":"/hazards/", "name_short":"Hazard Analysis"}
            ]
        }
    }
    
    context = base_context.copy()
    
    if template_name in template_specific_data:
        context.update(template_specific_data[template_name])
    
    if "page_title" not in context:
        generic_title = current_page_name_from_build.replace('_', ' ').title()
        context["page_title"] = f"{generic_title} - UrbanPulse"
        if template_name == "home.html" and "page_title" not in template_specific_data.get("home.html", {}):
             context["page_title"] = "UrbanPulse - Urban Data Analytics"
    
    # Ensure all keys within lists of dicts are present to avoid template errors with missing keys
    if template_name == "investment.html" and "opportunities" in context:
        for opp in context["opportunities"]:
            opp.setdefault("id", f"prop-{opp.get('name', 'N/A').replace(' ', '-')}")
            opp.setdefault("image_slug", "property_placeholder.jpg")
            opp.setdefault("type", "N/A")
            opp.setdefault("address", "Address unavailable")
            opp.setdefault("safety_score", 0.0)
            opp.setdefault("description", "No description available.")
            opp.setdefault("price", "$0")
            opp.setdefault("lat", 0) # Default lat/lng if missing
            opp.setdefault("lng", 0)


    return context

def main():
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
        if output_path.parent != Path(BUILD_DIR):
            output_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {output_path.parent}")
    
    static_output_dir = Path(BUILD_DIR) / "static"
    if os.path.exists(STATIC_ASSETS_DIR):
        print(f"Copying static assets from '{STATIC_ASSETS_DIR}' to '{static_output_dir}'...")
        shutil.copytree(STATIC_ASSETS_DIR, static_output_dir, dirs_exist_ok=True)
    else:
        print(f"Warning: Static assets directory '{STATIC_ASSETS_DIR}' not found.")
    
    media_input_dir = "media" 
    media_output_dir = Path(BUILD_DIR) / "media"
    if os.path.exists(media_input_dir):
        print(f"Copying media files from '{media_input_dir}' to '{media_output_dir}'...")
        shutil.copytree(media_input_dir, media_output_dir, dirs_exist_ok=True)
    else:
        print(f"Info: Media directory '{media_input_dir}' not found.")
    
    print("Processing templates...")
    # Added select_autoescape and tojson filter
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(['html', 'xml']),
        extensions=['jinja2.ext.loopcontrols'] # For break/continue if needed, though not used yet
    )
    env.filters['tojson'] = json.dumps


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
            # sys.exit(1) # Fail build on any error

    print(f"Static site build complete! Files are in the '{BUILD_DIR}' directory.")

if __name__ == "__main__":
    main()

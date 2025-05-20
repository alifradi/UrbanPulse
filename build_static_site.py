#!/usr/bin/env python
"""
Static site builder for UrbanPulse Django project
This script generates a static version of the UrbanPulse website for Netlify deployment
"""

import os
import shutil
import sys # Keep sys for sys.exit
from pathlib import Path
from jinja2 import Environment, FileSystemLoader # Import Jinja2 at the top

# Configuration
BUILD_DIR = "build"
TEMPLATES_DIR = "core/templates/core"  # Make sure this path is correct relative to your project root
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
    Now includes current_page_name for active navigation link highlighting.
    """
    base_context = {
        "STATIC_URL": "/static/",
        "MEDIA_URL": "/media/",
        "current_page_name": current_page_name_from_build, # Added for nav highlighting
        # "BASE_URL": "/" # Optional: if you need absolute base for links, though relative usually fine for Netlify
    }
    
    # Template-specific context (ensure these match your template needs)
    # These are examples; customize them based on what each page actually needs.
    template_contexts = {
        "home.html": {
            "page_title": "UrbanPulse - Urban Data Analytics",
            "featured_insights": [ # Example data for home page cards
                {"title": "Buildings Analyzed", "value": "14,382", "icon": "bi-building"},
                {"title": "Cities Covered", "value": "237", "icon": "bi-geo-alt"},
                {"title": "Business Opportunities", "value": "3,845", "icon": "bi-shop"},
                {"title": "Data Accuracy", "value": "98.7%", "icon": "bi-check-circle"}
            ]
        },
        "investment.html": {
            "page_title": "Investment Opportunities - UrbanPulse",
            "opportunities": [ # Example data for investment page
                {"id": "prop1", "name": "Downtown Office Building", "image_slug": "property1.jpg", "type": "Commercial", "address": "123 Main St, Downtown", "safety_score": 4.0, "description": "Modern office building...", "price": "$2,450,000"},
                {"id": "prop2", "name": "East Side Mixed-Use", "image_slug": "property2.jpg", "type": "Mixed Use", "address": "456 Park Ave, East Side", "safety_score": 4.5, "description": "Newly renovated mixed-use...", "price": "$3,750,000"},
                {"id": "prop3", "name": "North District Residential", "image_slug": "property3.jpg", "type": "Residential", "address": "789 Oak St, North District", "safety_score": 3.0, "description": "Multi-family residential complex...", "price": "$4,200,000"},
                {"id": "prop4", "name": "Industrial Zone Warehouse", "image_slug": "property4.jpg", "type": "Industrial", "address": "101 Factory Rd, Industrial Zone", "safety_score": 3.5, "description": "Modern warehouse facility...", "price": "$1,850,000"},
                {"id": "prop5", "name": "West End Retail Center", "image_slug": "property5.jpg", "type": "Commercial", "address": "222 Market St, West End", "safety_score": 4.0, "description": "Established retail center...", "price": "$3,100,000"},
                {"id": "prop6", "name": "South Quarter Land", "image_slug": "property6.jpg", "type": "Vacant Land", "address": "333 River Rd, South Quarter", "safety_score": 5.0, "description": "Prime development land...", "price": "$5,800,000"},
            ]
        },
        "hazards.html": {
            "page_title": "Hazard Analysis & Sustainability - UrbanPulse",
            "hazard_reports": [ # Example data for sustainability reports
                 {"score_grade": "A", "district_name": "Downtown District", "summary": "Leading sustainability...", "green_buildings_pct": 85, "solar_capacity_mw": 12.5, "ev_stations_count": 245, "public_transit_rating": "Excellent", "waste_recycling_pct": 78, "full_report_link": "#"},
                 {"score_grade": "B", "district_name": "North District", "summary": "Strong sustainability...", "green_buildings_pct": 72, "solar_capacity_mw": 8.3, "ev_stations_count": 178, "public_transit_rating": "Good", "waste_recycling_pct": 65, "full_report_link": "#"},
                 {"score_grade": "C", "district_name": "Industrial Zone", "summary": "Moderate sustainability...", "green_buildings_pct": 45, "solar_capacity_mw": 5.1, "ev_stations_count": 62, "public_transit_rating": "Limited", "waste_recycling_pct": 52, "full_report_link": "#"},
            ]
        },
        "contact.html": {
            "page_title": "Contact Us - UrbanPulse",
            "form_action": "#"  # For static site, form submission needs a service like Netlify Forms or Formspree
        },
        "team.html": {
            "page_title": "Our Team - UrbanPulse",
            "team_members": [
                {"name": "Ali Fradi", "position": "Co-Founder", "image_slug": "team/ali_fr.jpeg", "diploma": "M.Sc in Applied Mathematics...", "bio": "Former data consultant...", "linkedin_url": "https://www.linkedin.com/in/ali-frady/", "github_url": "https://github.com/alifradi"},
                {"name": "Kais Riani", "position": "Co-Founder", "image_slug": "team/kais_r.jpg", "diploma": "Ph.D. in Computer and Information Sciences...", "bio": "Computer vision and machine learning engineer...", "linkedin_url": "https://www.linkedin.com/in/kais-riani/", "github_url": "#"},
                {"name": "Yakin Hajlaoui", "position": "Co-Founder", "image_slug": "team/yakin_h.jpg", "diploma": "Ph.D. in Applied Mathematics...", "bio": "Expert in mathematical modeling...", "linkedin_url": "https://www.linkedin.com/in/yakin-hajlaoui/", "twitter_url": "#"}
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
            "services": [ # Example data for services page
                {"name": "Data Insights & Analytics", "icon": "graph-up-arrow", "description": "Comprehensive analysis...", "points": ["Population analysis", "Infrastructure assessment"], "link":"/investment/", "name_short":"Data Insights"},
                {"name": "Investment Opportunity Analysis", "icon": "building-check", "description": "Data-driven identification...", "points": ["Property evaluation", "Market trend analysis"], "link":"/investment/", "name_short":"Investment Analysis"},
                {"name": "Hazard & Sustainability Assessment", "icon": "shield-check", "description": "Comprehensive analysis of risks...", "points": ["Environmental risk mapping", "Climate resilience"], "link":"/hazards/", "name_short":"Hazard Analysis"}
            ]
        }
    }
    
    context = base_context.copy()
    if template_name in template_contexts:
        context.update(template_contexts[template_name])
    
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
        if output_path.parent != Path(BUILD_DIR):
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
            
            # Get context, now passing the 'name' from page_config for current_page_name
            context = get_mock_context_for_template(page_config["template"], page_config["name"])
            rendered_content = template.render(**context)
            
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(rendered_content)
            
            print(f"Generated {output_file_path}")
        except Exception as e:
            print(f"Error processing template '{page_config['template']}' to '{page_config['output']}': {str(e)}")
            # Consider re-raising the exception if you want the build to fail on any template error
            # raise 

    print(f"Static site build complete! Files are in the '{BUILD_DIR}' directory.")

if __name__ == "__main__":
    main()

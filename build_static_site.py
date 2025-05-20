#!/usr/bin/env python
"""
Static site builder for UrbanPulse Django project
This script generates a static version of the UrbanPulse website for Netlify deployment
"""

import os
import shutil
# subprocess and sys are no longer needed for Jinja2 installation
from pathlib import Path
from jinja2 import Environment, FileSystemLoader # Import Jinja2 at the top

# Configuration
BUILD_DIR = "build"
# STATIC_DIR = "static" # This variable was defined but not used directly in main logic, BUILD_DIR/static is used.
TEMPLATES_DIR = "core/templates/core"  # Make sure this path is correct relative to your project root
STATIC_ASSETS_DIR = "core/static/core" # Make sure this path is correct
PAGES = [
    {"template": "home.html", "output": "index.html"},
    {"template": "investment.html", "output": "investment/index.html"},
    {"template": "hazards.html", "output": "hazards/index.html"},
    {"template": "contact.html", "output": "contact/index.html"},
    {"template": "team.html", "output": "team/index.html"},
    {"template": "contributions.html", "output": "contributions/index.html"},
    {"template": "services.html", "output": "services/index.html"},
]

def get_mock_context_for_template(template_name):
    """Generate mock context data for templates"""
    # Base context used across all templates
    base_context = {
        "STATIC_URL": "/static/",  # Assuming static files will be served from /static/
        "MEDIA_URL": "/media/",    # Assuming media files will be served from /media/
    }
    
    # Template-specific context (ensure these match your template needs)
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
                {"name": "Sarah Johnson", "position": "CEO", "image": "team/ceo.jpg"}, # Ensure these image paths are correct relative to your static/media setup
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
                {"name": "Data Insights & Analytics", "icon": "graph-up-arrow"}, # Ensure your templates can use these icon names
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

def main():
    """Main build function"""
    print("Starting UrbanPulse static site build...")
    
    # Ensure template directory exists
    if not os.path.isdir(TEMPLATES_DIR):
        print(f"Error: Templates directory '{TEMPLATES_DIR}' not found. Please check the path.")
        sys.exit(1) # Exit if templates directory is missing

    # Create build directory
    if os.path.exists(BUILD_DIR):
        print(f"Cleaning existing {BUILD_DIR} directory...")
        shutil.rmtree(BUILD_DIR)
    
    os.makedirs(BUILD_DIR, exist_ok=True)
    
    # Create directories for pages if they have subpaths
    for page in PAGES:
        output_path = Path(BUILD_DIR) / page["output"]
        if output_path.parent != Path(BUILD_DIR): # Check if output is in a subdirectory
            output_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {output_path.parent}")
    
    # Copy static assets
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
    
    # Copy media files if they exist
    media_input_dir = "media" # Assuming 'media' is at the project root
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
    
    # Process templates
    print("Processing templates...")
    
    # Set up Jinja environment
    # Ensure TEMPLATES_DIR is an absolute path or correctly relative to where the script is run from.
    # For Netlify, paths are usually relative to the repository root.
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    
    # Process each page
    for page in PAGES:
        try:
            template = env.get_template(page["template"])
            output_file_path = Path(BUILD_DIR) / page["output"]
            
            # Render template with mock context
            context = get_mock_context_for_template(page["template"])
            rendered_content = template.render(**context)
            
            # Write to output file
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(rendered_content)
            
            print(f"Generated {output_file_path}")
        except Exception as e:
            # Provide more specific error information if possible
            print(f"Error processing template '{page['template']}' to '{page['output']}': {str(e)}")
            # Depending on severity, you might want to exit or continue
            # For CI, it's often better to fail fast:
            # raise

    print(f"Static site build complete! Files are in the '{BUILD_DIR}' directory.")

if __name__ == "__main__":
    main()

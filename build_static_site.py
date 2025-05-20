#!/usr/bin/env python
"""
Static site builder for UrbanPulse Django project
This script generates a static version of the UrbanPulse website for Netlify deployment
"""

import os
import shutil
import sys 
import json 
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

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
                {"title": "Buildings Analyzed", "value": "14,382", "icon": "building"},
                {"title": "Cities Covered", "value": "237", "icon": "geo-alt"},
                {"title": "Business Opportunities", "value": "3,845", "icon": "shop"},
                {"title": "Data Accuracy", "value": "98.7%", "icon": "check-circle"}
            ]
        },
        "investment.html": {
            "page_title": "Investment Opportunities - UrbanPulse",
            "opportunities": [ 
                {"id": "prop1", "name": "Downtown Office Building", "image_slug": "property1.jpg", "type": "Commercial", "address": "123 Main St, Downtown", "safety_score": 4.0, "description": "Modern office building...", "price": "$2,450,000", "lat": 40.7128, "lng": -74.0060},
                {"id": "prop2", "name": "East Side Mixed-Use", "image_slug": "property2.jpg", "type": "Mixed Use", "address": "456 Park Ave, East Side", "safety_score": 4.5, "description": "Newly renovated mixed-use...", "price": "$3,750,000", "lat": 40.7200, "lng": -73.9800},
            ]
        },
        "hazards.html": {
            "page_title": "Hazard Analysis & Sustainability - UrbanPulse",
            "hazard_reports": [ 
                 {"score_grade": "A", "district_name": "Downtown District", "summary": "Leading sustainability...", "green_buildings_pct": 85, "solar_capacity_mw": 12.5, "full_report_link": "#"},
                 {"score_grade": "B", "district_name": "North District", "summary": "Strong sustainability...", "green_buildings_pct": 72, "solar_capacity_mw": 8.3, "full_report_link": "#"},
            ]
        },
        "contact.html": {
            "page_title": "Contact Us - UrbanPulse",
            "page_title_hero": "Contact Us", # Specific title for H1
            "form_action": "#" 
        },
        "team.html": {
            "page_title": "Our Team - UrbanPulse",
            "page_title_hero": "Our Team", # Specific title for H1
            "team_members": [
                {"name": "Ali Fradi", "position": "Co-Founder", "image_slug": "team/ali_fr.jpeg", "diploma": "M.Sc in Applied Matherematics, Polytechnique Montreal, Canada", "bio": "Former data consultant with 5+ years of experience in operational research, applied mathematics, and data engineering. Worked for financial institutions, agriculture and industries in different positions.", "linkedin_url": "https://www.linkedin.com/in/ali-frady/", "github_url": "https://github.com/alifradi", "twitter_url": ""},
                 {"name": "Kais Riani", "position": "Co-Founder", "image_slug": "team/kais_r.jpg", "diploma": "Ph.D. in Computer and Information Sciences, University of Michigan, USA", "bio": "Computer vision and machine learning engineer. Worked on urban planning and data science projects with several companies for almost 4+ years.", "linkedin_url": "https://www.linkedin.com/in/kais-riani/", "github_url": "", "twitter_url": ""},
                  {"name": "Yakin Hajlaoui", "position": "Co-Founder", "image_slug": "team/yakin_h.jpg", "diploma": "Ph.D. in Applied Matherematics, Polytechnique Montreal, Canada", "bio": "Expert in mathematical modeling for different problems. Worked for mining companies, financial institutions and startups for 4+ years.", "linkedin_url": "https://www.linkedin.com/in/yakin-hajlaoui/", "github_url": "", "twitter_url": ""}
            ]
        },
        "contributions.html": {
            "page_title": "Recent Contributions - UrbanPulse",
            "page_title_hero": "Recent Contributions", # Specific title for H1
            "contributions": [
                {"title": "Predictive Analytics", "publication_info": "Journal X", "description": "Novel framework.", "author_image_slug": "team/default_avatar.png", "author_name": "Author Y", "date": "Date Z", "link": "#"},
            ]
        },
        "services.html": {
            "page_title": "Services & Partnerships - UrbanPulse",
            "page_title_hero": "Services & Partnerships", # Title for H1
            "core_services": [
                {
                    "icon": "graph-up-arrow", "name": "Data Insights & Analytics", 
                    "description": "Comprehensive analysis of urban data to reveal patterns, trends, and opportunities across cities and neighborhoods.",
                    "points": ["Population and demographic analysis", "Infrastructure condition assessment", "Business activity and economic indicators", "Safety and inspection history analysis", "Custom data visualization and reporting"],
                    "link": "/investment/", "link_text": "Explore Data Insights"
                },
                {
                    "icon": "building-check", "name": "Investment Opportunity Analysis",
                    "description": "Data-driven identification and evaluation of urban investment opportunities with comprehensive risk and return assessment.",
                    "points": ["Property and location evaluation", "Market trend analysis and forecasting", "Comparative ROI modeling", "Vacancy and business potential assessment", "Investment risk profiling"],
                    "link": "/investment/", "link_text": "Explore Investment Analysis"
                },
                {
                    "icon": "shield-check", "name": "Hazard & Sustainability Assessment",
                    "description": "Comprehensive analysis of environmental risks, hazards, and sustainability metrics for urban areas and properties.",
                    "points": ["Environmental risk mapping", "Climate resilience evaluation", "Green energy installation analysis", "Sustainability scoring and benchmarking", "Hazard mitigation recommendations"],
                    "link": "/hazards/", "link_text": "Explore Hazard Analysis"
                }
            ],
            "specialized_services": [
                {
                    "icon": "people", "name": "Strategic Consulting", 
                    "description": "Expert guidance on urban development strategies, investment decisions, and sustainability initiatives based on comprehensive data analysis.",
                    "points": ["Urban development strategy formulation", "Investment portfolio optimization", "Sustainability transformation planning", "Risk mitigation strategy development"],
                    "link_url": "/contact/", "link_text": "Request Consultation"
                },
                {
                    "icon": "gear", "name": "Custom Data Solutions",
                    "description": "Tailored data collection, analysis, and visualization solutions designed to address specific urban challenges and opportunities.",
                    "points": ["Custom data collection and integration", "Proprietary analytics model development", "Specialized visualization dashboards", "Data API and integration services"],
                    "link_url": "/contact/", "link_text": "Discuss Your Needs"
                },
                {
                    "icon": "mortarboard", "name": "Training & Capacity Building",
                    "description": "Comprehensive training programs to help organizations build internal capacity for urban data analytics and data-driven decision making.",
                    "points": ["Urban data literacy workshops", "Analytics platform training", "Data-driven decision making seminars", "Custom training curriculum development"],
                    "link_url": "/contact/", "link_text": "Explore Training Options"
                },
                {
                    "icon": "clipboard-data", "name": "Research & Development",
                    "description": "Collaborative research initiatives to advance urban data analytics methodologies, tools, and applications for specific sectors or challenges.",
                    "points": ["Sector-specific research partnerships", "Methodology development and validation", "Pilot program design and implementation", "Academic and industry collaborations"],
                    "link_url": "/contact/", "link_text": "Discuss Research Opportunities"
                }
            ],
            "service_packages": [
                {
                    "name": "Starter", "price": "$2,500", "period": "/month", 
                    "lead_text": "Essential urban data insights for smaller projects and organizations.",
                    "features": ["Basic data analytics dashboard", "Monthly insights reports", "Access to core datasets", "Single city coverage", "Email support"],
                    "non_features": ["Custom analytics", "API access", "Dedicated consultant"],
                    "button_link": "/contact/", "button_text": "Get Started", "is_featured": False
                },
                {
                    "name": "Professional", "price": "$6,500", "period": "/month",
                    "lead_text": "Comprehensive analytics and insights for medium-sized organizations and projects.",
                    "features": ["Advanced analytics dashboard", "Weekly insights reports", "Access to all datasets", "Up to 3 cities coverage", "Priority support", "Basic custom analytics", "Limited API access"],
                    "non_features": ["Dedicated consultant"],
                    "button_link": "/contact/", "button_text": "Get Started", "is_featured": True
                },
                {
                    "name": "Enterprise", "price": "Custom", "period": " pricing",
                    "lead_text": "Tailored solutions for large organizations with complex urban data needs.",
                    "features": ["Custom analytics platform", "Real-time data and reporting", "Full dataset access + custom data", "Unlimited city coverage", "24/7 premium support", "Advanced custom analytics", "Full API access", "Dedicated consultant team"],
                    "non_features": [],
                    "button_link": "/contact/", "button_text": "Contact Sales", "is_featured": False
                }
            ],
            "partners": [
                {"image_slug": "partner1.png", "name": "Technology Solutions"},
                {"image_slug": "partner2.png", "name": "Research Institute"},
                {"image_slug": "partner3.png", "name": "Government Agency"},
                {"image_slug": "partner4.png", "name": "Investment Group"},
                {"image_slug": "partner5.png", "name": "University Partner"},
                {"image_slug": "partner6.png", "name": "Sustainability Alliance"},
                {"image_slug": "partner7.png", "name": "Data Provider"},
                {"image_slug": "partner8.png", "name": "Industry Association"}
            ],
            "testimonials": [
                {
                    "stars": 5, "text": "UrbanPulse's data analytics transformed our investment strategy, helping us identify opportunities we would have otherwise missed. Their hazard analysis saved us from a potentially disastrous investment in a flood-prone area.",
                    "image_slug": "testimonial1.jpg", "client_name": "Jennifer Martinez", "client_title": "Director of Investments, Urban Growth Capital"
                },
                {
                    "stars": 5, "text": "As a city planner, I've found UrbanPulse's insights invaluable for making data-driven decisions about infrastructure investments. Their sustainability metrics have helped us prioritize green initiatives with the highest impact.",
                    "image_slug": "testimonial2.jpg", "client_name": "David Wilson", "client_title": "Chief Urban Planner, Metropolitan Development Authority"
                },
                {
                    "stars": 4, "text": "The ROI on our partnership with UrbanPulse has been exceptional. Their custom analytics platform has become an essential tool for our development team, providing insights that drive our strategic decisions.", # Assuming 4.5 stars means 4 full stars
                    "image_slug": "testimonial3.jpg", "client_name": "Michael Chang", "client_title": "CEO, Innovative Urban Developers"
                }
            ]
        }
    }
    
    context = base_context.copy()
    
    if template_name in template_specific_data:
        context.update(template_specific_data[template_name])
    
    if "page_title" not in context: # Fallback for HTML <title>
        generic_title = current_page_name_from_build.replace('_', ' ').title()
        context["page_title"] = f"{generic_title} - UrbanPulse"
    
    # Ensure page_title_hero exists for templates that use it, even if empty
    if template_name in ["contact.html", "team.html", "contributions.html", "services.html"] and "page_title_hero" not in context:
        context["page_title_hero"] = context["page_title"] # Default hero title to page title

    # Set default for lists of dictionaries to prevent missing key errors
    if context.get("opportunities"):
        for item in context["opportunities"]:
            item.setdefault("id", "")
            item.setdefault("name", "N/A")
            item.setdefault("image_slug", "property_placeholder.jpg")
            item.setdefault("type", "N/A")
            item.setdefault("address", "N/A")
            item.setdefault("safety_score", 0)
            item.setdefault("description", "")
            item.setdefault("price", "N/A")
            item.setdefault("lat", 0)
            item.setdefault("lng", 0)
    if context.get("hazard_reports"):
        for item in context["hazard_reports"]:
            item.setdefault("score_grade", "N/A")
            item.setdefault("district_name", "N/A")
            item.setdefault("summary", "")
            item.setdefault("green_buildings_pct", 0)
            item.setdefault("solar_capacity_mw", 0)
            item.setdefault("full_report_link", "#")
    if context.get("team_members"):
        for item in context["team_members"]:
            item.setdefault("name", "N/A")
            item.setdefault("position", "N/A")
            item.setdefault("image_slug", "team/default_avatar.png")
            item.setdefault("diploma", "")
            item.setdefault("bio", "")
            item.setdefault("linkedin_url", "")
            item.setdefault("github_url", "")
            item.setdefault("twitter_url", "")
    if context.get("contributions"):
        for item in context["contributions"]:
            item.setdefault("title", "N/A")
            item.setdefault("publication_info", "")
            item.setdefault("description", "")
            item.setdefault("author_image_slug", "team/default_avatar.png")
            item.setdefault("author_name", "N/A")
            item.setdefault("date", "")
            item.setdefault("link", "#")
    if context.get("services"):
        for item in context["services"]:
            item.setdefault("name", "N/A")
            item.setdefault("icon", "briefcase")
            item.setdefault("description", "")
            item.setdefault("points", [])
            item.setdefault("link", "#")
            item.setdefault("name_short", "Service")
    if context.get("featured_insights"):
        for item in context["featured_insights"]:
            item.setdefault("title", "N/A")
            item.setdefault("value", "N/A")
            item.setdefault("icon", "info-circle")


    return context

def main():
    print("Starting UrbanPulse static site build...")
    if not os.path.isdir(TEMPLATES_DIR):
        print(f"Error: Templates directory '{TEMPLATES_DIR}' not found.")
        sys.exit(1)
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR, exist_ok=True)

    for page_config in PAGES:
        output_path = Path(BUILD_DIR) / page_config["output"]
        if output_path.parent != Path(BUILD_DIR):
            output_path.parent.mkdir(parents=True, exist_ok=True)
    
    static_output_dir = Path(BUILD_DIR) / "static"
    if os.path.exists(STATIC_ASSETS_DIR):
        shutil.copytree(STATIC_ASSETS_DIR, static_output_dir, dirs_exist_ok=True)
    else:
        print(f"Warning: Static assets directory '{STATIC_ASSETS_DIR}' not found.")
    
    print("Processing templates...")
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(['html', 'xml']),
        extensions=['jinja2.ext.loopcontrols'] 
    )
    env.filters['tojson'] = json.dumps

    for page_config in PAGES:
        try:
            template = env.get_template(page_config["template"])
            context = get_mock_context_for_template(page_config["template"], page_config["name"])
            rendered_content = template.render(**context)
            output_file_path = Path(BUILD_DIR) / page_config["output"]
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(rendered_content)
            print(f"Generated {output_file_path}")
        except Exception as e:
            print(f"Error processing template '{page_config['template']}' to '{page_config['output']}': {str(e)}")
            # sys.exit(1) # Optionally fail build on any error

    print(f"Static site build complete! Files are in the '{BUILD_DIR}' directory.")

if __name__ == "__main__":
    main()

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
                {"title": "Cities Covered", "value": "4", "icon": "geo-alt"},
                #{"title": "Business Opportunities", "value": "3,845", "icon": "shop"},
                {"title": "Data Accuracy", "value": "Gold to silver data sources", "icon": "check-circle"}
            ]
        },
        "investment.html": {
            "page_title": "Investment Opportunities - UrbanPulse",
             "page_title_hero": "Investment Opportunities",
            "opportunities": [ 
                {"id": "prop1", "name": "Downtown Office Building", "image_slug": "property1.jpg", "type": "Commercial", "address": "123 Main St, Downtown", "safety_score": 4.0, "description": "Modern office building...", "price": "$2,450,000", "lat": 40.7128, "lng": -74.0060},
                {"id": "prop2", "name": "East Side Mixed-Use", "image_slug": "property2.jpg", "type": "Mixed Use", "address": "456 Park Ave, East Side", "safety_score": 4.5, "description": "Newly renovated mixed-use...", "price": "$3,750,000", "lat": 40.7200, "lng": -73.9800},
            ]
        },
        "hazards.html": {
            "page_title": "Hazard Analysis & Sustainability - UrbanPulse",
            "page_title_hero": "Hazard Analysis & Sustainability",
            "sustainability_reports": [ # Renamed from hazard_reports for clarity
                 {"score_grade": "A", "district_name": "Downtown District", "summary": "Leading sustainability initiatives with extensive green building adoption and renewable energy integration.", "green_buildings_pct": 85, "solar_capacity_mw": 12.5, "ev_stations_count": 245, "public_transit_rating": "Excellent", "waste_recycling_pct": 78, "full_report_link": "#"},
                 {"score_grade": "B", "district_name": "North District", "summary": "Strong sustainability performance with ongoing improvements in renewable energy and transportation.", "green_buildings_pct": 72, "solar_capacity_mw": 8.3, "ev_stations_count": 178, "public_transit_rating": "Good", "waste_recycling_pct": 65, "full_report_link": "#"},
                 {"score_grade": "C", "district_name": "Industrial Zone", "summary": "Moderate sustainability with significant improvement opportunities in emissions and energy efficiency.", "green_buildings_pct": 45, "solar_capacity_mw": 5.1, "ev_stations_count": 62, "public_transit_rating": "Limited", "waste_recycling_pct": 52, "full_report_link": "#"},
                 {"score_grade": "B", "district_name": "East Side", "summary": "Strong sustainability metrics with recent improvements in green building adoption and public transit.", "green_buildings_pct": 68, "solar_capacity_mw": 7.8, "ev_stations_count": 156, "public_transit_rating": "Very Good", "waste_recycling_pct": 70, "full_report_link": "#"},
                 {"score_grade": "D", "district_name": "South Quarter", "summary": "Below average sustainability performance with significant room for improvement across all metrics.", "green_buildings_pct": 32, "solar_capacity_mw": 2.3, "ev_stations_count": 28, "public_transit_rating": "Poor", "waste_recycling_pct": 35, "full_report_link": "#"},
                 {"score_grade": "C", "district_name": "West End", "summary": "Average sustainability performance with recent improvements in renewable energy adoption.", "green_buildings_pct": 55, "solar_capacity_mw": 6.2, "ev_stations_count": 95, "public_transit_rating": "Average", "waste_recycling_pct": 58, "full_report_link": "#"}
            ],
            "historical_events_data": [
                {"title": "Downtown Flooding", "severity_class": "danger", "severity_text": "Critical", "date_location": "June 15, 2023 | Downtown District", "description": "Severe flooding affected 60% of the downtown area...", "economic_impact": "$42.5 Million", "recovery_time": "8 Months", "response_rating": "Adequate (3/5)", "impact_class": "high", "report_link": "#"},
                {"title": "Industrial Zone Fire", "severity_class": "warning", "severity_text": "Major", "date_location": "August 3, 2022 | Industrial Zone", "description": "Fire at a manufacturing facility spread to adjacent properties...", "economic_impact": "$18.7 Million", "recovery_time": "5 Months", "response_rating": "Good (4/5)", "impact_class": "medium", "report_link": "#"},
                {"title": "Power Grid Failure", "severity_class": "warning", "severity_text": "Major", "date_location": "January 12, 2022 | Multiple Districts", "description": "Widespread power outage during winter storm...", "economic_impact": "$23.2 Million", "recovery_time": "3 Months", "response_rating": "Poor (2/5)", "impact_class": "medium", "report_link": "#"},
                {"title": "Chemical Spill", "severity_class": "info", "severity_text": "Moderate", "date_location": "March 28, 2021 | Industrial Zone", "description": "Contained chemical spill at manufacturing facility...", "economic_impact": "$3.8 Million", "recovery_time": "2 Months", "response_rating": "Excellent (5/5)", "impact_class": "low", "report_link": "#"},
                {"title": "Water Main Break", "severity_class": "secondary", "severity_text": "Minor", "date_location": "October 5, 2020 | East Side", "description": "Water main break affected service to approximately 200 residences...", "economic_impact": "$850,000", "recovery_time": "2 Weeks", "response_rating": "Good (4/5)", "impact_class": "low", "report_link": "#"}
            ],
            "district_risk_evolution": [
                {"name": "Downtown", "current_risk_class": "medium", "current_risk_text": "Medium (60%)", "proj5_risk_class": "medium", "proj5_risk_text": "Medium (65%)", "proj15_risk_class": "high", "proj15_risk_text": "High (72%)", "proj25_risk_class": "high", "proj25_risk_text": "High (78%)", "vulnerabilities": "Flooding, Infrastructure Age, Heat Island Effect"},
                {"name": "North District", "current_risk_class": "low", "current_risk_text": "Low (35%)", "proj5_risk_class": "low", "proj5_risk_text": "Low (38%)", "proj15_risk_class": "medium", "proj15_risk_text": "Medium (52%)", "proj25_risk_class": "medium", "proj25_risk_text": "Medium (58%)", "vulnerabilities": "Wildland Interface, Water Supply"},
                {"name": "East Side", "current_risk_class": "medium", "current_risk_text": "Medium (55%)", "proj5_risk_class": "low", "proj5_risk_text": "Low (48%)", "proj15_risk_class": "low", "proj15_risk_text": "Low (42%)", "proj25_risk_class": "low", "proj25_risk_text": "Low (40%)", "vulnerabilities": "Current Infrastructure, Improving with Investments"},
                {"name": "West End", "current_risk_class": "medium", "current_risk_text": "Medium (58%)", "proj5_risk_class": "medium", "proj5_risk_text": "Medium (62%)", "proj15_risk_class": "medium", "proj15_risk_text": "Medium (65%)", "proj25_risk_class": "high", "proj25_risk_text": "High (70%)", "vulnerabilities": "Coastal Proximity, Aging Infrastructure"},
                {"name": "South Quarter", "current_risk_class": "high", "current_risk_text": "High (75%)", "proj5_risk_class": "high", "proj5_risk_text": "High (80%)", "proj15_risk_class": "high", "proj15_risk_text": "High (85%)", "proj25_risk_class": "high", "proj25_risk_text": "High (88%)", "vulnerabilities": "Flood Plain, Industrial Contamination, Infrastructure"},
                {"name": "Industrial Zone", "current_risk_class": "high", "current_risk_text": "High (72%)", "proj5_risk_class": "medium", "proj5_risk_text": "Medium (65%)", "proj15_risk_class": "medium", "proj15_risk_text": "Medium (60%)", "proj25_risk_class": "medium", "proj25_risk_text": "Medium (55%)", "vulnerabilities": "Environmental Hazards, Improving with Remediation"}
            ]
        },
        "contact.html": {
            "page_title": "Contact Us - UrbanPulse",
            "page_title_hero": "Contact Us", # Specific title for H1
            # MODIFIED: Update this to your Formspree endpoint
            "form_action": "https://formspree.io/f/mblobwqq" 
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
                #    "name": "Starter", "price": "$2,500", "period": "/month", 
                #    "lead_text": "Essential urban data insights for smaller projects and organizations.",
                #    "features": ["Basic data analytics dashboard", "Monthly insights reports", "Access to core datasets", "Single city coverage", "Email support"],
                #    "non_features": ["Custom analytics", "API access", "Dedicated consultant"],
                #    "button_link": "/contact/", "button_text": "Get Started", "is_featured": False
                },
                {
                #    "name": "Professional", "price": "$6,500", "period": "/month",
                #    "lead_text": "Comprehensive analytics and insights for medium-sized organizations and projects.",
                #    "features": ["Advanced analytics dashboard", "Weekly insights reports", "Access to all datasets", "Up to 3 cities coverage", "Priority support", "Basic custom analytics", "Limited API access"],
                #    "non_features": ["Dedicated consultant"],
                #    "button_link": "/contact/", "button_text": "Get Started", "is_featured": True
                },
                {
                #    "name": "Enterprise", "price": "Custom", "period": " pricing",
                #    "lead_text": "Tailored solutions for large organizations with complex urban data needs.",
                #    "features": ["Custom analytics platform", "Real-time data and reporting", "Full dataset access + custom data", "Unlimited city coverage", "24/7 premium support", "Advanced custom analytics", "Full API access", "Dedicated consultant team"],
                #    "non_features": [],
                #    "button_link": "/contact/", "button_text": "Contact Sales", "is_featured": False
                }
            ],
            "partners": [

              #  {"image_slug": "goc.PNG", "name": "Partner"},
              #  {"image_slug": "qatar-digital-government.png", "name": "Partner"},
              #  {"image_slug": "LogoTXTW.png", "name": "Partner"}
            ],
            "testimonials": [
                {
              #      "stars": 5, "text": "UrbanPulse's data analytics transformed our investment strategy, helping us identify opportunities we would have otherwise missed. Their hazard analysis saved us from a potentially disastrous investment in a flood-prone area.",
              #      "image_slug": "testimonial1.jpg", "client_name": "Jennifer Martinez", "client_title": "Director of Investments, Urban Growth Capital"
                },
                {
              #      "stars": 5, "text": "As a city planner, I've found UrbanPulse's insights invaluable for making data-driven decisions about infrastructure investments. Their sustainability metrics have helped us prioritize green initiatives with the highest impact.",
              #      "image_slug": "testimonial2.jpg", "client_name": "David Wilson", "client_title": "Chief Urban Planner, Metropolitan Development Authority"
                },
                {
               #     "stars": 4, "text": "The ROI on our partnership with UrbanPulse has been exceptional. Their custom analytics platform has become an essential tool for our development team, providing insights that drive our strategic decisions.", # Assuming 4.5 stars means 4 full stars
               #     "image_slug": "testimonial3.jpg", "client_name": "Michael Chang", "client_title": "CEO, Innovative Urban Developers"
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

    list_configs = {
        "opportunities": {"id": "", "name": "N/A", "image_slug": "property_placeholder.jpg", "type": "N/A", "address": "N/A", "safety_score": 0, "description": "", "price": "N/A", "lat": 0, "lng": 0},
        "sustainability_reports": {"score_grade": "N/A", "district_name": "N/A", "summary": "", "green_buildings_pct": 0, "solar_capacity_mw": 0, "ev_stations_count":0, "public_transit_rating":"N/A", "waste_recycling_pct":0, "full_report_link": "#"}, # Added setdefault for sustainability_reports
        "historical_events_data": {"title": "N/A", "severity_class": "secondary", "severity_text": "N/A", "date_location": "N/A", "description": "", "economic_impact": "N/A", "recovery_time": "N/A", "response_rating": "N/A", "impact_class": "low", "report_link": "#"},
        "district_risk_evolution": {"name": "N/A", "current_risk_class": "low", "current_risk_text": "N/A", "proj5_risk_class": "low", "proj5_risk_text": "N/A", "proj15_risk_class": "low", "proj15_risk_text": "N/A", "proj25_risk_class": "low", "proj25_risk_text": "N/A", "vulnerabilities": ""},
        "team_members": {"name": "N/A", "position": "N/A", "image_slug": "team/default_avatar.png", "diploma": "", "bio": "", "linkedin_url": "", "github_url": "", "twitter_url": ""},
        "contributions": {"title": "N/A", "publication_info": "", "description": "", "author_image_slug": "team/default_avatar.png", "author_name": "N/A", "date": "", "link": "#"},
        "core_services": {"icon": "briefcase", "name": "N/A", "description": "", "points": [], "link": "#", "link_text": "Learn More"},
        "specialized_services": {"icon": "gear", "name": "N/A", "description": "", "points": [], "link_url": "#", "link_text": "Learn More"},
        "service_packages": {"name": "N/A", "price": "Contact Us", "period": "", "lead_text": "", "features": [], "non_features": [], "button_link": "#", "button_text": "Details", "is_featured": False},
        "partners": {"image_slug": "partners/default.png", "name": "N/A"},
        "testimonials": {"stars": 0, "text": "", "image_slug": "testimonials/default.jpg", "client_name": "N/A", "client_title": ""},
        "featured_insights": {"title": "N/A", "value": "N/A", "icon": "info-circle"}
    }

    for list_key, defaults in list_configs.items():
        if context.get(list_key): 
            for item in context[list_key]: 
                if isinstance(item, dict): 
                    for default_key, default_value in defaults.items():
                        item.setdefault(default_key, default_value)
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
    
    media_input_dir = "media" 
    media_output_dir = Path(BUILD_DIR) / "media"
    if os.path.exists(media_input_dir):
        shutil.copytree(media_input_dir, media_output_dir, dirs_exist_ok=True)
    else:
        print(f"Info: Media directory '{media_input_dir}' not found. Skipping media file copy.")

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
            # To make Netlify build fail on any error, uncomment the next line
            # sys.exit(1) 

    print(f"Static site build complete! Files are in the '{BUILD_DIR}' directory.")

if __name__ == "__main__":
    main()

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
            "page_title": "UrbanPulse - Global Urban Intelligence for Commercial Expansion",
            "hero_title": "Global Urban Intelligence for Strategic Expansion",
            "featured_insights": [
                {"title": "Global POIs", "value": "60,000+", "icon": "bi-geo-alt"},
                {"title": "Key Markets", "value": "7+ (QA, AE, SA, CA, BH, EG)", "icon": "bi-globe"},
                {"title": "Verified Businesses", "value": "5,000+", "icon": "bi-shop"},
                {"title": "Update Frequency", "value": "Weekly", "icon": "bi-arrow-repeat"}
            ]
        },
        "investment.html": {
            "page_title": "Urban Data Insights - UrbanPulse",
            "page_title_hero": "Urban Data Insights",
            "insight_posts": [
                {
                    "title": "Quality of Life in Montreal",
                    "image_path": "showoff/quality of life in montreal.jpeg",
                    "paragraph": "Our advanced Machine Learning models analyze and map the Quality of Life across Montreal's neighborhoods, transforming complex urban data into precise visual intelligence. This mapping of ML results empowers real estate companies and brokers to accurately identify superior residential locations, providing the reassurance needed to spot high-potential areas and make informed investment decisions."
                }
            ]
        },
        "hazards.html": {
            "page_title": "Urban Opportunity & Site Analysis - UrbanPulse",
            "page_title_hero": "Urban Opportunity & Site Analysis",
            "sustainability_reports": [
                 {"score_grade": "A", "district_name": "Mile End, Montreal", "summary": "High commercial density with superior pedestrian catchment and artisanal cluster potential.", "green_buildings_pct": 82, "solar_capacity_mw": 5.0, "ev_stations_count": 45, "public_transit_rating": "Excellent (STM)", "waste_recycling_pct": 78, "full_report_link": "#"},
                 {"score_grade": "A", "district_name": "Lusail, Qatar", "summary": "Rapidly growing business district with premium infrastructure and international brand attraction.", "green_buildings_pct": 92, "solar_capacity_mw": 15.0, "ev_stations_count": 120, "public_transit_rating": "Excellent (Metro Link)", "waste_recycling_pct": 82, "full_report_link": "#"},
                 {"score_grade": "B", "district_name": "Liberty Village, Toronto", "summary": "Young professional demographic with high density of service-based commercial POIs.", "green_buildings_pct": 75, "solar_capacity_mw": 8.2, "ev_stations_count": 85, "public_transit_rating": "Very Good (TTC)", "waste_recycling_pct": 70, "full_report_link": "#"},
                 {"score_grade": "B", "district_name": "Downtown Dubai, UAE", "summary": "World-class retail anchor density and massive international tourist catchment.", "green_buildings_pct": 88, "solar_capacity_mw": 10.5, "ev_stations_count": 310, "public_transit_rating": "Very Good", "waste_recycling_pct": 75, "full_report_link": "#"}
            ],
            "historical_events_data": [
                {"title": "Doha Flash Flood Event", "severity_class": "danger", "severity_text": "Critical", "date_location": "April 2024 | Doha, Qatar", "description": "Record rainfall led to significant infrastructure disruptions and basement flooding in low-elevation residential clusters.", "economic_impact": "$15 Million (Est.)", "recovery_time": "3 Weeks", "response_rating": "Rapid (4/5)", "impact_class": "high", "report_link": "#"},
                {"title": "Dubai Extreme Heatwave", "severity_class": "warning", "severity_text": "Major", "date_location": "August 2023 | Dubai, UAE", "description": "Peak temperatures exceeding 50°C stressed cooling systems in older architectural clusters.", "economic_impact": "Operational Surge", "recovery_time": "Climate Seasonal", "response_rating": "Good (4/5)", "impact_class": "medium", "report_link": "#"}
            ],
            "district_risk_evolution": [
                {"name": "Doha Bay", "current_risk_class": "medium", "current_risk_text": "Medium (Flood/Heat)", "proj5_risk_class": "medium", "proj5_risk_text": "Mitigated (60%)", "proj15_risk_class": "high", "proj15_risk_text": "High (Heat Stress)", "proj25_risk_class": "high", "proj25_risk_text": "High (75%)", "vulnerabilities": "Sea Level Rise, Urban Heat Island"},
                {"name": "Riyadh Center", "current_risk_class": "low", "current_risk_text": "Low (Seismic)", "proj5_risk_class": "low", "proj5_risk_text": "Low (40%)", "proj15_risk_class": "medium", "proj15_risk_text": "Medium (Water Stress)", "proj25_risk_class": "medium", "proj25_risk_text": "Medium (55%)", "vulnerabilities": "Water Depletion, Temperature Extremes"}
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
                {"name": "Ali Fradi", "position": "Co-Founder", "image_slug": "team/IMG_9658.png", "diploma": "M.Sc in Applied Matherematics, Polytechnique Montreal, Canada", "bio": "Former data consultant with 5+ years of experience in operational research, applied mathematics, and data engineering. Worked for financial institutions, agriculture and industries in different positions.", "linkedin_url": "https://www.linkedin.com/in/ali-frady/", "github_url": "https://github.com/alifradi", "twitter_url": ""},
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
            "page_title": "Global Urban Intelligence Services - UrbanPulse",
            "page_title_hero": "Global Site Selection & Market Analysis",
            "core_services": [
                {
                    "icon": "globe", "name": "Cross-Border Market Benchmarking", 
                    "description": "Compare commercial viability across global cities from Montreal to Dubai using standardized POI metrics.",
                    "points": ["Identify undervalued commercial zones in 7+ countries", "Analyze 60,000+ POIs for catchment potential", "Compare restaurant density and competitive clusters", "Benchmarking international expansion feasibility"],
                    "link": "/investment/", "link_text": "Compare Global Markets"
                },
                {
                    "icon": "shop", "name": "Commercial Site Selection",
                    "description": "Helping international brands and restaurant chains find the 'best spot' using high-density amenity mapping.",
                    "points": ["Micro-location analysis for high-footfall categories", "Demographic-anchor correlation mapping", "Proximity analysis to 5,000+ geocoded businesses", "Custom catchment reports for international retail"],
                    "link": "/investment/", "link_text": "Find Your Site"
                },
                {
                    "icon": "graph-up-arrow", "name": "Opportunity Indexing",
                    "description": "Score districts based on commercial potential, worker proximity, and transit density.",
                    "points": ["Urban Opportunity Index (0-100) per district", "Identify 'Retail Deserts' with high unserved demand", "Transit accessibility scoring for worker hubs", "Visual heatmap of commercial activity"],
                    "link": "/investment/", "link_text": "Analyze Opportunities"
                }
            ],
            "specialized_services": [
                {
                    "icon": "briefcase", "name": "Strategic Growth Consulting", 
                    "description": "Expert guidance for international companies entering new markets in North America or the GCC.",
                    "points": ["Market entry strategy for international brands", "Portfolio expansion optimization", "Commercial risk & opportunity assessment", "Site-specific feasibility studies"],
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

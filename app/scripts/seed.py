"""
One-time seeder: creates the admin user and seeds initial portfolio data.

Usage:
    python -m app.scripts.seed
"""

import asyncio

from app.core.config import settings
from app.core.database import col
from app.core.security import hash_password

PROJECTS = [
    {"name": "WEBSec-Tester", "type": "Fullstack", "cat": "personal", "tags": ["Python", "FastAPI", "Jinja2", "Docker"], "url": "https://websec-tester.onrender.com/", "img": "https://i.ibb.co/hJVn0vK7/websec-tester.png", "desc": "A web security testing tool."},
    {"name": "Streamify", "type": "Fullstack", "cat": "personal", "tags": ["React JS", "FastAPI"], "url": "https://github.com/satishsinha/streamify_project", "img": "https://i.ibb.co/Rgsw85d/streamify.jpg", "desc": "Streaming platform."},
    {"name": "TranscodePlus", "type": "Backend", "cat": "personal", "tags": ["FastAPI"], "url": "https://github.com/satishsinha/TranscodePlus", "img": "https://i.ibb.co/fGQxc9W/transcode.jpg", "desc": "Media transcoding service."},
    {"name": "Oneaccess", "type": "Fullstack", "cat": "personal", "tags": ["React JS", "FastAPI"], "url": "https://github.com/kunal-paul04/OneAccess", "img": "https://i.ibb.co/5kMNFJk/oneaccess.jpg", "desc": "Single sign-on portal."},
    {"name": "Streamlet Resume", "type": "Fullstack", "cat": "personal", "tags": ["Python", "Streamlit"], "url": "https://kunal-paul-resume.streamlit.app/", "img": "https://i.ibb.co/tcMMFNj/streamlet-resume.png", "desc": "Interactive resume."},
    {"name": "MY Bharat", "type": "Backend", "cat": "professional", "tags": ["Python", "Flask API"], "url": "https://mybharat.gov.in/", "img": "https://i.ibb.co/cC9fj1g/mybharat.png", "desc": "Youth volunteering platform."},
    {"name": "Parinaam Manjusha", "type": "Fullstack", "cat": "professional", "tags": ["PHP", "CodeIgniter"], "url": "https://cbse.digitallocker.gov.in/", "img": "https://i.ibb.co/2qLnY1c/parinaam-manjusha.png", "desc": "CBSE result repository."},
    {"name": "NAD", "type": "Backend", "cat": "professional", "tags": ["PHP", "Python", "CodeIgniter"], "url": "https://nad.digilocker.gov.in/", "img": "https://i.ibb.co/bW44DZ4/nad.png", "desc": "National Academic Depository."},
    {"name": "DigiLocker", "type": "Backend", "cat": "professional", "tags": ["PHP", "Python", "Flask API"], "url": "https://www.digilocker.gov.in/", "img": "https://i.ibb.co/jMFsw3K/digilocker.png", "desc": "National digital document wallet."},
]

EXPERIENCE = [
    {"role": "Deputy Manager, Software Development", "company": "Digital India Corporation · MeitY", "start": "Apr 2024", "end": "Present", "tags": ["Python", "FastAPI", "AWS", "Docker", "ELK", "RabbitMQ", "Airflow"], "desc": "Spearheaded design & deployment of DigiLocker, NAD, ABC, and MY Bharat serving millions. Engineered scalable microservices with AWS S3, Docker, FastAPI. Orchestrated workflows with Apache Airflow, boosting automation and reliability."},
    {"role": "Assistant Manager, Software Development", "company": "Digital India Corporation · MeitY", "start": "Feb 2023", "end": "Apr 2024", "tags": ["Python", "PHP", "QA", "UI Design"], "desc": "Led testing framework resolving 200+ critical bugs before launch. Designed government UI used by 100K+ citizens. Architected complex client-server solutions boosting customer satisfaction significantly."},
    {"role": "Software Developer", "company": "Digital India Corporation · NeSDA", "start": "Mar 2022", "end": "Feb 2023", "tags": ["DigiLocker", "NAD", "API Integration"], "desc": "Worked on DigiLocker and NAD. Reduced manual data entry by 50%. Led third-party API integration increasing user engagement by 20%. Identified and resolved critical software bugs ensuring optimal reliability."},
    {"role": "Digital Marketing Executive", "company": "D.R. Brijmohan & Sons Pvt. Ltd.", "start": "Dec 2020", "end": "Feb 2022", "tags": ["SEO", "A/B Testing", "Email Marketing"], "desc": "Planned and executed web, SEO, and social campaigns. Boosted social media engagement by 45%. Improved conversion rates with A/B testing and UX best practices."},
    {"role": "Software Developer", "company": "Technowell Services Pvt. Ltd.", "start": "Dec 2018", "end": "Nov 2020", "tags": ["PHP", "MySQL", "HTML/CSS", "JavaScript"], "desc": "Built customized software for diverse clients with PHP & MySQL. Enhanced UX with HTML/CSS interfaces. Integrated third-party services and optimized AJAX and JavaScript features."},
]

SKILLS = [
    {"name": "Python", "cat": "Backend", "pct": 95},
    {"name": "PHP (CodeIgniter)", "cat": "Backend", "pct": 90},
    {"name": "FastAPI / Flask", "cat": "Backend", "pct": 92},
    {"name": "MySQL / PostgreSQL", "cat": "Backend", "pct": 85},
    {"name": "React JS", "cat": "Frontend", "pct": 75},
    {"name": "HTML / CSS / JS", "cat": "Frontend", "pct": 85},
    {"name": "AWS (S3, EC2, Lambda)", "cat": "DevOps & Cloud", "pct": 85},
    {"name": "Docker / Microservices", "cat": "DevOps & Cloud", "pct": 88},
    {"name": "Apache Airflow", "cat": "DevOps & Cloud", "pct": 80},
    {"name": "ELK Stack", "cat": "Tools & Infra", "pct": 82},
    {"name": "Redis / RabbitMQ", "cat": "Tools & Infra", "pct": 80},
    {"name": "Git / CI-CD", "cat": "Tools & Infra", "pct": 88},
]

EDUCATION = [
    {"deg": "Master of Computer Application", "short": "MCA", "inst": "Assam Science and Technology University, Guwahati", "year": "2018", "grade": "7.58"},
    {"deg": "Bachelor of Computer Application", "short": "BCA", "inst": "Gauhati University, Guwahati", "year": "2015", "grade": "7.0"},
    {"deg": "Higher Secondary — Science Stream", "short": "HSC", "inst": "Kendriya Vidyalaya Narangi, Guwahati · CBSE", "year": "2012", "grade": ""},
    {"deg": "Secondary School Certificate", "short": "SSC", "inst": "Kendriya Vidyalaya Narangi, Guwahati · CBSE", "year": "2010", "grade": ""},
]

CONTACT = {
    "name": "Kunal Kanti Paul",
    "email": "kunalkantipaul@gmail.com",
    "phone1": "+91 96781 39456",
    "phone2": "+91 700261 3771",
    "location": "Guwahati, Assam, India",
    "resume": "https://drive.google.com/file/d/1qvV6Kvmmz1DjzNZ7C5g3Nl5Q3w6RcTm5/view?usp=sharing",
    "github": "https://github.com/kunal-paul04",
    "linkedin": "",
    "available": True,
}


async def seed() -> None:
    # Admin user
    if not settings.ADMIN_PASSWORD:
        print("ERROR: Set ADMIN_PASSWORD in .env before seeding.")
        return

    existing = await col("users").find_one({"username": settings.ADMIN_USERNAME})
    if existing:
        print(f"Admin user '{settings.ADMIN_USERNAME}' already exists — skipping.")
    else:
        await col("users").insert_one(
            {"username": settings.ADMIN_USERNAME, "password": hash_password(settings.ADMIN_PASSWORD)}
        )
        print(f"Created admin user: {settings.ADMIN_USERNAME}")

    # Portfolio collections
    for collection, data in [
        ("projects", PROJECTS),
        ("experience", EXPERIENCE),
        ("skills", SKILLS),
        ("education", EDUCATION),
    ]:
        count = await col(collection).count_documents({})
        if count == 0:
            await col(collection).insert_many(data)
            print(f"Seeded {len(data)} {collection}.")
        else:
            print(f"{collection}: {count} documents already present — skipping.")

    # Contact (singleton)
    if await col("contact").count_documents({}) == 0:
        await col("contact").insert_one(CONTACT)
        print("Seeded contact info.")
    else:
        print("Contact info already present — skipping.")

    print("Done.")


if __name__ == "__main__":
    asyncio.run(seed())

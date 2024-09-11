# contains schema of project

# schema for intro
def intro(item) -> dict:
    return {
        "id": str(item["_id"]),
        "intro": item["intro"]
    }


def intro_list(items) -> list:
    return [intro(item) for item in items]


# schema for certificate
def certification(item) -> dict:
    return {
        "id": str(item["_id"]),
        "certificate_id": item["certificate_id"],
        "certificate_title": item["certificate_title"],
        "certificate_name": item["certificate_name"],
        "certificate_provider": item["certificate_provider"],
        "certificate_link": item["certificate_link"]
    }


def certificate_list_entity(items) -> list:
    return [certification(item) for item in items]


# schema for skillset
def skillset(item) -> dict:
    return {
        "id": str(item["_id"]),
        "category": item["category"],
        "skills": item["skills"],
        "icon": item["icon"]
    }


def skillset_list(items) -> list:
    return [skillset(item) for item in items]


# schema for resume
def resume(item) -> dict:
    return {
        "id": str(item["_id"]),
        "link": item["link"]
    }


# schema for education
def education(item) -> dict:
    return {
        "id": str(item["_id"]),
        "course": item["course"],
        "year": item["year"],
        "description": item["description"]
    }


def education_list(items) -> list:
    return [education(item) for item in items]


# schema for work
def work(item) -> dict:
    return {
        "id": str(item["_id"]),
        "duration": item["duration"],
        "company": item["company"],
        "designation": item["designation"],
        "description": item["description"]
    }


def work_list(items) -> list:
    return [work(item) for item in items]


# schema for tech_skill
def tech_skill(item) -> dict:
    return {
        "id": str(item["_id"]),
        "duration": item["duration"],
        "company": item["company"],
        "designation": item["designation"],
        "description": item["description"]
    }


def tech_skill_list(items) -> list:
    return [tech_skill(item) for item in items]


# schema for projects
def projects(item) -> dict:
    return {
        "id": str(item["_id"]),
        "title": item["title"],
        "category": item["category"],
        "technology": item["technology"],
        "link": item["link"],
        "tag": item["tag"],
        "image": item["image"]
    }


def project_list(items) -> list:
    return [projects(item) for item in items]

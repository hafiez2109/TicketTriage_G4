CATEGORY_KEYWORDS = {
    "IT Support": ["wifi", "wi-fi", "internet", "login", "password", "laptop",
                   "computer", "network", "vpn", "email", "printer", "software"],
    "Facilities": ["aircon", "air conditioning", "leak", "broken", "chair",
                   "desk", "lighting", "door", "toilet", "cleaning", "repair"],
    "Course Registration": ["course", "enroll", "enrolment", "enrollment",
                             "registration", "class schedule", "add class", "drop class"],
    "Student Finance": ["fee", "fees", "payment", "invoice", "refund",
                         "scholarship", "billing", "tuition"],
    "Library Services": ["library", "book", "borrow", "return book",
                          "overdue", "journal", "database access"],
}

DEFAULT_CATEGORY = "General Enquiry"


def classify_ticket(title, description):
    text = f"{title} {description}".lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category
    return DEFAULT_CATEGORY
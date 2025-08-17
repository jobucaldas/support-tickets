from flask import Flask, render_template
import json
app = Flask(__name__)

# Definição de categorias
CATEGORY_DICT = {
    "Item Return": ["return", "exchange", "refund", "warranty", "replace"],
    "Account": ["account", "login", "locked", "signup", "register", "password", "reset"],
    "Payment": ["payment", "store credit", "failed payment", "gift card", "charge", "billing", "invoice", "transaction"],
    "Promotion": ["price", "promo", "discount", "coupon", "offer", "sale", "deal"],
    "Package": ["tracking", "package", "delay", "shipment", "delivery", "lost", "damaged", "courier"],
    "Technical Issue": ["bug", "error", "issue", "crash", "slow", "not working", "failure"],
    "Product Inquiry": ["availability", "stock", "size", "color", "spec", "specification", "feature"],
    "Feedback/Complaint": ["complaint", "feedback", "unsatisfied", "poor", "bad service", "suggestion", "review"]
}

def categorize(ticket):
    subject = ticket.get("subject", "").lower()
    main_comment = ticket.get("comment", {}).get("body", "").lower()
    comments = ticket["comments"]

    scores = {cat: 0 for cat in CATEGORY_DICT}

    # Verificar qual categoria se encaixa melhor entre as definidas
    for category, keywords in CATEGORY_DICT.items():
        for kw in keywords:
            if kw in subject:
                scores[category] += 1
            if kw in main_comment:
                scores[category] += 1
            for comment in comments:
                content = comment.get("body", "").lower()
                if kw in comment:
                    scores[category] += 1

    top_category = max(scores, key=scores.get)

    if scores[top_category] > 0:
        return top_category

    return "Other"

@app.route("/categories")
def get_categories():
    # Abre arquivo de tickets
    with open('mock_tickets.json', 'r') as file:
        tickets = json.load(file)["tickets"]

    categories = {}
    for ticket in tickets:
        category = categorize(ticket)
        categories.setdefault(category, []).append(ticket)
    
    return categories

@app.route("/tickets")
def get_tickets():
    # Abre arquivo de tickets
    with open('mock_tickets.json', 'r') as file:
        tickets = json.load(file)["tickets"]
    
    return tickets

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

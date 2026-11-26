from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template, request
import db

app = Flask(__name__)
FROM = ("FROM items i JOIN categories k ON k.id=i.category_id JOIN cities c ON c.id=i.city_id "
        "WHERE i.status='open'")

def ago(dt):
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    s = int((datetime.utcnow() - dt).total_seconds())
    if s < 3600: return f"{max(1, s // 60)} min ago"
    if s < 86400: return f"{s // 3600} hr ago"
    d = s // 86400
    return "Yesterday" if d == 1 else f"{d} days ago"

def where(a, skip=()):
    w, p = "", []
    if a.get("city"): w += " AND c.name=%s"; p.append(a["city"])
    if a.get("category") and "category" not in skip: w += " AND k.name=%s"; p.append(a["category"])
    if a.get("type") in ("lost", "found"): w += " AND i.type=%s"; p.append(a["type"])
    if a.get("days", "").isdigit() and int(a["days"]) > 0:
        w += " AND i.occurred_at>=%s"; p.append(datetime.utcnow() - timedelta(days=int(a["days"])))
    for t in a.get("q", "").split()[:6]:
        w += " AND (i.title LIKE %s OR i.description LIKE %s OR i.area LIKE %s OR k.name LIKE %s)"
        p += ["%" + t + "%"] * 4
    return w, p

@app.context_processor
def ctx():
    return {"cities": db.query("SELECT name FROM cities ORDER BY name")}

@app.get("/")
def home(): return render_template("home.html", page="home")

@app.get("/explore")
def explore(): return render_template("explore.html", page="explore")

def soon(page, title, screen):
    return render_template("soon.html", page=page, title=title, screen=screen)

@app.get("/map")
def map_page(): return soon("map_page", "Map Discovery", 3)
@app.get("/smart-match")
def smart_match(): return soon("smart_match", "Smart Match", 7)
@app.get("/my-refound")
def mine(): return soon("mine", "My RE:FOUND", 6)
@app.get("/report")
def report(): return soon("report", "Report an item", 4)
@app.get("/item/<int:item_id>")
def item(item_id): return soon("item", "Item details", 5)

@app.get("/api/items")
def api_items():
    a = request.args
    w, p = where(a)
    try: limit = max(1, min(int(a.get("limit", 12)), 48)); page = max(1, int(a.get("page", 1)))
    except ValueError: limit, page = 12, 1
    order = "ASC" if a.get("sort") == "old" else "DESC"
    total = db.query("SELECT COUNT(*) AS n " + FROM + w, p)[0]["n"]
    rows = db.query("SELECT i.id,i.type,i.title,i.description,i.area,i.kind,i.color,i.photo,i.occurred_at,"
                    "k.name AS category,c.name AS city " + FROM + w +
                    f" ORDER BY i.occurred_at {order}, i.id DESC LIMIT %s OFFSET %s", p + [limit, (page - 1) * limit])
    for r in rows: r["when"] = ago(r.pop("occurred_at"))
    return jsonify(items=rows, total=total, page=page, has_more=page * limit < total)

@app.get("/api/categories")
def api_categories():
    w, p = where(request.args, skip=("category",))
    rows = db.query("SELECT k.name, COUNT(*) AS count " + FROM + w + " GROUP BY k.name, k.sort_order ORDER BY k.sort_order", p)
    return jsonify([{"name": "All", "count": sum(r["count"] for r in rows)}] + rows)

@app.get("/api/cities")
def api_cities():
    return jsonify(db.query("SELECT name, lat, lng FROM cities ORDER BY name"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

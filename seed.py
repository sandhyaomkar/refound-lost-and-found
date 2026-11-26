"""Creates tables and loads demo data (only if the database is empty)."""
from datetime import datetime, timedelta

CITIES = {"Bengaluru": (12.9716, 77.5946), "Mumbai": (19.076, 72.8777), "Delhi": (28.6139, 77.209),
          "Chennai": (13.0827, 80.2707), "Hyderabad": (17.385, 78.4867), "Pune": (18.5204, 73.8567)}
CATS = ["Bags", "Keys", "Wallets", "Electronics", "Jewellery", "Accessories"]
# city, type, category, title, area, hours_ago, kind, color, description
ITEMS = [
("Bengaluru","found","Bags","Tan leather satchel","Cubbon Park",3,"bag","#8a6a4b","Brass buckle, initials “SR” stitched inside the flap."),
("Bengaluru","lost","Keys","Car keys, Hyundai fob","HSR Layout",30,"keys","#b8643f","Blue lanyard with a small brass bell."),
("Bengaluru","found","Wallets","Black bifold wallet","MG Road metro",5,"wallet","#2f3a33","Contains cards but no cash. Handed to station desk."),
("Bengaluru","lost","Electronics","White earbuds case","Indiranagar",50,"phone","#a9b8a0","Left earbud has a green sticker."),
("Bengaluru","found","Jewellery","Silver ring, flat band","Koramangala",4,"ring","#3d5a49","Engraved inside with a date."),
("Bengaluru","lost","Accessories","Reading glasses, tortoiseshell","Lalbagh",72,"glasses","#d6c7a8","Soft green case with a zip."),
("Bengaluru","found","Accessories","Navy umbrella","Whitefield",28,"umbrella","#5a6e82","Wooden handle, left at a café."),
("Bengaluru","lost","Bags","Blue canvas backpack","Jayanagar",6,"bag","#4a6a8a","Laptop sleeve inside, name tag on strap."),
("Bengaluru","found","Keys","Bike key with yellow tag","Malleshwaram",200,"keys","#a0603f","Single key, rubber tag."),
("Bengaluru","lost","Wallets","Brown leather wallet","Church Street",400,"wallet","#7a5a40","Has a driving licence inside."),
("Bengaluru","found","Electronics","Black Android phone","Majestic bus stand",9,"phone","#444444","Locked, cracked screen protector."),
("Bengaluru","lost","Jewellery","Gold hoop earring","Frazer Town",96,"ring","#b08a4a","Single earring, small pearl drop."),
("Mumbai","found","Wallets","Brown card holder","Bandra",4,"wallet","#7a5a40","Four cards inside."),
("Mumbai","lost","Keys","House keys, three","Dadar",30,"keys","#6e7d68","Red tag marked 4B."),
("Delhi","found","Electronics","Silver phone, cracked case","Connaught Place",5,"phone","#444444","Lock screen shows a dog."),
("Delhi","lost","Jewellery","Gold bracelet","Lajpat Nagar",50,"ring","#b08a4a","Thin chain with a small clasp."),
("Chennai","found","Bags","Green tote","Marina Beach",3,"bag","#3e6b52","Contains a paperback and sunscreen."),
("Hyderabad","lost","Accessories","Grey wool scarf","Banjara Hills",26,"umbrella","#8a8f8a","Hand-knitted with a fringe."),
("Pune","found","Keys","Bike key with tag","Koregaon Park",6,"keys","#a0603f","Yellow rubber tag."),
]

def run(q, ex, now=None):
    """q(sql, params) -> rows; ex(sql, params) -> None."""
    now = now or datetime.utcnow()
    if q("SELECT COUNT(*) AS n FROM items")[0]["n"]:
        return False
    for n, (la, lo) in CITIES.items():
        ex("INSERT INTO cities (name, lat, lng) VALUES (%s,%s,%s)", (n, la, lo))
    for i, n in enumerate(CATS):
        ex("INSERT INTO categories (name, sort_order) VALUES (%s,%s)", (n, i))
    cid = {r["name"]: r["id"] for r in q("SELECT id, name FROM cities")}
    kid = {r["name"]: r["id"] for r in q("SELECT id, name FROM categories")}
    for j, (c, t, k, title, area, h, kind, col, d) in enumerate(ITEMS):
        la, lo = CITIES[c]
        ex("INSERT INTO items (type,title,description,category_id,city_id,area,lat,lng,kind,color,occurred_at,created_at)"
           " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
           (t, title, d, kid[k], cid[c], area, la + ((j * 37) % 100 - 50) / 1500, lo + ((j * 53) % 100 - 50) / 1500,
            kind, col, now - timedelta(hours=h), now))
    return True

if __name__ == "__main__":
    import db
    c = db.conn()
    with c.cursor() as cur:
        for stmt in open("schema.sql").read().split(";"):
            if stmt.strip():
                cur.execute(stmt)
        def q(s, p=()):
            cur.execute(s, p); return list(cur.fetchall())
        print("seeded" if run(q, lambda s, p=(): cur.execute(s, p)) else "database already has data")
    c.close()

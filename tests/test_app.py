"""Route and query tests. Uses SQLite as a stand-in for MySQL (same SQL, %s -> ?)."""
import re, sqlite3, sys, os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import pytest, db, seed

SCHEMA = [
 "CREATE TABLE cities (id INTEGER PRIMARY KEY, name TEXT UNIQUE, lat REAL, lng REAL)",
 "CREATE TABLE categories (id INTEGER PRIMARY KEY, name TEXT UNIQUE, sort_order INT)",
 "CREATE TABLE items (id INTEGER PRIMARY KEY, type TEXT, title TEXT, description TEXT, category_id INT, city_id INT,"
 " area TEXT, lat REAL, lng REAL, kind TEXT, color TEXT, photo TEXT, status TEXT DEFAULT 'open', occurred_at TEXT, created_at TEXT)"]

@pytest.fixture(scope="module")
def client():
    con = sqlite3.connect(":memory:", check_same_thread=False); con.row_factory = sqlite3.Row
    for s in SCHEMA: con.execute(s)
    def q(sql, p=()):
        return [dict(r) for r in con.execute(sql.replace("%s", "?"), [x.isoformat(" ") if isinstance(x, datetime) else x for x in p])]
    ex = lambda sql, p=(): q(sql, p)
    assert seed.run(q, ex) is True and seed.run(q, ex) is False  # seeds once
    db.query = q
    import app
    return app.app.test_client()

def api(c, **kw):
    r = c.get("/api/items", query_string=kw); assert r.status_code == 200; return r.get_json()
def titles(d): return [i["title"] for i in d["items"]]

def test_pages_and_nav(client):
    for u in ["/", "/explore", "/map", "/smart-match", "/my-refound", "/report", "/item/1"]:
        assert client.get(u).status_code == 200
    html = client.get("/").get_data(as_text=True)
    for href in ["/explore", "/map", "/smart-match", "/my-refound", "/report"]: assert f'href="{href}"' in html
    assert "Bengaluru" in html and "Pune" in html  # city menu from DB

def test_city_filter(client):
    assert api(client, city="Bengaluru", limit=48)["total"] == 12
    assert titles(api(client, city="Pune")) == ["Bike key with tag"]

def test_search(client):
    d = api(client, city="Bengaluru", q="wallet"); assert d["total"] == 2 and all("wallet" in t.lower() for t in titles(d))
    assert api(client, city="Bengaluru", q="koramangala ring")["total"] == 1   # multi-term AND
    assert api(client, city="Bengaluru", q="KEYS")["total"] >= 2               # case-insensitive, matches category
    assert api(client, city="Bengaluru", q="' OR 1=1 --")["total"] == 0        # injection-safe

def test_filters(client):
    assert all(i["type"] == "lost" for i in api(client, city="Bengaluru", type="lost", limit=48)["items"])
    assert all(i["category"] == "Bags" for i in api(client, city="Bengaluru", category="Bags")["items"])
    d = api(client, city="Bengaluru", category="Keys", type="found"); assert titles(d) == ["Bike key with yellow tag"]
    assert api(client, city="Bengaluru", days="1")["total"] < api(client, city="Bengaluru")["total"]
    assert api(client, city="Bengaluru", type="bogus")["total"] == 12          # invalid value ignored

def test_sort_and_paging(client):
    new = titles(api(client, city="Bengaluru", limit=48)); old = titles(api(client, city="Bengaluru", limit=48, sort="old"))
    assert new == old[::-1]
    p1 = api(client, city="Bengaluru", limit=5); p3 = api(client, city="Bengaluru", limit=5, page=3)
    assert p1["has_more"] and not p3["has_more"] and len(p3["items"]) == 2
    assert api(client, city="Bengaluru", limit="x")["page"] == 1               # bad numbers don't crash

def test_categories_counts(client):
    r = client.get("/api/categories", query_string={"city": "Bengaluru"}).get_json()
    assert r[0] == {"name": "All", "count": 12} and sum(c["count"] for c in r[1:]) == 12
    r = client.get("/api/categories", query_string={"city": "Bengaluru", "type": "lost"}).get_json()
    assert r[0]["count"] == 6

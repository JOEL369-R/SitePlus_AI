from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime
import sqlite3, uuid

BASE=Path(__file__).resolve().parent
UPLOAD_DIR=BASE/"static"/"uploads"
UPLOAD_DIR.mkdir(parents=True,exist_ok=True)
DB=BASE/"sitepulse.db"
ALLOWED={"png","jpg","jpeg","webp"}
app=Flask(__name__)
app.config["MAX_CONTENT_LENGTH"]=12*1024*1024

def connect():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init_db():
    with connect() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS inspections(
        id INTEGER PRIMARY KEY AUTOINCREMENT, project TEXT, package TEXT,
        reported REAL, estimate REAL, status TEXT, image TEXT, notes TEXT, created_at TEXT)""")

@app.get("/")
def home():
    init_db()
    return render_template("index.html")

@app.get("/api/dashboard")
def dashboard():
    init_db()
    with connect() as c:
        total=c.execute("SELECT COUNT(*) FROM inspections").fetchone()[0]
    return jsonify({"metrics":{"inspections":128+total,"verified":96,"packages":14,"variance":-4}})

@app.post("/api/inspect")
def inspect():
    init_db()
    f=request.files.get("photo")
    if not f or not f.filename: return jsonify(error="Please attach a site photograph."),400
    ext=f.filename.rsplit(".",1)[-1].lower() if "." in f.filename else ""
    if ext not in ALLOWED: return jsonify(error="Use JPG, PNG or WEBP."),400
    try:
        reported=float(request.form.get("reported",65))
        if not 0<=reported<=100: raise ValueError()
    except ValueError: return jsonify(error="Progress must be between 0 and 100."),400
    project=request.form.get("project","Aurelia Heights").strip()[:100]
    package=request.form.get("package","Structural works").strip()[:100]
    notes=request.form.get("notes","").strip()[:500]
    token=uuid.uuid4().hex[:10]
    filename=secure_filename(token+"_"+f.filename)
    f.save(UPLOAD_DIR/filename)
    # Demonstration-only placeholder. It does not inspect image pixels.
    estimate=round(max(0,min(100,reported+(((sum(token.encode())%9)-4)*.7))),1)
    created=datetime.now().isoformat(timespec="minutes")
    with connect() as c:
        cur=c.execute("INSERT INTO inspections(project,package,reported,estimate,status,image,notes,created_at) VALUES(?,?,?,?,?,?,?,?)",
        (project,package,reported,estimate,"Needs review",filename,notes,created))
        rid=cur.lastrowid
    return jsonify(id=rid,project=project,package=package,reported=reported,estimate=estimate,
        status="Needs review",image="/static/uploads/"+filename,created_at=created,
        message="Inspection saved. An engineer must verify this estimate."),201

@app.post("/api/inspections/<int:rid>/verify")
def verify(rid):
    init_db()
    with connect() as c:
        cur=c.execute("UPDATE inspections SET status='Verified' WHERE id=?",(rid,))
        if cur.rowcount==0: return jsonify(error="Inspection not found."),404
    return jsonify(ok=True,status="Verified")

@app.get("/api/inspections")
def inspections():
    init_db()
    with connect() as c:
        rows=c.execute("SELECT * FROM inspections ORDER BY id DESC LIMIT 30").fetchall()
    return jsonify([dict(x) for x in rows])

@app.errorhandler(413)
def too_large(_):
    return jsonify(error="Image too large. Maximum upload size is 12 MB."),413

if __name__=="__main__":
    init_db()
    app.run(debug=True,host="127.0.0.1",port=5000)

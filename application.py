import os
import sys

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


MYSQL_RANDOM_ROOT_PASSWORD = os.environ.get("MYSQL_RANDOM_ROOT_PASSWORD")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")

if (
    MYSQL_RANDOM_ROOT_PASSWORD is None
    or MYSQL_DATABASE is None
    or MYSQL_USER is None
    or MYSQL_PASSWORD is None
):
    print(
        "To run this module,"
        " you must set a each of"
        " `MYSQL_RANDOM_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`,"
        " `MYSQL_PASSWORD`"
        " as environment variables - aborting ..."
    )
    sys.exit(1)


DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost:3307/{MYSQL_DATABASE}"
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)

    issues = db.relationship(
        "Issue",
        backref="parent_project",
        cascade="all, delete, delete-orphan",
    )

    def __repr__(self):
        return f"<Project (id={self.id}, name={self.name})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Issue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)

    project_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "projects.id",
            ondelete="cascade",
        ),
        nullable=False,
    )

    def __repr__(self):
        return f"<Issue (id={self.id})>"


@app.route("/api/health-check", methods=["GET"])
def health_check():
    return {"health-check": "passed"}


@app.route("/api/projects", methods=["POST"])
def create_project():
    name = request.json.get("name")
    if name is None:
        r = jsonify(
            {
                "message": "Your request body must contain a name key",
            }
        )
        r.status = 400
        return r

    p = Project(name=name)
    db.session.add(p)
    db.session.commit()
    r = jsonify(p.to_dict())
    r.status = 201
    return r


@app.route("/api/projects", methods=["GET"])
def get_projects():
    projects = Project.query.all()
    return {
        "projects": [p.to_dict() for p in projects],
    }

from flask import Flask, jsonify, render_template, flash, redirect, Response, session, escape, session
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

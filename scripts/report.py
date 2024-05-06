from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

db = SQLAlchemy()

class Report(db.Model):
    time = db.Column(db.DateTime, primary_key=True)
    accuracy = db.Column(db.Float)
    moisture_level = db.Column(Enum('Acceptable', 'Too Dry', 'Too Moist', name="moisture_levels"))

    def __repr__(self):
        return f'<Report Time={self.time}, Accuracy={self.accuracy}, Moisture Level={self.moisture_level}>'

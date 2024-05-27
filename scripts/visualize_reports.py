from . import constants
from .database import db
from .report import Report
import collections

def get_all_reports():
    try:
        reports = Report.query.all()
        if reports:
            return [{
                "time": report.time,
                "accuracy": report.accuracy,
                "moisture_level": report.moisture_level
            } for report in reports]
        else:
            return []
    except Exception as e:
        return f"An error occurred: {e}"
    
def count_moisture_levels():
    try:
        reports = Report.query.all()
        moisture_levels = [report.moisture_level for report in reports if report.moisture_level is not None]
        return dict(collections.Counter(moisture_levels))
    except Exception as e:
        return f"An error occurred: {e}"

def convert_to_time_series():
    try:
        reports = Report.query.all()
        time_series = [(report.time, report.accuracy) for report in reports if report.time is not None and report.accuracy is not None]
        time_series.sort(key=lambda x: x[0])  # Sort by time
        return time_series
    except Exception as e:
        return f"An error occurred: {e}"
     


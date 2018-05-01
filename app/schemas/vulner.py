from datetime import datetime
from webargs import fields

from app.exceptions import ParamError
from app.engines import db
from app.models import Infomation
from app.schemas import length_validator, OneOf

query_vulners_schema = {
    'start': fields.Int(missing=0),
    'length': fields.Int(missing=15, validate=length_validator),
    'order': fields.Nested({
        'field': fields.Str(missing='posted_time'),
        'direction': fields.Str(missing='desc', validate=OneOf(['asc', 'desc']))
    }, missing={}),
    'filter': fields.Nested({
        'title': fields.Str(),
        'level': fields.Str(),
        'source': fields.Str(),
        'cve_id': fields.Str(),
        'vulner_type': fields.Str(),
        'posted_time': fields.List(fields.Str())
    }, missing={})
}
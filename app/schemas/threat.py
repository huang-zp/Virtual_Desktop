from datetime import datetime
from webargs import fields

from app.exceptions import ParamError
from app.engines import db
from app.models import Infomation
from app.schemas import length_validator, OneOf

query_threat_ip_schema = {
    'start': fields.Int(missing=0),
    'length': fields.Int(missing=15, validate=length_validator),
    'order': fields.Nested({
        'field': fields.Str(missing='crawl_time'),
        'direction': fields.Str(missing='desc', validate=OneOf(['asc', 'desc']))
    }, missing={}),
    'filter': fields.Nested({
        'ip': fields.Str(),
        'source': fields.Str(),
        'asn': fields.Str(),
        'category': fields.Str()
        # 'cnvd_id': fields.Str(),
        # 'affect_product': fields.Str(),
        # 'level': fields.Str(),
        # 'cve_id': fields.Str(),
        # 'validation_info': fields.Str(),
    }, missing={})
}


query_threat_domain_schema = {
    'start': fields.Int(missing=0),
    'length': fields.Int(missing=15, validate=length_validator),
    'order': fields.Nested({
        'field': fields.Str(missing='crawl_time'),
        'direction': fields.Str(missing='desc', validate=OneOf(['asc', 'desc']))
    }, missing={}),
    'filter': fields.Nested({
        'domain': fields.Str(),
        'source': fields.Str()
        # 'cnvd_id': fields.Str(),
        # 'affect_product': fields.Str(),
        # 'level': fields.Str(),
        # 'cve_id': fields.Str(),
        # 'validation_info': fields.Str(),
    }, missing={})
}

query_threat_schema = {
    'field': fields.Str()
}

query_ip_data = {
    'format_time': fields.Str(missing="2018-04-25")
}

query_domain_data = {
    'format_time': fields.Str(missing="2018-04-25")
}
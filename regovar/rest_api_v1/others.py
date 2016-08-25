#!env/python3
# coding: utf-8

from regovar.config import *
from regovar.common import *

from regovar.rest_api_v1.rest_common import *


# 
# Server configuration ============================================================================
#

def api_get_config():

	db_data = {}
	if db_session is None:
		db_data = {"db_error": ERRC_00001}
	else:
		Parameter = Base.classes.parameter
		params = db_session.query(Parameter)
		db_session.execute("SELECT key, value FROM parameter")
		for p in params:
			db_data[p.key] = p.value

	result = { 
		"domain" :          REST_DOMAIN, 
		"version" :         REST_VERSION,
		"range_max" :       REST_RANGE_MAX,
		"range_default" :   REST_RANGE_DEFAULT
	}

	result.update(db_data)

	return jsonify(result)
 

from functools import reduce

from odoo import http, models, fields
from odoo.http import request, send_file
from docxtpl import DocxTemplate
import os
import json

import logging
_logger = logging.getLogger(__name__)

from datetime import datetime

from odoo.addons.base_om.models.util import *

class GEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime):
			return obj.isoformat()
		if isinstance(obj, bytes):
			return str(obj)
		return json.JSONEncoder.default(self, obj)

class DownloadController(http.Controller):
	@http.route('/download/data/<int:id>', type='http', auth='user', website=False)
	def download_sale_bast(self, id, **kw):
		logs([id])
		return 
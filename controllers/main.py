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

class MainController(http.Controller):
	with_product = False
	is_sale_template = True

	@http.route('/form/v1', type='http', auth='user', website=False)
	def v1(self):
		view_id = self.env.ref('base_om.view_import_contact_wizard').id
		r = {
			'type': 'ir.actions.act_window',
			'name': 'Import Contact',
			'res_model': 'res.partner',
			'view_mode': 'form',
			'views': [(view_id, 'form')],
			'target': 'new',
			'context': self.env.context,
		}
		logs(r)
		return r
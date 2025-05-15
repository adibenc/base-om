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
	with_product = False
	is_sale_template = True

	def _download_bast(self, picking_id, sale=None):
		# wip handle if picking_id is int / stock.picking
		picking = request.env['stock.picking'].browse(picking_id)
		if not picking:
			return request.not_found()
		out_dir = "/var/lib/odoo/"

		if not sale:
			sale = picking.move_ids.sale_line_id.order_id

		product_data = []

		# Path to your template file
		file_path = '/home/user/file.docx'
		file_path = "/var/lib/odoo/templates/"
		base_file_path = f"{file_path}/bast-t1.docx"

		doc = DocxTemplate(base_file_path)

		# bdd = BASTData()
		bdd = picking.get_bast_data()
		if self.is_sale_template:
			product_data = picking.get_product_data("empty")
		else:
			product_data = picking.get_product_data()

		bdd.set_products(product_data)
			
		bdd.setup_totalqty()

		context = bdd.__dict__
		doc.render(context)

		# use proper filename
		# nama-desa-kota
		filename = 'bast_filled.docx'
		# addr = sale.partner_id.get_address("fnbast")
		addr = sale.partner_id.bast_fnaddress
		filename = f"base_om-bast-{addr}.docx"
		filled_path = f"{file_path}/{filename}"
		doc.save(filled_path)

		# Read the file content
		try:
			with open(filled_path, 'rb') as f:
				file_content = f.read()
		except FileNotFoundError:
			return request.not_found()

		# Replace placeholders in the file content (if needed)
		# Assuming you have placeholders like {{partner_geo}} in your .docx
		# This part requires a docx library like python-docx to properly edit the docx file.
		# However, if you are only filling out text, you can replace the text using string.replace.
		
		# file_content = file_content.replace(b'{{partner_geo}}', partner_geo.encode())

		# Send the file as a download response
		
		headers = [
			('Content-Type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
			('Content-Disposition', 'attachment; filename="%s"' % filename),
		]

		# return send_file(file_content, filename=filename, headers=headers)
		# Send the file as a response
		return request.make_response(file_content, headers)

	@http.route('/download/sale/bast/<int:sale_id>', type='http', auth='user', website=False)
	def download_sale_bast(self, sale_id, **kw):
		sale = request.env['sale.order'].browse(sale_id)
		picking_id = sale.picking_ids
		# picking_id = sale.picking_id
		
		logs([sale, picking_id])
		# wip set no product total for template if from sale
		return self._download_bast(picking_id.id, sale)

	@http.route('/download/bast/<int:picking_id>', type='http', auth='user', website=False)
	def download_bast(self, picking_id, **kw):
		return self._download_bast(picking_id)
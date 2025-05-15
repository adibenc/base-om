# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.base_om.models.x_model import *

class PartnerGeo(XModel):
	_name = 'base_om.res_partner_geo'
	_description = 'Partner Geo'
	_inherit = ['mail.thread', 'mail.activity.mixin', 'x.attr']
	
	name = fields.Char(string='Pin name',)
	longitude = fields.Float(string='Longitude', required=True)
	latitude = fields.Float(string='Latitude', required=True)

	# wip uniq long lat

	# many2one view name query
	@api.depends('name', 'longitude', 'latitude')
	def _compute_display_name(self):
		for rec in self:
			print(rec)
			if rec.longitude and rec.latitude and rec.name:
				rec.display_name = f"{rec.name} - [{rec.longitude}, {rec.latitude}]"
			else:
				rec.display_name = f"{rec._name},{rec.id}"


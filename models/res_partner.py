# -*- coding: utf-8 -*-
import csv, base64, io, os, subprocess as sub
import openpyxl
from openpyxl.utils import get_column_letter

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.addons.fs_file.fields import FSFile
from odoo.addons.base_om.models.x_model import *
from odoo.addons.base_om.models.util import *

class Partner(XAttrMixin):
	_description = 'Contact'
	_inherit = ['res.partner',]
	
	prov_id = fields.Many2one("base_om.geo_province", string="Prov")
	city_id = fields.Many2one("base_om.geo_city", string="Kota/Kab")
	kec_id = fields.Many2one("base_om.geo_kec", string="Kecamatan")
	village_id = fields.Many2one("base_om.geo_village", string="Desa")

	partner_geo_id = fields.Many2one(
		'base_om.res_partner_geo', string='Geo location',
		index=True,
		help='Selected geo location for a contact')
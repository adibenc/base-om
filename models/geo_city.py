# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.base_om.models.x_model import *


class GeoCity(XModel):
    _name = 'base_om.geo_city'
    _description = 'Geo city'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'x.attr']

    code = fields.Char(string="Code",)
    name = fields.Char(string="Name", required=True, )
    is_kab = fields.Boolean(string="Is kabupaten",)
    province_id = fields.Many2one('base_om.geo_province')
    kec_ids = fields.One2many('base_om.geo_kec', "city_id")
    prefixed = fields.Char(string="Prefixed", compute="_c_px")

    _sql_constraints = [
        ('name', 
        'unique(name)',
        'Nama harus unik!')
    ]

    @api.depends('name')
    def _c_px(self):
        for rec in self:
            if rec.name:
                px = "Kabupaten" if rec.is_kab else "Kota"
                rec.prefixed = f"{px} {rec.name}"
            else:
                rec.prefixed = f"-"

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
    
    @api.model
    def _increment_name(self, name):
        """Increments the name by adding a number or incrementing an existing number."""
        import re
        match = re.search(r'\((\d+)\)$', name)  # Check for existing number at end
        if match:
            number = int(match.group(1)) + 1
            new_name = re.sub(r'\(\d+\)$', f'({number})', name)
        else:
            new_name = f'{name} (1)'  # Add (1) if no number exists
        return new_name

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        copied_count = 0
        original_name = self.name
        new_name = original_name

        while self.env['base_om.geo_city'].search([('name', '=', new_name)]):
            copied_count += 1
            new_name = self._increment_name(original_name)

        default['name'] = new_name
        return super(GeoCity, self).copy(default)

    # return list of geo name with city as root
    def get_children(self, depth=3):
        cities = self.search([
            ('id','!=',0)
        ])
        r = []
        for rec in cities:
            for kec in rec.kec_ids:
                if depth==1:
                    continue
                for vil in kec.vil_ids:
                    for rp in vil.partner_ids:
                        r.append([rec.name, kec.name, vil.name, rp.name])
        return r
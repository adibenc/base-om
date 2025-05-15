# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.base_om.models.x_model import *


class GeoProvince(XModel):
    _name = 'base_om.geo_province'
    _description = 'Geo Provinces'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'x.attr']

    name = fields.Char(string="Name", required=True, )

    _sql_constraints = [
        ('name', 
        'unique(name)',
        'Nama harus unik!')
    ]

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

        while self.env['base_om.geo_province'].search([('name', '=', new_name)]):
            copied_count += 1
            new_name = self._increment_name(original_name)

        default['name'] = new_name
        return super(GeoProvince, self).copy(default)


# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.base_om.models.x_model import *


class GeoVillage(XModel):
    _name = 'base_om.geo_village'
    _description = 'Geo village'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'x.attr']

    name = fields.Char(string="Name", required=True, )
    city_id = fields.Char(string="City", compute="_c_vil_city")
    kec_id = fields.Many2one('base_om.geo_kec')
    partner_ids = fields.One2many('res.partner', 'village_id')
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
                px = "Desa"
                rec.prefixed = f"{px} {rec.name}"
            else:
                rec.prefixed = f"-"

    @api.depends('kec_id')
    def _c_vil_city(self):
        for rec in self:
            print(rec)
            if rec.kec_id:
                pgs = [p.city_id for p in rec.kec_id]
                x = "".join([f"{pg.name}" for pg in pgs if pg.name])
                rec.city_id = x
            else:
                rec.city_id = f"-"
    
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

        while self.env['base_om.geo_village'].search([('name', '=', new_name)]):
            copied_count += 1
            new_name = self._increment_name(original_name)

        default['name'] = new_name
        return super(GeoVillage, self).copy(default)


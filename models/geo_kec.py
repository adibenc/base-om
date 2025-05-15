# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.base_om.models.x_model import *


class GeoKec(XModel):
    _name = 'base_om.geo_kec'
    _description = 'Geo kecamatan'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'x.attr' ]

    code = fields.Char(string="Code",)
    name = fields.Char(string="Name", required=True, )
    province_id = fields.Char(string="Province", compute="_c_kec_prov")
    city_id = fields.Many2one('base_om.geo_city')
    vil_ids = fields.One2many('base_om.geo_village', "kec_id")
    prefixed = fields.Char(string="Prefixed", compute="_c_px")

    _sql_constraints = [
        ('name', 
        'unique(name)',
        'Nama harus unik!')
    ]

    @api.depends('name')
    def _c_px(self):
        for rec in self:
            print(rec)
            if rec.name:
                rec.prefixed = f"Kecamatan {rec.name}"
            else:
                rec.prefixed = f"-"
    
    @api.depends('city_id')
    def _c_kec_prov(self):
        for rec in self:
            print(rec)
            if rec.city_id:
                pgs = [p.province_id for p in rec.city_id]
                x = "".join([f"{pg.name}" for pg in pgs if pg.name])
                rec.province_id = x
            else:
                rec.province_id = f"-"
            
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

        while self.env['base_om.geo_kec'].search([('name', '=', new_name)]):
            copied_count += 1
            new_name = self._increment_name(original_name)

        default['name'] = new_name
        return super(GeoKec, self).copy(default)


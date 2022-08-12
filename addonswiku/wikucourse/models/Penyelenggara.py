from odoo import fields, models, api


class Penyelenggara(models.Model):
    _inherit = 'res.partner'
    _description = 'Description'

    is_tutor = fields.Boolean(
        string='Tutor',
        required=False)
    is_admin = fields.Boolean(
        string='Admin',
        required=False)

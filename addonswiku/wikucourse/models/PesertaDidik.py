from odoo import fields, models, api


class PesertaDidik(models.Model):
    _inherit = 'res.partner'
    _description = 'Form peserta didik wiku course'
    jenis_kursus = fields.Selection(selection=[('pemrograman', 'Pemrograman'), ('bahasa', 'Bahasa'), ('keterampilan', 'Keterampian')],
        string='Jenis_kursus',
        required=False)
    is_peserta = fields.Boolean(
        string='Peserta',
        required=False)



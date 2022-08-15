from odoo import fields, models, api


class SessionPemrograman(models.Model):
    _name = 'wikucourse.sessionpemrograman'
    _description = 'session course wikucourse'

    name = fields.Char(string='Nama')
    nama_kursus = fields.Many2one(
        comodel_name='wikucourse.pemrograman',
        string='Nama Kursus',
        required=False)
    tgl_mulai = fields.Datetime(
        string='Tgl Mulai',
        default=fields.Datetime.now(),
        required=False)
    peserta_ids = fields.One2many(
        comodel_name='res.partner',
        inverse_name='kursus',
        string='Peserta',
        required=False)

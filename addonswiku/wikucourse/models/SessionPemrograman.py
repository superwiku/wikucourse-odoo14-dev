from odoo import fields, models, api


class SessionPemrograman(models.Model):
    _name = 'wikucourse.sessionpemrograman'
    _description = 'Description'
    name = fields.Char(string='Nama')
    nama_kursus = fields.Many2one(
        comodel_name='wikucourse.pemrograman',
        string='Nama Kursus',
        required=False)
    nama_tutor = fields.Many2one(
        comodel_name='res.partner',
        string='Nama_tutor',
        required=False,
        domain=[('function', '=', 'Tutor Pemrograman')])

    tgl_mulai = fields.Datetime(
        string='Tgl Mulai',
        required=False,
        default=fields.Datetime.now())

    peserta_pemrograman_ids = fields.One2many(
        comodel_name='wikucourse.pesertapemrograman',
        inverse_name='session_id',
        string='Peserta',
        required=False)
    jml_siswa = fields.Integer(
        compute='_compute_peserta',
        string='Jml Siswa',
        required=False)

    @api.model
    def _compute_peserta(self):
        for record in self:
            a = self.env['wikucourse.pesertapemrograman'].search([('session_id', '=', record.id)]).mapped('display_name')
            b = len(a)
            record.jml_siswa = b
            print(b)


class PesertaPemrograman(models.Model):
    _name = 'wikucourse.pesertapemrograman'
    _description = 'PesertaPemrograman'

    name = fields.Char()
    peserta_ids = fields.Many2one(
        comodel_name='res.partner',
        string='Peserta Pemrograman',
        required=False,
        domain=[('is_peserta', '=', True) and ('jenis_kursus', '=', 'pemrograman')])
    session_id = fields.Many2one(
        comodel_name='wikucourse.sessionpemrograman',
        string='Session_id',
        required=False)

from odoo import fields, models, api


class CourseCategory(models.Model):
    _name = 'wikucourse.coursecategory'
    _description = 'Nama Kategori Course'

    name = fields.Char(string='Kategori Kursus')
    kapasitas_kelas = fields.Integer(
        string='Kapasitas Kelas',
        required=True)

    level_belajar = fields.Many2one(
        comodel_name='wikucourse.levelcategory',
        string='Level Belajar',
        required=True)

    biaya = fields.Integer(compute='_compute_biaya',
                           string='Biaya',
                           required=False)

    @api.depends('level_belajar')
    def _compute_biaya(self):
        for a in self:
            a.biaya = a.level_belajar.biaya


class Pemrograman(models.Model):
    _inherit = 'wikucourse.coursecategory'
    _name = 'wikucourse.pemrograman'
    _description = 'ini kelas pemrograman'
    startup = fields.Char(
        string='Startup',
        required=False)
    jml_siswa_prog = fields.Integer(
        string='Jml Siswa Pemrograman',
        required=False)
    kapasitas_sisa = fields.Integer(compute='_compute_sisa',
                                    string='Sisa Kapasitas',
                                    required=False)

    @api.depends('jml_siswa_prog')
    def _compute_sisa(self):
        for record in self:
            record.kapasitas_sisa = record.kapasitas_kelas - record.jml_siswa_prog


class Bahasa(models.Model):
    _inherit = 'wikucourse.coursecategory'
    _name = 'wikucourse.bahasa'
    _description = 'ini kelas bahasa'
    negara_pendamping = fields.Char(
        string='Negara Pendamping',
        required=False)
    jml_siswa_bahasa = fields.Integer(
        string='Jml Siswa Bahasa',
        required=False)
    kapasitas_sisa = fields.Integer(string='Sisa Kapasitas',
                                    required=False)



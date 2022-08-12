from odoo import fields, models, api


class CourseCategory(models.Model):
    _name = 'wikucourse.coursecategory'
    _description = 'Nama Kategori Course'

    name = fields.Char(string='Kategori Kursus')
    kapasitas_kelas = fields.Integer(
        string='Kapasitas Kelas',
        required=True)
    sisa_kapasitas = fields.Integer(compute='_compute_sisa',
                                    string='Sisa Kapasitas',
                                    required=False,
                                    store=True)
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

    @api.depends('kapasitas_kelas')
    def _compute_sisa(self):
        for i in self:
            i.sisa_kapasitas = i.kapasitas_kelas


class Pemrograman(models.Model):
    _inherit = 'wikucourse.coursecategory'
    _name = 'wikucourse.pemrograman'
    _description = 'ini kelas pemrograman'
    startup = fields.Char(
        string='Startup',
        required=False)


class Bahasa(models.Model):
    _inherit = 'wikucourse.coursecategory'
    _name = 'wikucourse.bahasa'
    _description = 'ini kelas bahasa'
    negara_pendamping = fields.Char(
        string='Negara Pendamping',
        required=False)

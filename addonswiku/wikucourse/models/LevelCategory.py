from odoo import fields, models, api


class LevelCategory(models.Model):
    _name = 'wikucourse.levelcategory'
    _description = 'Kategori Level Kursus Wiku'

    name = fields.Selection(string='Nama Level',
                            selection=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])
    keterangan = fields.Char(string='Keterangan')
    biaya = fields.Integer(
        string='Biaya',
        required=True)
    course_ids = fields.One2many(
        comodel_name='wikucourse.coursecategory',
        inverse_name='level_belajar',
        string='Daftar Kursus',
        required=False)

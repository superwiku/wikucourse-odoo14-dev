from odoo import fields, api, models
from odoo.modules import get_module_path
import os
import xlsxwriter
import base64
from odoo.exceptions import ValidationError, UserError



class AsmReportSuratJalan(models.TransientModel):
    _name = 'surat.jalan.report.wizard'
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.company.id)
    date_start = fields.Date(required=True, string="Tanggal Awal")
    date_end = fields.Date(required=True, string="Tanggal Akhir")
    is_invoice = fields.Boolean('Ter Invoice')
    is_not_invoice = fields.Boolean('Belum  Ter Invoice')
    is_both = fields.Boolean('Keduanya')
    type = fields.Selection([('dt', "DT"), ('mixer', "Mixer"), ('trailer', "Trailer")], string='Type', required=True)


    @api.onchange('is_invoice')
    def _is_invoice(self):
        for i in self:
            if i.is_invoice == True:
                i.is_not_invoice = False
                i.is_both = False


    @api.onchange('is_not_invoice')
    def _is_not_invoice(self):
        for i in self:
            if i.is_not_invoice == True:
                i.is_invoice = False
                i.is_both = False


    @api.onchange('is_both')
    def _is_both(self):
        for i in self:
            if i.is_both == True:
                i.is_invoice = False
                i.is_not_invoice = False




    def export(self):
        module_path = get_module_path('asm_fleet')
        fpath = module_path + '/generated_files/'
        if not os.path.isdir(fpath):
            os.mkdir(fpath)

        workbook = xlsxwriter.Workbook(module_path + '/generated_files/' + 'laporan-surat-jalan.xlsx')
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({
            'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter'})
        currency_format = workbook.add_format({
            'align': 'center',
            'num_format': '_(* #,##0_);_(* (#,##0);_(* "-"??_);_(@_)',
            'valign': 'vcenter'
        })

        currency_format2 = workbook.add_format({
            'align': 'center',
            'num_format': '_(* #,##0.00_);_(* (#,##0.00);_(* "-"??_);_(@_)',
            'valign': 'vcenter'
        })

        centerformmat = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
        })

        dateformmat = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'num_format': 'd-mmm-yy'
        })

        merge_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': 'true',
            'border': 1
        })
        worksheet.set_column(1, 1, 17)
        worksheet.set_column(2, 2, 30)
        worksheet.set_column(3, 3, 30)
        worksheet.set_column(4, 4, 25)
        worksheet.set_column(6, 6, 15)
        worksheet.set_column(5, 5, 20)
        worksheet.set_column(7, 7, 17)
        worksheet.set_column(8, 8, 17)
        worksheet.set_column(9, 9, 25)
        worksheet.set_column(10, 10, 25)
        worksheet.set_column(11, 11, 25)
        worksheet.set_column(11, 11, 25)

        if self.is_invoice == True and self.type == 'dt':
            worksheet.merge_range('A1:A2', 'No.', merge_format)
            worksheet.merge_range('B1:B2', 'No SJ.', merge_format)
            worksheet.merge_range('C1:C2', 'Kode Mobil.', merge_format)
            worksheet.merge_range('D1:D2', 'Customer', merge_format)
            worksheet.merge_range('E1:E2', 'Tujuan Akhir', merge_format)
            worksheet.merge_range('F1:F2', 'Final Material', merge_format)
            worksheet.merge_range('G1:G2', 'Nilai Invoice', merge_format)
            worksheet.merge_range('H1:H2', 'Tipe Transaksi', merge_format)
            worksheet.merge_range('I1:I2', 'Tanggal SJ', merge_format)
            worksheet.merge_range('J1:J2', 'No. DO', merge_format)
            worksheet.merge_range('K1:K2', 'Quarry', merge_format)
            worksheet.merge_range('L1:L2', 'Tujuan', merge_format)
            worksheet.merge_range('M1:M2', 'Driver', merge_format)
            worksheet.merge_range('N1:N2', 'UJT', merge_format)

            suratjalandata = self.env['asm.surat.jalan'].search([
                ('company_id', '=', self.company_id.id), ('date', '>=', self.date_start),
            ('date', '<=', self.date_end), ('invoice_id', '!=',False)
            ])
            data = []
            # for i in suratjalandata:
            #     datadict = {
            #         'material': i.final_material_id.name,
            #         'customer': i.customer_id.name,
            #         'tj': i.final_plant_id.name,
            #         'harga_po': i.po_id.price,
            #         'plat': i.vehicle_id.name,
            #         'vol_inv': i.volume_netto,
            #         'no_sj': i.name,
            #         'tipe_tran': i.transaction_type,
            #         'date': i.date,
            #         'do': i.do_id.name,
            #         'quarry': i.quarry_id.name,
            #         'plant': i.plant_id.name,
            #         'driver': i.driver_id.name,
            #         'ujt': i.ujt_price_amount,
            #
            #     }
            #     data.append(datadict)

            row = 1
            col = 0
            angka = 0
            for j in range(len(data)):
                angka += 1
                row += 1
                worksheet.write(row, col, angka, centerformmat)
                worksheet.write(row, col + 1, data[j]['no_sj'], centerformmat)
                worksheet.write(row, col + 2, data[j]['plat'], centerformmat)
                worksheet.write(row, col + 3, data[j]['customer'], centerformmat)
                if data[j]['tj'] == False:
                    worksheet.write(row, col + 4, '-', centerformmat)
                else:
                    worksheet.write(row, col + 4, data[j]['tj'], centerformmat)
                if data[j]['material'] == False:
                    worksheet.write(row, col + 5, '-', centerformmat)
                else:
                    worksheet.write(row, col + 5, data[j]['material'], centerformmat)
                worksheet.write(row, col + 6, data[j]['vol_inv'] * data[j]['harga_po'], currency_format)
                worksheet.write(row, col + 7, data[j]['tipe_tran'], centerformmat)
                worksheet.write(row, col + 8, data[j]['date'], dateformmat)
                worksheet.write(row, col + 9, data[j]['do'], centerformmat)
                worksheet.write(row, col + 10, data[j]['quarry'], centerformmat)
                worksheet.write(row, col + 11, data[j]['plant'], centerformmat)
                worksheet.write(row, col + 12, data[j]['driver'], centerformmat)
                worksheet.write(row, col + 13, data[j]['ujt'], centerformmat)

        if self.is_not_invoice ==  True and self.type == 'dt':
            worksheet.merge_range('A1:A2', 'No.', merge_format)
            worksheet.merge_range('B1:B2', 'No SJ.', merge_format)
            worksheet.merge_range('C1:C2', 'Kode Mobil.', merge_format)
            worksheet.merge_range('D1:D2', 'Customer', merge_format)
            worksheet.merge_range('E1:E2', 'Tujuan Akhir', merge_format)
            worksheet.merge_range('F1:F2', 'Final Material', merge_format)
            worksheet.merge_range('G1:G2', 'Nilai Invoice', merge_format)
            worksheet.merge_range('H1:H2', 'Tipe Transaksi', merge_format)
            worksheet.merge_range('I1:I2', 'Tanggal SJ', merge_format)
            worksheet.merge_range('J1:J2', 'No. DO', merge_format)
            worksheet.merge_range('K1:K2', 'Quarry', merge_format)
            worksheet.merge_range('L1:L2', 'Tujuan', merge_format)
            worksheet.merge_range('M1:M2', 'Driver', merge_format)
            worksheet.merge_range('N1:N2', 'UJT', merge_format)
            suratjalandata = self.env['asm.surat.jalan'].search([
                ('company_id', '=', self.company_id.id), ('date', '>=', self.date_start),
                ('date', '<=', self.date_end), ('invoice_id', '=', False)
            ])
            data = []
            for i in suratjalandata:
                datadict = {
                    'material': i.final_material_id.name,
                    'customer': i.customer_id.name,
                    'tj': i.final_plant_id.name,
                    'harga_po': i.po_id.price,
                    'plat': i.vehicle_id.name,
                    'vol_inv': i.volume_netto,
                    'no_sj': i.name,
                    'tipe_tran': i.transaction_type,
                    'date': i.date,
                    'do': i.do_id.name,
                    'quarry': i.quarry_id.name,
                    'plant': i.plant_id.name,
                    'driver': i.driver_id.name,
                    'ujt': i.ujt_price_amount,

                }
                data.append(datadict)

            row = 1
            col = 0
            angka = 0
            for j in range(len(data)):
                angka += 1
                row += 1
                worksheet.write(row, col, angka, centerformmat)
                worksheet.write(row, col + 1, data[j]['no_sj'], centerformmat)
                worksheet.write(row, col + 2, data[j]['plat'], centerformmat)
                worksheet.write(row, col + 3, data[j]['customer'], centerformmat)
                if data[j]['tj'] == False:
                    worksheet.write(row, col + 4, '-', centerformmat)
                else:
                    worksheet.write(row, col + 4, data[j]['tj'], centerformmat)
                if data[j]['material'] == False:
                    worksheet.write(row, col + 5, '-', centerformmat)
                else:
                    worksheet.write(row, col + 5, data[j]['material'], centerformmat)
                worksheet.write(row, col + 6, data[j]['vol_inv'] * data[j]['harga_po'], currency_format)
                worksheet.write(row, col + 7, data[j]['tipe_tran'], centerformmat)
                worksheet.write(row, col + 8, data[j]['date'], dateformmat)
                worksheet.write(row, col + 9, data[j]['do'], centerformmat)
                worksheet.write(row, col + 10, data[j]['quarry'], centerformmat)
                worksheet.write(row, col + 11, data[j]['plant'], centerformmat)
                worksheet.write(row, col + 12, data[j]['driver'], centerformmat)
                worksheet.write(row, col + 13, data[j]['ujt'], centerformmat)


        #bothinvoicedt
        if self.is_both ==  True and self.type == 'dt':
            worksheet.merge_range('A1:A2', 'No.', merge_format)
            worksheet.merge_range('B1:B2', 'No SJ.', merge_format)
            worksheet.merge_range('C1:C2', 'Kode Mobil.', merge_format)
            worksheet.merge_range('D1:D2', 'Customer', merge_format)
            worksheet.merge_range('E1:E2', 'Tujuan Akhir', merge_format)
            worksheet.merge_range('F1:F2', 'Final Material', merge_format)
            worksheet.merge_range('G1:G2', 'Nilai Invoice', merge_format)
            worksheet.merge_range('H1:H2', 'Tipe Transaksi', merge_format)
            worksheet.merge_range('I1:I2', 'Tanggal SJ', merge_format)
            worksheet.merge_range('J1:J2', 'No. DO', merge_format)
            worksheet.merge_range('K1:K2', 'Quarry', merge_format)
            worksheet.merge_range('L1:L2', 'Tujuan', merge_format)
            worksheet.merge_range('M1:M2', 'Driver', merge_format)
            worksheet.merge_range('N1:N2', 'UJT', merge_format)
            suratjalandata = self.env['asm.surat.jalan'].search([
                ('company_id', '=', self.company_id.id), ('date', '>=', self.date_start),
                ('date', '<=', self.date_end)
            ])
            data = []
            for i in suratjalandata:
                datadict = {
                    'material': i.final_material_id.name,
                    'customer': i.customer_id.name,
                    'tj': i.final_plant_id.name,
                    'harga_po': i.po_id.price,
                    'plat': i.vehicle_id.name,
                    'vol_inv': i.volume_netto,
                    'no_sj': i.name,
                    'tipe_tran': i.transaction_type,
                    'date': i.date,
                    'do': i.do_id.name,
                    'quarry': i.quarry_id.name,
                    'plant': i.plant_id.name,
                    'driver': i.driver_id.name,
                    'ujt': i.ujt_price_amount,

                }
                data.append(datadict)

            row = 1
            col = 0
            angka = 0
            for j in range(len(data)):
                angka += 1
                row += 1
                worksheet.write(row, col, angka, centerformmat)
                worksheet.write(row, col + 1, data[j]['no_sj'], centerformmat)
                worksheet.write(row, col + 2, data[j]['plat'], centerformmat)
                worksheet.write(row, col + 3, data[j]['customer'], centerformmat)
                if data[j]['tj'] == False:
                    worksheet.write(row, col + 4, '-', centerformmat)
                else:
                    worksheet.write(row, col + 4, data[j]['tj'], centerformmat)
                if data[j]['material'] == False:
                    worksheet.write(row, col + 5, '-', centerformmat)
                else:
                    worksheet.write(row, col + 5, data[j]['material'], centerformmat)
                worksheet.write(row, col + 6, data[j]['vol_inv'] * data[j]['harga_po'], currency_format)
                worksheet.write(row, col + 7, data[j]['tipe_tran'], centerformmat)
                worksheet.write(row, col + 8, data[j]['date'], dateformmat)
                worksheet.write(row, col + 9, data[j]['do'], centerformmat)
                worksheet.write(row, col + 10, data[j]['quarry'], centerformmat)
                worksheet.write(row, col + 11, data[j]['plant'], centerformmat)
                worksheet.write(row, col + 12, data[j]['driver'], centerformmat)
                worksheet.write(row, col + 13, data[j]['ujt'], centerformmat)


                #//////////


        if self.is_not_invoice == True and self.type == 'mixer':
            suratjalandata = self.env['asm.surat.jalan.mixer'].search([
                ('company_id', '=', self.company_id.id), ('date', '>=', self.date_start),
                ('date', '<=', self.date_end), ('invoice_id', '=', False)
            ])
            worksheet.merge_range('A1:A2', 'No.', merge_format)
            worksheet.merge_range('B1:B2', 'No SJ.', merge_format)
            worksheet.merge_range('C1:C2', 'Kode Mobil.', merge_format)
            worksheet.merge_range('D1:D2', 'Customer', merge_format)
            worksheet.merge_range('E1:E2', 'Tujuan', merge_format)
            worksheet.merge_range('F1:F2', 'Material', merge_format)
            worksheet.merge_range('G1:G2', 'Tipe Transaksi', merge_format)
            worksheet.merge_range('H1:H2', 'Tanggal SJ', merge_format)
            worksheet.merge_range('I1:I2', 'Tujuan', merge_format)
            worksheet.merge_range('J1:J2', 'Driver', merge_format)
            data = []
            for i in suratjalandata:
                datadict = {
                    'material': i.material_id.name,
                    'customer': i.customer_id.name,
                    'tj': i.plant_id.name,
                    'harga_po': i.po_id.price,
                    'plat': i.vehicle_id.name,
                    'no_sj': i.name,
                    'tipe_tran': i.transaction_type,
                    'date': i.date,
                    'plant': i.plant_id.name,
                    'driver': i.driver_id.name,


                }
                data.append(datadict)

            row = 1
            col = 0
            angka = 0
            for j in range(len(data)):
                angka += 1
                row += 1
                worksheet.write(row, col, angka, centerformmat)
                worksheet.write(row, col + 1, data[j]['no_sj'], centerformmat)
                worksheet.write(row, col + 2, data[j]['plat'], centerformmat)
                worksheet.write(row, col + 3, data[j]['customer'], centerformmat)
                if data[j]['tj'] == False:
                    worksheet.write(row, col + 4, '-', centerformmat)
                else:
                    worksheet.write(row, col + 4, data[j]['tj'], centerformmat)
                if data[j]['material'] == False:
                    worksheet.write(row, col + 5, '-', centerformmat)
                else:
                    worksheet.write(row, col + 5, data[j]['material'], centerformmat)
                worksheet.write(row, col + 6, data[j]['tipe_tran'], centerformmat)
                worksheet.write(row, col + 7, data[j]['date'], dateformmat)
                worksheet.write(row, col + 8, data[j]['plant'], centerformmat)
                worksheet.write(row, col + 9, data[j]['driver'], centerformmat)

        if self.is_invoice == True and self.type == 'mixer':
            suratjalandata = self.env['asm.surat.jalan.mixer'].search([
                ('company_id', '=', self.company_id.id), ('date', '>=', self.date_start),
                ('date', '<=', self.date_end), ('invoice_id', '!=', False)
            ])
            worksheet.merge_range('A1:A2', 'No.', merge_format)
            worksheet.merge_range('B1:B2', 'No SJ.', merge_format)
            worksheet.merge_range('C1:C2', 'Kode Mobil.', merge_format)
            worksheet.merge_range('D1:D2', 'Customer', merge_format)
            worksheet.merge_range('E1:E2', 'Tujuan', merge_format)
            worksheet.merge_range('F1:F2', 'Material', merge_format)
            worksheet.merge_range('G1:G2', 'Tipe Transaksi', merge_format)
            worksheet.merge_range('H1:H2', 'Tanggal SJ', merge_format)
            worksheet.merge_range('I1:I2', 'Tujuan', merge_format)
            worksheet.merge_range('J1:J2', 'Driver', merge_format)
            data = []
            for i in suratjalandata:
                datadict = {
                    'material': i.material_id.name,
                    'customer': i.customer_id.name,
                    'tj': i.plant_id.name,
                    'harga_po': i.po_id.price,
                    'plat': i.vehicle_id.name,
                    'no_sj': i.name,
                    'tipe_tran': i.transaction_type,
                    'date': i.date,
                    'plant': i.plant_id.name,
                    'driver': i.driver_id.name,


                }
                data.append(datadict)

            row = 1
            col = 0
            angka = 0
            for j in range(len(data)):
                angka += 1
                row += 1
                worksheet.write(row, col, angka, centerformmat)
                worksheet.write(row, col + 1, data[j]['no_sj'], centerformmat)
                worksheet.write(row, col + 2, data[j]['plat'], centerformmat)
                worksheet.write(row, col + 3, data[j]['customer'], centerformmat)
                if data[j]['tj'] == False:
                    worksheet.write(row, col + 4, '-', centerformmat)
                else:
                    worksheet.write(row, col + 4, data[j]['tj'], centerformmat)
                if data[j]['material'] == False:
                    worksheet.write(row, col + 5, '-', centerformmat)
                else:
                    worksheet.write(row, col + 5, data[j]['material'], centerformmat)
                worksheet.write(row, col + 6, data[j]['tipe_tran'], centerformmat)
                worksheet.write(row, col + 7, data[j]['date'], dateformmat)
                worksheet.write(row, col + 8, data[j]['plant'], centerformmat)
                worksheet.write(row, col + 9, data[j]['driver'], centerformmat)

        #isbothmixer
        if self.is_both == True and self.type == 'mixer':
            suratjalandata = self.env['asm.surat.jalan.mixer'].search([
                ('company_id', '=', self.company_id.id), ('date', '>=', self.date_start),
                ('date', '<=', self.date_end),
            ])
            worksheet.merge_range('A1:A2', 'No.', merge_format)
            worksheet.merge_range('B1:B2', 'No SJ.', merge_format)
            worksheet.merge_range('C1:C2', 'Kode Mobil.', merge_format)
            worksheet.merge_range('D1:D2', 'Customer', merge_format)
            worksheet.merge_range('E1:E2', 'Tujuan', merge_format)
            worksheet.merge_range('F1:F2', 'Material', merge_format)
            worksheet.merge_range('G1:G2', 'Tipe Transaksi', merge_format)
            worksheet.merge_range('H1:H2', 'Tanggal SJ', merge_format)
            worksheet.merge_range('I1:I2', 'Tujuan', merge_format)
            worksheet.merge_range('J1:J2', 'Driver', merge_format)
            data = []
            for i in suratjalandata:
                datadict = {
                    'material': i.material_id.name,
                    'customer': i.customer_id.name,
                    'tj': i.plant_id.name,
                    'harga_po': i.po_id.price,
                    'plat': i.vehicle_id.name,
                    'no_sj': i.name,
                    'tipe_tran': i.transaction_type,
                    'date': i.date,
                    'plant': i.plant_id.name,
                    'driver': i.driver_id.name,


                }
                data.append(datadict)

            row = 1
            col = 0
            angka = 0
            for j in range(len(data)):
                angka += 1
                row += 1
                worksheet.write(row, col, angka, centerformmat)
                worksheet.write(row, col + 1, data[j]['no_sj'], centerformmat)
                worksheet.write(row, col + 2, data[j]['plat'], centerformmat)
                worksheet.write(row, col + 3, data[j]['customer'], centerformmat)
                if data[j]['tj'] == False:
                    worksheet.write(row, col + 4, '-', centerformmat)
                else:
                    worksheet.write(row, col + 4, data[j]['tj'], centerformmat)
                if data[j]['material'] == False:
                    worksheet.write(row, col + 5, '-', centerformmat)
                else:
                    worksheet.write(row, col + 5, data[j]['material'], centerformmat)
                worksheet.write(row, col + 6, data[j]['tipe_tran'], centerformmat)
                worksheet.write(row, col + 7, data[j]['date'], dateformmat)
                worksheet.write(row, col + 8, data[j]['plant'], centerformmat)
                worksheet.write(row, col + 9, data[j]['driver'], centerformmat)

        if self.is_invoice == True and self.type == 'trailer':
            worksheet.merge_range('A1:A2', 'No.', merge_format)
            worksheet.merge_range('B1:B2', 'No SJ.', merge_format)
            worksheet.merge_range('C1:C2', 'Kode Mobil.', merge_format)
            worksheet.merge_range('D1:D2', 'Customer', merge_format)
            worksheet.merge_range('E1:E2', 'Tujuan Akhir', merge_format)
            worksheet.merge_range('F1:F2', 'Final Material', merge_format)
            worksheet.merge_range('G1:G2', 'Tipe Transaksi', merge_format)
            worksheet.merge_range('H1:H2', 'Tanggal SJ', merge_format)
            worksheet.merge_range('I1:I2', 'Tujuan', merge_format)
            worksheet.merge_range('J1:J2', 'Driver', merge_format)
            worksheet.merge_range('K1:K2', 'UJT', merge_format)
            suratjalandata = self.env['asm.surat.jalan.trailer'].search([
                ('company_id', '=', self.company_id.id), ('date', '>=', self.date_start),
                ('date', '<=', self.date_end), ('invoice_id', '!=', False)
            ])
            data = []
            for i in suratjalandata:
                datadict = {
                    'material': i.material_id.name,
                    'customer': i.customer_id.name,
                    'tj': i.plant_id.name,
                    'harga_po': i.po_id.price,
                    'plat': i.vehicle_id.name,
                    'no_sj': i.name,
                    'tipe_tran': i.transaction_type,
                    'date': i.date,
                    'plant': i.plant_id.name,
                    'driver': i.driver_id.name,
                    'ujt': i.ujt_price_amount,

                }
                data.append(datadict)

            row = 1
            col = 0
            angka = 0
            for j in range(len(data)):
                angka += 1
                row += 1
                worksheet.write(row, col, angka, centerformmat)
                worksheet.write(row, col + 1, data[j]['no_sj'], centerformmat)
                worksheet.write(row, col + 2, data[j]['plat'], centerformmat)
                worksheet.write(row, col + 3, data[j]['customer'], centerformmat)
                if data[j]['tj'] == False:
                    worksheet.write(row, col + 4, '-', centerformmat)
                else:
                    worksheet.write(row, col + 4, data[j]['tj'], centerformmat)
                if data[j]['material'] == False:
                    worksheet.write(row, col + 5, '-', centerformmat)
                else:
                    worksheet.write(row, col + 5, data[j]['material'], centerformmat)
                worksheet.write(row, col + 6, data[j]['tipe_tran'], centerformmat)
                worksheet.write(row, col + 7, data[j]['date'], dateformmat)
                worksheet.write(row, col + 8, data[j]['plant'], centerformmat)
                worksheet.write(row, col + 9, data[j]['driver'], centerformmat)
                worksheet.write(row, col + 10, data[j]['ujt'], currency_format2)


        if self.is_not_invoice == True and self.type == 'trailer':
            worksheet.merge_range('A1:A2', 'No.', merge_format)
            worksheet.merge_range('B1:B2', 'No SJ.', merge_format)
            worksheet.merge_range('C1:C2', 'Kode Mobil.', merge_format)
            worksheet.merge_range('D1:D2', 'Customer', merge_format)
            worksheet.merge_range('E1:E2', 'Tujuan Akhir', merge_format)
            worksheet.merge_range('F1:F2', 'Final Material', merge_format)
            worksheet.merge_range('G1:G2', 'Tipe Transaksi', merge_format)
            worksheet.merge_range('H1:H2', 'Tanggal SJ', merge_format)
            worksheet.merge_range('I1:I2', 'Tujuan', merge_format)
            worksheet.merge_range('J1:J2', 'Driver', merge_format)
            worksheet.merge_range('K1:K2', 'UJT', merge_format)
            suratjalandata = self.env['asm.surat.jalan.trailer'].search([
                ('company_id', '=', self.company_id.id), ('date', '>=', self.date_start),
                ('date', '<=', self.date_end), ('invoice_id', '=', False)
            ])
            data = []
            for i in suratjalandata:
                datadict = {
                    'material': i.material_id.name,
                    'customer': i.customer_id.name,
                    'tj': i.plant_id.name,
                    'harga_po': i.po_id.price,
                    'plat': i.vehicle_id.name,
                    'no_sj': i.name,
                    'tipe_tran': i.transaction_type,
                    'date': i.date,
                    'plant': i.plant_id.name,
                    'driver': i.driver_id.name,
                    'ujt': i.ujt_price_amount,

                }
                data.append(datadict)

            row = 1
            col = 0
            angka = 0
            for j in range(len(data)):
                angka += 1
                row += 1
                worksheet.write(row, col, angka, centerformmat)
                worksheet.write(row, col + 1, data[j]['no_sj'], centerformmat)
                worksheet.write(row, col + 2, data[j]['plat'], centerformmat)
                worksheet.write(row, col + 3, data[j]['customer'], centerformmat)
                if data[j]['tj'] == False:
                    worksheet.write(row, col + 4, '-', centerformmat)
                else:
                    worksheet.write(row, col + 4, data[j]['tj'], centerformmat)
                if data[j]['material'] == False:
                    worksheet.write(row, col + 5, '-', centerformmat)
                else:
                    worksheet.write(row, col + 5, data[j]['material'], centerformmat)
                worksheet.write(row, col + 6, data[j]['tipe_tran'], centerformmat)
                worksheet.write(row, col + 7, data[j]['date'], dateformmat)
                worksheet.write(row, col + 8, data[j]['plant'], centerformmat)
                worksheet.write(row, col + 9, data[j]['driver'], centerformmat)
                worksheet.write(row, col + 10, data[j]['ujt'], currency_format2)


        #isbothtrailer
        if self.is_both == True and self.type == 'trailer':
            worksheet.merge_range('A1:A2', 'No.', merge_format)
            worksheet.merge_range('B1:B2', 'No SJ.', merge_format)
            worksheet.merge_range('C1:C2', 'Kode Mobil.', merge_format)
            worksheet.merge_range('D1:D2', 'Customer', merge_format)
            worksheet.merge_range('E1:E2', 'Tujuan Akhir', merge_format)
            worksheet.merge_range('F1:F2', 'Final Material', merge_format)
            worksheet.merge_range('G1:G2', 'Tipe Transaksi', merge_format)
            worksheet.merge_range('H1:H2', 'Tanggal SJ', merge_format)
            worksheet.merge_range('I1:I2', 'Tujuan', merge_format)
            worksheet.merge_range('J1:J2', 'Driver', merge_format)
            worksheet.merge_range('K1:K2', 'UJT', merge_format)
            suratjalandata = self.env['asm.surat.jalan.trailer'].search([
                ('company_id', '=', self.company_id.id), ('date', '>=', self.date_start),
                ('date', '<=', self.date_end)
            ])
            data = []
            for i in suratjalandata:
                datadict = {
                    'material': i.material_id.name,
                    'customer': i.customer_id.name,
                    'tj': i.plant_id.name,
                    'harga_po': i.po_id.price,
                    'plat': i.vehicle_id.name,
                    'no_sj': i.name,
                    'tipe_tran': i.transaction_type,
                    'date': i.date,
                    'plant': i.plant_id.name,
                    'driver': i.driver_id.name,
                    'ujt': i.ujt_price_amount,

                }
                data.append(datadict)

            row = 1
            col = 0
            angka = 0
            for j in range(len(data)):
                angka += 1
                row += 1
                worksheet.write(row, col, angka, centerformmat)
                worksheet.write(row, col + 1, data[j]['no_sj'], centerformmat)
                worksheet.write(row, col + 2, data[j]['plat'], centerformmat)
                worksheet.write(row, col + 3, data[j]['customer'], centerformmat)
                if data[j]['tj'] == False:
                    worksheet.write(row, col + 4, '-', centerformmat)
                else:
                    worksheet.write(row, col + 4, data[j]['tj'], centerformmat)
                if data[j]['material'] == False:
                    worksheet.write(row, col + 5, '-', centerformmat)
                else:
                    worksheet.write(row, col + 5, data[j]['material'], centerformmat)
                worksheet.write(row, col + 6, data[j]['tipe_tran'], centerformmat)
                worksheet.write(row, col + 7, data[j]['date'], dateformmat)
                worksheet.write(row, col + 8, data[j]['plant'], centerformmat)
                worksheet.write(row, col + 9, data[j]['driver'], centerformmat)
                worksheet.write(row, col + 10, data[j]['ujt'], currency_format2)

        if self.is_invoice == True and self.is_not_invoice == True or self.is_invoice == True and self.is_not_invoice == True and self.is_both == True or self.is_invoice == True  and self.is_both == True or self.is_not_invoice == True  and self.is_both == True:
            raise ValidationError("Pilih Hanya Salah Satu Kondisi")

        workbook.close()
        csv_filename = 'laporan-surat-jalan.xlsx'
        with open(module_path + '/generated_files/' + csv_filename, 'rb') as opened_file:
            base64_csv_file = base64.b64encode(opened_file.read())
            attachment = self.env['ir.attachment'].create({
                'name': csv_filename,
                'type': 'binary',
                'datas': base64_csv_file,
            })

            return {
                'type': 'ir.actions.act_url',
                'name': 'products',
                'url': '/web/content/{}?download=true'.format(attachment.id),
            }

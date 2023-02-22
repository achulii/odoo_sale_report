from odoo import models, api

class ProductPricelistReportInherited(models.AbstractModel):
    _inherit = 'report.product.report_pricelist'

    def _get_product_data(self, is_product_tmpl, product, pricelist, quantities):
        data = super()._get_product_data(is_product_tmpl, product, pricelist, quantities)
        product_product = self.env['product.product'].search([('id', '=', data['id'])])
        data['image'] = product_product.image_1920 if product_product.image_1920 else ''
        return data
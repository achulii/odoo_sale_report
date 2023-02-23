from odoo import models, api

class ProductPricelistReportInherited(models.AbstractModel):
    _inherit = 'report.product.report_pricelist'

    def _get_product_data(self, is_product_tmpl, product, pricelist, quantities):
        data = super()._get_product_data(is_product_tmpl, product, pricelist, quantities)
        image = self.env['product.product'].search([('product_tmpl_id', '=', product.id)], limit=1).image_1920
        data['image'] = image
        return data
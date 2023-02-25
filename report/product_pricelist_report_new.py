from odoo import api, models


class ProductPricelistReportNew(models.AbstractModel):
    _name = 'report.product.report_pricelist_new'
    _description = 'Pricelist Report New'

    def _get_report_values(self, docids, data):
        return self._get_report_data(data, 'pdf')

    @api.model
    def get_html(self, data):
        render_values = self._get_report_data(data, 'html')
        return self.env['ir.qweb']._render('new_sales_report.pricelist_report_page_new', render_values)

    def _get_report_data(self, data, report_type='html'):
        quantities = data['quantities'] or [1]

        pricelist_id = data['pricelist_id'] and int(data['pricelist_id']) or None
        pricelist = self.env['product.pricelist'].browse(pricelist_id).exists()
        if not pricelist:
            pricelist = self.env['product.pricelist'].search([], limit=1)

        active_model = data['active_model']
        active_ids = data.get('active_ids') or []
        is_product_tmpl = active_model == 'product.template'
        ProductClass = self.env[active_model]

        products = ProductClass.browse(active_ids) if active_ids else ProductClass.search([('sale_ok', '=', True)])
        products_data = [
            self._get_product_data(is_product_tmpl, product, pricelist, quantities)
            for product in products
        ]

        return {
            'is_html_type': report_type == 'html',
            'is_product_tmpl': is_product_tmpl,
            'is_visible_title': bool(data['is_visible_title']) or False,
            'pricelist': pricelist,
            'products': products_data,
            'quantities': quantities,
        }

    def _get_product_data(self, is_product_tmpl, product, pricelist, quantities):
        data = {
            'id': product.id,
            'name': is_product_tmpl and product.name or product.display_name,
            'price': dict.fromkeys(quantities, 0.0),
            'uom': product.uom_id.name,
        }
        image = self.env['product.product'].search([('product_tmpl_id', '=', product.id)], limit=1).image_1920
        data['image'] = image
        for qty in quantities:
            data['price'][qty] = pricelist._get_product_price(product, qty)

        if is_product_tmpl and product.product_variant_count > 1:
            data['variants'] = [
                self._get_product_data(False, variant, pricelist, quantities)
                for variant in product.product_variant_ids
            ]

        return data

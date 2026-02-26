from odoo import models, api, _
from odoo.exceptions import UserError

class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    def get_package_contents_info(self):
        """ Returns detailed info for the frontend """
        self.ensure_one()
        contents = []
        for quant in self.quant_ids:
            contents.append({
                'product_name': quant.product_id.display_name,
                'quantity': quant.quantity,
                'uom': quant.product_uom_id.name,
                'lot': quant.lot_id.name if quant.lot_id else '',
            })
        
        return {
            'id': self.id,
            'name': self.name,
            'location_name': self.location_id.display_name,
            'contents': contents,
        }

    def _find_location(self, term):
        """ Helper to find location by barcode or name """
        domain = ['|', ('barcode', '=', term), ('name', '=', term)]
        return self.env['stock.location'].search(domain, limit=1)

    def action_move_to_location(self, location_barcode):
        """ Moves this package to a new location """
        self.ensure_one()
        
        # Updated search to use helper
        location = self._find_location(location_barcode)
        
        if not location:
            return {
                'success': False, 
                'message': _("Location '%s' not found (try Barcode or Name).") % location_barcode
            }
        
        if self.location_id == location:
             return {
                'success': False, 
                'message': _("Package is already at %s") % location.display_name
            }

        try:
            self.quant_ids.write({'location_id': location.id})
        except Exception as e:
             return {'success': False, 'message': str(e)}

        return {
            'success': True, 
            'message': _("Package %s moved to %s") % (self.name, location.display_name),
            'new_location': location.display_name
        }

    @api.model
    def action_batch_move_to_location(self, package_ids, location_barcode):
        """ Moves multiple packages to a new location """
        # Updated search to use helper
        location = self.env['stock.quant.package'].browse(package_ids[0])._find_location(location_barcode)
        
        if not location:
            return {
                'success': False, 
                'message': _("Location '%s' not found (try Barcode or Name).") % location_barcode
            }
        
        packages = self.browse(package_ids)
        if not packages:
             return {'success': False, 'message': _("No packages to move.")}

        try:
            quants = packages.mapped('quant_ids')
            quants.write({'location_id': location.id})
        except Exception as e:
            return {'success': False, 'message': str(e)}

        return {
            'success': True, 
            'message': _("%s Packages moved to %s") % (len(packages), location.display_name)
        }

    @api.model
    def action_get_packages_from_location(self, location_barcode):
        """ Returns all packages in a scanned location (Select All) """
        location = self.env['stock.location'].search(['|', ('barcode', '=', location_barcode), ('name', '=', location_barcode)], limit=1)
        
        if not location:
            return {'success': False, 'message': _("Location '%s' not found.") % location_barcode}

        # Find packages currently in this location
        packages = self.search([('location_id', '=', location.id)])
        
        if not packages:
            return {'success': False, 'message': _("No packages found in %s.") % location.display_name}
        
        # Reuse detailed info logic
        results = [pkg.get_package_contents_info() for pkg in packages]
        
        return {
            'success': True,
            'packages': results,
            'message': _("Loaded %s packages from %s.") % (len(results), location.display_name)
        }
import base64
from odoo import api, fields, models

class MrpReportWizard(models.TransientModel):
    _name = 'mrp.report.wizard'
    _description = 'Manufacturing Report Options'

    production_id = fields.Many2one('mrp.production', string='Manufacturing Order', required=True)
    
    action_type = fields.Selection([
        ('print', 'Print'),
        ('download', 'Download'),
        ('email', 'Email'),
        ('label', 'Print Labels (ZPL)')
    ], string='Action', default='print', required=True)

    # --- Helper Methods for Single-Tap Buttons ---
    def action_print_direct(self):
        self.action_type = 'print'
        return self.action_confirm()

    def action_download_direct(self):
        self.action_type = 'download'
        return self.action_confirm()

    def action_label_direct(self):
        self.action_type = 'label'
        return self.action_confirm()

    def action_email_direct(self):
        self.action_type = 'email'
        return self.action_confirm()

    def action_confirm(self):
        self.ensure_one()
        
        # Print / Download trigger standard PDF action
        if self.action_type in ['print', 'download']:
            return self.env.ref('tug_mrp_mods.action_report_mrp_external').report_action(self.production_id)
        
        # ZPL Label Trigger
        elif self.action_type == 'label':
            return self.env.ref('tug_mrp_mods.action_report_mrp_package_zpl').report_action(self.production_id)

        # Email Trigger
        elif self.action_type == 'email':
            # 1. Load the email template
            template_id = self.env.ref('tug_mrp_mods.mail_template_mrp_external').id
            
            # 2. Generate the PDF manually
            report_xml_id = 'tug_mrp_mods.action_report_mrp_external'
            pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(report_xml_id, [self.production_id.id])
            
            # 3. Create the Attachment
            attachment_name = f"MO_{self.production_id.name.replace('/', '_')}.pdf"
            attachment = self.env['ir.attachment'].create({
                'name': attachment_name,
                'type': 'binary',
                'datas': base64.b64encode(pdf_content),
                'res_model': 'mrp.production',
                'res_id': self.production_id.id,
                'mimetype': 'application/pdf',
            })

            # 4. Prepare context
            ctx = {
                'default_model': 'mrp.production',
                'default_res_ids': self.production_id.ids,
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_composition_mode': 'comment',
                'force_email': True,
                'default_attachment_ids': [(6, 0, [attachment.id])] 
            }
            
            # 5. Open the Email Composer
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [(False, 'form')],
                'view_id': False,
                'target': 'new',
                'context': ctx,
            }

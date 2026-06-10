# Xero — Invoicing

Xero is a cloud-based accounting software platform for small and medium businesses. This environment covers the **Invoicing** module.

## Components to Implement

### Invoice List View
- Table of all invoices with columns: invoice number, reference, contact/customer name, date issued, due date, total amount, amount due, status (draft, awaiting approval, awaiting payment, paid, overdue, voided)
- Filter by status, date range, contact
- Search by invoice number, reference, or contact name
- Sort by any column
- Bulk actions (approve, send, delete draft)
- Pagination

### Invoice Creation / Edit Form
- Contact/customer selection (searchable dropdown with option to add new)
- Invoice number (auto-generated or custom)
- Reference field
- Invoice date and due date pickers
- Currency selection
- Line items table:
  - Description, quantity, unit price, tax rate (dropdown), account code, line total
  - Add/remove line items
  - Auto-calculated subtotal, tax, and total
- Notes/memo field
- Attached files section
- Save as draft, approve, or approve and send actions

### Invoice Detail / Preview
- Professional invoice layout preview (printable/PDF style)
- Status badge and payment history
- Action buttons: edit, send, mark as sent, add payment, void, copy to new invoice
- Activity timeline (created, sent, viewed, paid events)

### Record Payment
- Payment date, amount, bank account selection
- Partial payment support
- Payment reference/note
- Exchange rate (for foreign currency)

### Invoice Settings
- Default due date terms (e.g., 7 days, 14 days, 30 days, end of month)
- Default tax rate
- Invoice number sequence configuration
- Invoice branding theme selection
- Default email template for sending invoices
- Late payment penalty/interest settings

### Contacts Integration
- Quick-add contact from invoice form
- Contact details: name, email, phone, billing address, tax ID
- Outstanding balance per contact

### Reporting Summary
- Total invoiced, total outstanding, total overdue amounts
- Aging summary (current, 1-30 days, 31-60 days, 61-90 days, 90+ days)

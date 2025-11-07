# Inventory Management System

A comprehensive inventory management system built with Django, Python, and PostgreSQL for small shops, retail stores, alimentation, and boutiques.

## Features

### Authentication & User Management
- User signup/login with roles (Admin, Manager, Cashier, Stock Manager)
- Role-based access control
- Profile management
- Password reset functionality
- Multi-tenancy support with business registration and management

### Dashboard
- Overview cards (Total Sales, Total Products, Total Customers, Low Stock Alerts)
- Graphs & charts (Sales trends, Top-selling products)
- Daily/Monthly revenue summary
- Recent transactions list
- Branch switching capability

### Product & Inventory Management
- Add/Edit/Delete products
- Product categories & subcategories
- Units of measure (kg, pcs, box)
- Product barcode or SKU system
- Product images
- Stock tracking (available, incoming, outgoing)
- Low stock alerts & reorder levels
- Expiry date tracking (for alimentation)

### Supplier Management
- Add/Edit suppliers
- Track supplier transactions (purchases)
- Supplier contact info & balances
- Purchase order history

### Purchase Management
- Create purchase orders
- Record supplier invoices
- Update stock automatically when items received
- Handle partial deliveries
- Generate purchase receipts

### Sales Management / POS (Point of Sale)
- Add sales manually or through POS interface
- Barcode scanning
- Real-time stock deduction after sale
- Discounts, tax, and promotions
- Invoice & receipt generation (PDF)
- Return/refund management

### Customer Management
- Add/Edit customers
- Track customer purchase history
- Loyalty points or membership system
- Customer balances (credit sales)

### Expense Management
- Record daily/weekly/monthly expenses (rent, electricity, etc.)
- Category-wise expense tracking
- Add notes and attachments

### Financial / Accounting Module
- Cash flow tracking
- Profit & loss report
- Sales vs Purchase comparison
- Payment tracking (cash, credit, mobile money, etc.)
- Supplier and customer balances

### Reports & Analytics
- Sales report (daily, monthly, yearly)
- Stock report (in/out, current level)
- Profit report
- Expense report
- Supplier & customer statements
- Export data to CSV, PDF, or Excel
- Branch performance reports

### Notifications & Alerts
- Low stock or expiry alerts
- Unpaid invoice reminders
- Email or in-app notifications

### Settings
- Business details (name, address, logo with removal option)
- Currency & tax settings
- Barcode format options
- Backup & restore database
- User permissions management
- Branch management for multi-location businesses

### Tenant Account Management
- Business registration and setup
- Update business details (name, contact info, etc.)
- Add or remove branches
- Deactivate business account when needed
- Branch management:
  - Create, edit, or delete branches
  - Assign names, locations, and managers for each branch
  - Monitor branch activities (sales, stock, staff performance)
  - Switch between branches in the dashboard to view specific data
  - Generate combined reports from all branches
- See [TENANT_ACCOUNT_MANAGEMENT.md](TENANT_ACCOUNT_MANAGEMENT.md) for detailed documentation

## Technology Stack

- **Backend**: Django 5.1+
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Authentication**: Django Authentication System
- **File Storage**: Django Media Files
- **Charts**: Chart.js

// ... existing content ...
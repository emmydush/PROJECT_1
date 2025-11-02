# Automatic Calculations in the Inventory Management System

This document summarizes all the automatic calculations implemented in the system that eliminate the need for manual calculations.

## 1. Product-Level Calculations

### Profit Per Unit
- **Location**: Product model (`products/models.py`)
- **Calculation**: `selling_price - cost_price`
- **Usage**: Displayed in product detail and list views

### Profit Margin
- **Location**: Product model (`products/models.py`)
- **Calculation**: `((selling_price - cost_price) / cost_price) * 100`
- **Usage**: Displayed as percentage in product detail view

### Total Profit (Current Stock)
- **Location**: Product model (`products/models.py`)
- **Calculation**: `profit_per_unit * quantity`
- **Usage**: Displayed in product detail view

## 2. Sale-Level Calculations

### Sale Item Profit
- **Location**: SaleItem model (`sales/models.py`)
- **Properties**:
  - `profit_per_unit`: `unit_price - product.cost_price`
  - `total_profit`: `profit_per_unit * quantity`
- **Usage**: Displayed in sale detail view

### Sale Total Profit
- **Location**: Sale model (`sales/models.py`)
- **Calculation**: Sum of all `sale_item.total_profit` for the sale
- **Usage**: Displayed in sales list view

## 3. Report-Level Calculations

### Daily Profit Summary
- **Location**: Profit & Loss report view (`reports/views.py`)
- **Calculation**: For each day in the date range:
  - Revenue: Sum of sales for the day
  - COGS: Sum of cost prices for products sold that day
  - Profit: Revenue - COGS
- **Usage**: Displayed in Profit & Loss report

### Monthly Profit Summary
- **Location**: Profit & Loss report view (`reports/views.py`)
- **Calculation**: For each month in the date range:
  - Revenue: Sum of sales for the month
  - COGS: Sum of cost prices for products sold that month
  - Profit: Revenue - COGS
- **Usage**: Displayed in Profit & Loss report

### Gross Profit
- **Location**: Profit & Loss report view (`reports/views.py`)
- **Calculation**: `sales_revenue - total_cogs`
- **Usage**: Displayed in financial summary

### Net Profit
- **Location**: Profit & Loss report view (`reports/views.py`)
- **Calculation**: `gross_profit - total_expenses`
- **Usage**: Displayed in financial summary

### Profit Margins
- **Location**: Profit & Loss report view (`reports/views.py`)
- **Calculations**:
  - Gross Profit Margin: `(gross_profit / sales_revenue) * 100`
  - Net Profit Margin: `(net_profit / sales_revenue) * 100`
- **Usage**: Displayed as progress bars in Profit & Loss report

## 4. Dashboard Calculations

### Today's Profit
- **Location**: Dashboard view (`dashboard/views.py`)
- **Calculation**: Sum of `sale.total_profit` for today's sales
- **Usage**: Displayed as dashboard statistic

## 5. Automatic Updates

### Stock Quantity Updates
- **Location**: Product model and signals
- **Description**: Automatically updated when sales are made or purchases are received
- **Usage**: Real-time stock level tracking

### Total Price Calculation
- **Location**: SaleItem model (`sales/models.py`)
- **Calculation**: `quantity * unit_price` (calculated on save)
- **Usage**: Ensures accurate total pricing for sale items

## Benefits

With these automatic calculations, users no longer need to:
- Manually calculate profit per product
- Manually calculate total profit for sales
- Manually track daily/monthly profit summaries
- Use external calculators for any financial calculations

All calculations are performed automatically by the system, providing real-time, accurate financial information.
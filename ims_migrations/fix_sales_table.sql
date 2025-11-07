-- Fix sales_sale table to match Django model expectations

-- Add missing columns
ALTER TABLE sales_sale ADD COLUMN IF NOT EXISTS subtotal DECIMAL(10,2) DEFAULT 0;
ALTER TABLE sales_sale ADD COLUMN IF NOT EXISTS tax DECIMAL(10,2) DEFAULT 0;
ALTER TABLE sales_sale ADD COLUMN IF NOT EXISTS discount DECIMAL(10,2) DEFAULT 0;

-- Rename existing columns to match Django model
ALTER TABLE sales_sale RENAME COLUMN discount_amount TO discount;
ALTER TABLE sales_sale RENAME COLUMN tax_amount TO tax;

-- Update default values for renamed columns
ALTER TABLE sales_sale ALTER COLUMN discount SET DEFAULT 0;
ALTER TABLE sales_sale ALTER COLUMN tax SET DEFAULT 0;

-- Copy data from final_amount to total_amount if needed
-- UPDATE sales_sale SET total_amount = final_amount WHERE total_amount = 0 OR total_amount IS NULL;

-- Drop extra columns that aren't in the Django model
-- ALTER TABLE sales_sale DROP COLUMN IF EXISTS sale_number;
-- ALTER TABLE sales_sale DROP COLUMN IF EXISTS final_amount;

-- Note: We're keeping sale_number and final_amount for now to avoid data loss
-- You can manually drop them later if they're truly not needed
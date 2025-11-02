# Stock Update Issue Fix

## Problem Description
When making a sale, the product stock quantity was not being updated correctly. The stock remained at its original value instead of being reduced by the sold quantity.

## Root Cause
The issue was caused by a type mismatch in the Django signal that handles stock updates. The `Product.quantity` field is a `DecimalField`, but the `SaleItem.quantity` was being treated as a `float` when performing arithmetic operations.

Error message:
```
Error updating product stock on sale: unsupported operand type(s) for -=: 'decimal.Decimal' and 'float'
```

## Solution
The fix involved converting the quantity values to the same type before performing arithmetic operations in the signals. Specifically, we used `Decimal(str(instance.quantity))` to ensure type compatibility.

### Files Modified
1. `products/signals.py` - Updated three signal handlers:
   - `update_product_stock_on_sale`
   - `update_product_stock_on_purchase_receive`
   - `restore_product_stock_on_sale_delete`

### Changes Made
```python
# Before (causing the error)
product.quantity -= instance.quantity

# After (fixed)
from decimal import Decimal
product.quantity -= Decimal(str(instance.quantity))
```

## Verification
The fix was verified using test scripts that:
1. Create a test product with known initial stock (100 units)
2. Process a sale for a specific quantity (5 units)
3. Check that the stock is correctly reduced (to 95 units)

Test results:
```
Created product: POS Test Product
Product SKU: POS_TEST_98D8BB5A
Initial stock: 100
Processing sale with 5 items
Sale processing response status: 200
Sale processed successfully! Sale ID: 7
Stock after sale: 95.00
✅ SUCCESS: Stock updated correctly!
```

## Impact
This fix ensures that:
- Product stock levels are correctly updated when sales are made
- Product stock levels are correctly updated when purchases are received
- Product stock levels are correctly restored when sales are deleted
- All arithmetic operations between Decimal and numeric values are handled properly

## Prevention
To prevent similar issues in the future:
1. Always be mindful of data types when performing arithmetic operations
2. Use explicit type conversion when working with different numeric types
3. Test critical functionality with actual data to catch type-related issues
4. Add comprehensive logging to signal handlers for easier debugging
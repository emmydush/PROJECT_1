# Chart Transparent Background Fix

## Overview
This document explains the changes made to fix the issue where chart backgrounds were not becoming transparent as expected.

## Issue
The previous implementation used `backgroundColor: 'transparent'` which should have made the chart backgrounds transparent, but this wasn't working as expected. Users were still seeing background colors on the charts.

## Root Cause
The issue was likely due to:
1. Browser caching of the old JavaScript files
2. Chart.js might not fully respect the 'transparent' value in all cases
3. The approach of using 'transparent' might not be the most effective way to remove backgrounds

## Solution
Changed from:
```javascript
backgroundColor: 'transparent'
```

To:
```javascript
backgroundColor: null
```

This is a more explicit way to tell Chart.js that there should be no background color, which should be more reliable.

## Files Modified
1. `templates/reports/sales.html` - Updated both line and bar charts
2. `templates/reports/profit_loss.html` - Updated line chart
3. `templates/reports/inventory.html` - Updated both bar charts
4. `templates/reports/expenses.html` - Updated line chart (pie chart retained colors)
5. `templates/reports/test_charts.html` - Updated both test charts

## Testing
To test the changes:
1. Clear your browser cache
2. Hard refresh the reports pages
3. Check that charts now appear without background colors

## Exception
The pie chart in `expenses.html` retains its background colors because:
- Pie charts rely on background colors to distinguish between segments
- Without background colors, all segments would appear as lines with no visual distinction
- This follows standard data visualization best practices

## Verification
You can verify the changes by:
1. Checking that the backgroundColor property is now set to null instead of 'transparent'
2. Testing in different browsers to ensure consistency
3. Confirming that the pie chart in expenses report still has its background colors

## Additional Notes
If you're still not seeing the changes:
1. Try opening the reports in an incognito/private browser window
2. Check that your browser is not caching the old files
3. Verify that the server is serving the updated files
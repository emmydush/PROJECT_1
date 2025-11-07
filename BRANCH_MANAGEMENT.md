# Branch Management

This document describes the branch management capabilities of the Inventory Management System.

## Overview

The system provides comprehensive branch management features that allow businesses to:

1. Create, edit, or delete branches
2. Assign names, locations, and managers for each branch
3. Monitor branch activities (sales, stock, staff performance)
4. Switch between branches in the dashboard to view specific data
5. Generate combined reports from all branches

## Technical Implementation

### Models
The Branch model in `superadmin/models.py` contains the following fields:
- `business`: Foreign key to the Business model
- `name`: Branch name
- `address`: Full address of the branch
- `phone`: Phone number
- `email`: Email address
- `manager`: Foreign key to User model (branch manager)
- `is_main`: Boolean flag indicating if this is the main branch
- `is_active`: Boolean flag indicating if the branch is active
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### Forms
The `BranchForm` in `superadmin/forms.py` provides validation and rendering for branch management forms with manager assignment.

### Views
The following views in `superadmin/views.py` handle branch management:
- `branch_list_view`: Displays all branches
- `branch_create_view`: Handles creation of new branches
- `branch_update_view`: Handles updating existing branches
- `branch_delete_view`: Handles deletion of branches
- `branch_reports_view`: Generates combined reports from all branches
- `switch_branch_view`: Allows switching between branches in the dashboard

### URLs
The following URLs in `superadmin/urls.py` provide access to branch management:
- `/branches/`: List all branches
- `/branches/create/`: Create a new branch
- `/branches/<id>/update/`: Update an existing branch
- `/branches/<id>/delete/`: Delete a branch
- `/branches/<id>/switch/`: Switch to a specific branch
- `/branches/reports/`: Generate branch reports

### Templates
The templates in `templates/superadmin/` provide the user interface for branch management:
- `branch_list.html`: Displays the list of branches with manager information
- `branch_form.html`: Form for creating/updating branches
- `branch_confirm_delete.html`: Confirmation page for branch deletion
- `branch_reports.html`: Combined reports from all branches
- `base_tenant.html`: Base template with branch switching dropdown

## Usage

### Creating a Branch
1. Navigate to Settings > Branch Management
2. Click "Add Branch"
3. Enter branch details (name, address, contact information)
4. Select a manager from the available users
5. Mark as main branch if this is the primary location
6. Click "Save Branch"

### Editing a Branch
1. Navigate to Settings > Branch Management
2. Click "Edit" on the branch you want to modify
3. Update branch details as needed
4. Change manager assignment if necessary
5. Click "Save Branch"

### Deleting a Branch
1. Navigate to Settings > Branch Management
2. Click "Delete" on the branch you want to remove
3. Note: The main branch cannot be deleted
4. Confirm deletion

### Assigning Managers
1. When creating or editing a branch, select a user from the "Branch Manager" dropdown
2. Only users associated with the business will appear in the dropdown
3. A branch can have at most one manager assigned

### Switching Between Branches
1. Use the branch dropdown in the dashboard header
2. Select "All Branches" to view combined data
3. Select a specific branch to view only that branch's data
4. The dashboard and all modules will filter to show data for the selected branch

### Generating Reports
1. Navigate to Reports > Branch Reports
2. View overall business metrics across all branches
3. View branch-specific metrics for each location
4. Compare performance across different branches

## Constraints

- Only one branch can be marked as the main branch
- The main branch cannot be deleted
- Only administrators can manage branches
- Only administrators and managers can view branch reports
- All branches must belong to the current business context
- Managers must be users associated with the business
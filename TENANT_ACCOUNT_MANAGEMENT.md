# Tenant Account Management

This document describes the tenant account management capabilities of the Inventory Management System.

## Overview

The system provides comprehensive tenant account management features that allow businesses to:

1. Register their business (sign up to use the IMS)
2. Update business details (name, logo, contact info, etc.)
3. Add or remove branches
4. Deactivate or delete their business account if needed
5. Manage branch-specific features including:
   - Create, edit, or delete branches
   - Assign names, locations, and managers for each branch
   - Monitor branch activities (sales, stock, staff performance)
   - Switch between branches in the dashboard to view specific data
   - Generate combined reports from all branches

## Technical Implementation

### Models
The system uses two main models for business information:

1. **Business** (`superadmin.models.Business`):
   - Core business information (company name, email, type)
   - Ownership and plan information
   - Status tracking (active, suspended, pending)

2. **Branch** (`superadmin.models.Branch`):
   - Branch-specific information (name, address, contact)
   - Manager assignment
   - Relationship to the main Business model
   - Status tracking (active/inactive, main branch)

### Forms
- `BusinessRegistrationForm`: For new business registration
- `BusinessDetailsForm`: For updating business information
- `BranchForm`: For branch management with manager assignment

### Views
- `business_details_view`: Initial business setup after user registration
- `business_update_view`: Update existing business details
- `branch_list_view`: Display all branches
- `branch_create_view`: Create new branches
- `branch_update_view`: Update existing branches
- `branch_delete_view`: Delete branches
- `branch_reports_view`: Generate combined reports from all branches
- `switch_branch_view`: Switch between branches in the dashboard
- `business_deactivate_view`: Deactivate the business

### URLs
Tenant account management is accessible through the following URL patterns:
- `/authentication/business-details/`: Initial business setup
- `/superadmin/business/update/`: Update business details
- `/superadmin/branches/`: Branch management
- `/superadmin/branches/create/`: Create new branch
- `/superadmin/branches/<id>/update/`: Update branch
- `/superadmin/branches/<id>/delete/`: Delete branch
- `/superadmin/branches/<id>/switch/`: Switch to branch
- `/superadmin/branches/reports/`: Branch reports
- `/superadmin/business/deactivate/`: Deactivate business

## Usage Flow

### New User Registration
1. User registers with email and password
2. User is redirected to business details page
3. User enters business information
4. System creates business and associates user as owner

### Branch Management
1. Navigate to Settings > Branch Management
2. View existing branches in the table
3. Click "Add Branch" to create a new branch
4. Assign a manager to the branch
5. Click "Edit" to modify an existing branch
6. Click "Delete" to remove a branch (except the main branch)
7. Use the branch switcher in the dashboard header to view data for specific branches
8. Generate combined reports from all branches in the Reports section

### Business Updates
1. Navigate to Settings > Update Business Details
2. Modify business information as needed
3. Save changes

### Business Deactivation
1. Navigate to Settings > Deactivate Business
2. Confirm deactivation
3. Business will be marked as suspended
# API Test Plan

This document outlines the test plan for the REST API implementation.

## Test Cases

### Authentication
1. Test user registration with valid data
2. Test user registration with invalid data (missing fields, password mismatch)
3. Test user login with valid credentials
4. Test user login with invalid credentials
5. Test user profile retrieval for authenticated users
6. Test user logout

### Products
1. Test listing products (authenticated user)
2. Test listing products (unauthenticated user) - should fail
3. Test creating a product (authenticated user)
4. Test creating a product (unauthenticated user) - should fail
5. Test retrieving product details
6. Test updating a product
7. Test deleting a product
8. Test filtering products by category
9. Test searching products by name/SKU

### Sales
1. Test listing sales
2. Test creating a sale
3. Test retrieving sale details

### Dashboard
1. Test retrieving dashboard statistics

## Implementation Plan

1. Create test database
2. Write unit tests for each endpoint
3. Implement test client for API testing
4. Run tests and verify functionality
5. Fix any issues identified during testing

## Tools
- Django Test Client
- Django REST Framework Test Cases
- Pytest (optional)
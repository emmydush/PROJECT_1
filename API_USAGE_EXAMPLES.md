# API Usage Examples

This document provides examples of how to use the Inventory Management System API.

## Authentication

### Login
```javascript
// JavaScript example
fetch('/api/v1/auth/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'testuser',
        password: 'testpass123'
    })
})
.then(response => response.json())
.then(data => {
    console.log('Token:', data.token);
    console.log('User:', data.user);
});
```

### Get User Profile
```javascript
// JavaScript example
fetch('/api/v1/auth/profile/', {
    method: 'GET',
    headers: {
        'Authorization': 'Token YOUR_TOKEN_HERE',
        'Content-Type': 'application/json',
    }
})
.then(response => response.json())
.then(data => {
    console.log('User profile:', data);
});
```

### Change Password
```javascript
// JavaScript example
const passwordData = {
    old_password: 'currentpassword',
    new_password: 'newpassword123',
    confirm_password: 'newpassword123'
};

fetch('/api/v1/auth/password/change/', {
    method: 'POST',
    headers: {
        'Authorization': 'Token YOUR_TOKEN_HERE',
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(passwordData)
})
.then(response => response.json())
.then(data => {
    console.log('Password change result:', data);
    // Note: You'll need to use the new token returned in the response
});
```

## Products

### List Products
```javascript
// JavaScript example
fetch('/api/v1/products/', {
    method: 'GET',
    headers: {
        'Authorization': 'Token YOUR_TOKEN_HERE',
        'Content-Type': 'application/json',
    }
})
.then(response => response.json())
.then(data => {
    console.log('Products:', data);
});
```

### Search and Filter Products
```javascript
// JavaScript example
fetch('/api/v1/products/?search=laptop&category=1&ordering=name', {
    method: 'GET',
    headers: {
        'Authorization': 'Token YOUR_TOKEN_HERE',
        'Content-Type': 'application/json',
    }
})
.then(response => response.json())
.then(data => {
    console.log('Filtered products:', data);
});
```

### Get Product Details
```javascript
// JavaScript example
fetch('/api/v1/products/1/', {
    method: 'GET',
    headers: {
        'Authorization': 'Token YOUR_TOKEN_HERE',
        'Content-Type': 'application/json',
    }
})
.then(response => response.json())
.then(data => {
    console.log('Product details:', data);
});
```

### Create Product
```javascript
// JavaScript example
const productData = {
    name: 'New Product',
    sku: 'NP001',
    category: 1,
    unit: 1,
    supplier: 1,
    quantity: 50,
    cost_price: 25.00,
    selling_price: 35.00,
    reorder_level: 10
};

fetch('/api/v1/products/create/', {
    method: 'POST',
    headers: {
        'Authorization': 'Token YOUR_TOKEN_HERE',
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(productData)
})
.then(response => response.json())
.then(data => {
    console.log('Created product:', data);
});
```

### Update Product
```javascript
// JavaScript example
const updatedData = {
    name: 'Updated Product Name',
    selling_price: 40.00
};

fetch('/api/v1/products/1/update/', {
    method: 'PUT',
    headers: {
        'Authorization': 'Token YOUR_TOKEN_HERE',
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(updatedData)
})
.then(response => response.json())
.then(data => {
    console.log('Updated product:', data);
});
```

### Delete Product
```javascript
// JavaScript example
fetch('/api/v1/products/1/delete/', {
    method: 'DELETE',
    headers: {
        'Authorization': 'Token YOUR_TOKEN_HERE',
        'Content-Type': 'application/json',
    }
})
.then(response => {
    if (response.status === 204) {
        console.log('Product deleted successfully');
    } else {
        console.log('Error deleting product');
    }
});
```

## Sales

### List Sales
```javascript
// JavaScript example
fetch('/api/v1/sales/', {
    method: 'GET',
    headers: {
        'Authorization': 'Token YOUR_TOKEN_HERE',
        'Content-Type': 'application/json',
    }
})
.then(response => response.json())
.then(data => {
    console.log('Sales:', data);
});
```

### Create Sale
```javascript
// JavaScript example
const saleData = {
    customer: 1,
    payment_method: 'cash',
    discount: 5.00,
    notes: 'Special discount for bulk purchase'
};

fetch('/api/v1/sales/create/', {
    method: 'POST',
    headers: {
        'Authorization': 'Token YOUR_TOKEN_HERE',
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(saleData)
})
.then(response => response.json())
.then(data => {
    console.log('Created sale:', data);
});
```

## Dashboard

### Get Dashboard Statistics
```javascript
// JavaScript example
fetch('/api/v1/dashboard/stats/', {
    method: 'GET',
    headers: {
        'Authorization': 'Token YOUR_TOKEN_HERE',
        'Content-Type': 'application/json',
    }
})
.then(response => response.json())
.then(data => {
    console.log('Dashboard stats:', data);
    console.log('Total products:', data.total_products);
    console.log('Low stock products:', data.low_stock_products);
    console.log('Total sales:', data.total_sales);
    console.log('Today sales:', data.today_sales);
});
```

## Python Example

```python
# Python example using requests library
import requests

# Login
login_data = {
    'username': 'testuser',
    'password': 'testpass123'
}
response = requests.post('http://localhost:8000/api/v1/auth/login/', json=login_data)
token = response.json()['token']

# Set up headers with token
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

# Get products
response = requests.get('http://localhost:8000/api/v1/products/', headers=headers)
products = response.json()
print(f"Found {products['count']} products")

# Create a new product
product_data = {
    'name': 'New Product',
    'sku': 'NP001',
    'category': 1,
    'unit': 1,
    'supplier': 1,
    'quantity': 50,
    'cost_price': 25.00,
    'selling_price': 35.00,
    'reorder_level': 10
}
response = requests.post('http://localhost:8000/api/v1/products/create/', 
                        json=product_data, headers=headers)
new_product = response.json()
print(f"Created product with ID: {new_product['id']}")

# Change password
password_data = {
    'old_password': 'testpass123',
    'new_password': 'newpass456',
    'confirm_password': 'newpass456'
}
response = requests.post('http://localhost:8000/api/v1/auth/password/change/',
                        json=password_data, headers=headers)
new_token = response.json()['token']
print("Password changed successfully")

# Update headers with new token
headers['Authorization'] = f'Token {new_token}'

# Continue using API with new token
```

## Mobile App Integration

For mobile applications, you would typically:
1. Store the authentication token securely
2. Use the token in all API requests
3. Handle pagination for list views
4. Implement offline caching where appropriate
5. Handle network errors gracefully
6. Implement secure password change functionality

## POS Integration

For POS systems, you would typically:
1. Authenticate once at startup
2. Cache product data for quick lookups
3. Process sales transactions in real-time
4. Sync data periodically with the backend
5. Handle barcode scanning integration
6. Allow staff to change their passwords for security
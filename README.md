# E-Commerce API Project

A RESTful API built with Flask for managing an e-commerce system with users, products, and orders.

## 🛠️ Programming Languages & Technologies Used

- **Python 3.9+** - Main programming language
- **Flask** - Web framework for building the REST API
- **SQLAlchemy 2.0** - Object-Relational Mapping (ORM) for database operations
- **Flask-SQLAlchemy** - Flask extension for SQLAlchemy integration
- **Flask-Marshmallow** - Serialization/deserialization library for API responses
- **MySQL** - Database management system
- **mysql-connector-python** - MySQL database connector

## 📋 Project Overview

This project is a comprehensive e-commerce API that provides full CRUD (Create, Read, Update, Delete) operations for managing:

- **Users** - Customer information with address details
- **Products** - Item catalog with pricing
- **Orders** - Purchase records linked to users
- **Order-Product Relationships** - Many-to-many relationships between orders and products

## 🏗️ Database Schema

### Users Table
- ID, Name, Email
- Address fields: Street Number, Street Name, City, State, ZIP Code

### Products Table
- ID, Name, Price

### Orders Table  
- ID, Order Date, User ID (Foreign Key)

### Order-Products Junction Table
- Order ID, Product ID (Many-to-many relationship)

## 🚀 API Endpoints

### User Management
- `POST /users` - Create a new user
- `GET /users` - Get all users
- `GET /users/{id}` - Get specific user
- `PUT /users/{id}` - Update user information
- `DELETE /users/{id}` - Delete a user

### Product Management
- `POST /products` - Create a new product
- `GET /products` - Get all products
- `GET /products/{id}` - Get specific product
- `PUT /products/{id}` - Update product information
- `DELETE /products/{id}` - Delete a product

### Order Management
- `POST /orders` - Create a new order
- `GET /orders` - Get all orders
- `GET /orders/{id}` - Get specific order
- `PUT /orders/{id}` - Update order information
- `DELETE /orders/{id}` - Delete an order

### Relationship Endpoints
- `GET /users/{user_id}/orders` - Get all orders for a specific user
- `GET /orders/{order_id}/products` - Get all products in a specific order
- `POST /orders/{order_id}/products` - Add a product to an order
- `DELETE /orders/{order_id}/products/{product_id}` - Remove a product from an order

## 📦 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- MySQL server
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd apiproject
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**
   - Update the database URI in `app.py`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/database_name'
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://127.0.0.1:5000`

## 📋 Dependencies (requirements.txt)

```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Marshmallow==0.15.0
marshmallow-sqlalchemy==0.29.0
mysql-connector-python==8.1.0
marshmallow==3.19.0
```

## 🧪 Testing with Postman

### Example API Calls

**Create a User:**
```json
POST /users
{
    "name": "John Doe",
    "email": "john@example.com",
    "street_number": 123,
    "street_name": "Main Street",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001"
}
```

**Create a Product:**
```json
POST /products
{
    "name": "iPhone 15 Pro",
    "price": 999.99
}
```

**Create an Order:**
```json
POST /orders
{
    "user_id": 1,
    "order_date": "2025-08-12T10:30:00"
}
```

**Add Product to Order:**
```json
POST /orders/1/products
{
    "product_id": 1
}
```

## 🔧 Key Features

- **RESTful Design** - Follows REST API conventions
- **Data Validation** - Input validation using Marshmallow schemas
- **Error Handling** - Comprehensive error responses with appropriate HTTP status codes
- **Relationship Management** - Handles complex many-to-many relationships
- **JSON Responses** - All responses in JSON format
- **Database Integration** - Uses SQLAlchemy ORM with MySQL backend

## 🏃‍♂️ Development

### Project Structure
```
apiproject/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── venv/              # Virtual environment
└── README.md          # This file
```

### Running in Development Mode
The application runs in debug mode by default, which provides:
- Automatic reloading on code changes
- Detailed error messages
- Debug console access

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🔍 Additional Notes

- The API uses SQLAlchemy 2.0 syntax for database operations
- All endpoints return JSON responses
- The application includes comprehensive error handling
- Database tables are automatically created when the application starts
- The project follows Python best practices and Flask conventions

---

**Author:** Shaney Hoyohoy  
**Created:** August 2025  
**Last Updated:** August 13, 2025

# Frontend API Integration Guide for Signup

This README provides a comprehensive guide for frontend developers on how to interact with the backend API for user registration via the `/signup` endpoint. Below, you will find details on the endpoint, necessary request formats, example requests, and best practices for handling responses.

## API Endpoint

### Signup
- **URL**: `/signup`
- **Method**: `POST`

## Required Headers

Ensure to include the following headers in your request:

- **Content-Type**: `application/json`
- **Authorization**: (if required) Add a bearer token like `Bearer <access_token>`

## JSON Request Body

The JSON object for the signup should include the following fields. Note that all fields are treated as strings and are optional unless specified otherwise:

```json
{
  "email": "string",
  "username": "string",
  "password": "string",
  "country": "string",
  "address": "string",
  "state": "string",
  "city": "string",
  "currency_code": "string",
  "postal_code": "string",
  "firstname": "string",
  "lastname": "string",
  "gender": "string",
  "phone": "string",
  "birthday": "date (YYYY-MM-DD)",
  "profile_picture_id": "string",
  "id_type": "string",
  "id_issue_date": "date (YYYY-MM-DD)",
  "id_expiration_date": "date (YYYY-MM-DD)",
  "id_picture": "string",
  "bvn": "string",
  "next_of_kin_firstname": "string",
  "next_of_kin_lastname": "string",
  "next_of_kin_relationship": "string",
  "next_of_kin_gender": "string",
  "next_of_kin_phone": "string",
  "next_of_kin_email": "string",
  "next_of_kin_address": "string"
}
```

### Example JSON Request for User Signup

```json
{
  "email": "john.doe@example.com",
  "username": "johnny2024",
  "password": "SecurePassword123!",
  "country": "USA",
  "address": "123 Main Street",
  "state": "NY",
  "city": "New York",
  "currency_code": "USD",
  "postal_code": "10001",
  "firstname": "John",
  "lastname": "Doe",
  "gender": "male",
  "phone": "+11234567890",
  "birthday": "1980-12-15",
  "profile_picture_id": "profile12345",
  "id_type": "passport",
  "id_issue_date": "2015-01-01",
  "id_expiration_date": "2025-01-01",
  "id_picture": "idpic12345",
  "bvn": "12345678901",
  "next_of_kin_firstname": "Jane",
  "next_of_kin_lastname": "Doe",
  "next_of_kin_relationship": "sister",
  "next_of_kin_gender": "female",
  "next_of_kin_phone": "+10987654321",
  "next_of_kin_email": "jane.doe@example.com",
  "next_of_kin_address": "124 Main Street, New York, NY 10001"
}
```

## Response Handling

- **Success Response**: A JSON object containing user details or a success message, typically including a status code of 200 or 201.
- **Error Response**: A JSON object that includes details about what went wrong, often with appropriate HTTP status codes like 400 for bad requests or 500 for server errors.

## Best Practices

- **Input Validation**: Always validate inputs on the frontend before submitting to minimize invalid requests.
- **Secure Communication**: Use HTTPS to ensure all data exchanged is secure.
- **Error Handling**: Implement comprehensive error handling to manage API errors effectively and provide meaningful feedback to users.

For more information or assistance, please refer to the API documentation or contact the backend team.
```

This version of the README is specifically tailored for developers needing to implement the user signup functionality, ensuring they have a clear understanding of how to construct requests and handle responses.

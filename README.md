# vasset_global

Below is the content structured as a Markdown README file, suitable for a frontend team needing guidance on interacting with a backend user management API.

```markdown
# Frontend API Integration Guide

This README provides guidelines for frontend developers on how to interact with the backend API for user registration or profile updates. Below you will find details on API endpoints, required data fields, example requests, and best practices for handling API responses.

## API Endpoint Details

The API endpoint you'll interact with can vary based on the functionality:

- Registration: `POST /api/users/register`
- User Updates: `PUT /api/users/{userId}/update`

## HTTP Methods

- Use POST for creating new user registrations.
- Use PUT for updating existing user details.

## Required Headers

Ensure the following headers are included in every request:

- Content-Type: `application/json`
- Authorization: (if required) `Bearer <access_token>`

## JSON Request Body

The JSON object includes various optional fields as detailed below. Note that while fields are optional, certain operations might require specific fields to be filled:

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
  "birthday": "date",
  "profile_picture_id": "string",
  "id_type": "string",
  "id_issue_date": "date",
  "id_expiration_date": "date",
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

### Example JSON Request for User Registration

```json
{
  "email": "user@example.com",
  "username": "newuser2024",
  "password": "securePassword123",
  "country": "USA",
  "address": "1234 Main St",
  "state": "CA",
  "city": "Los Angeles",
  "currency_code": "USD",
  "postal_code": "90001",
  "firstname": "John",
  "lastname": "Doe",
  "gender": "male",
  "phone": "+1234567890",
  "birthday": "1990-01-01",
  "profile_picture_id": "pic12345",
  "id_type": "passport",
  "id_issue_date": "2010-01-01",
  "id_expiration_date": "2030-01-01",
  "id_picture": "idpic12345",
  "bvn": "12345678901",
  "next_of_kin_firstname": "Jane",
  "next_of_kin_lastname": "Doe",
  "next_of_kin_relationship": "sister",
  "next_of_kin_gender": "female",
  "next_of_kin_phone": "+0987654321",
  "next_of_kin_email": "kin@example.com",
  "next_of_kin_address": "1234 Main St, Los Angeles, CA 90001"
}
```

## Response Handling

- Success Response: Typically a JSON object containing either user details or a confirmation of the operation.
- Error Response: A JSON object that provides error details, including status codes and messages for debugging.

## Best Practices

- Input Validation: Validate all inputs on the frontend before sending to the backend to minimize errors and unnecessary server load.
- Secure Communication: Use HTTPS for all API interactions to ensure data integrity and security.
- Robust Error Handling: Implement comprehensive error handling to gracefully handle API errors and provide feedback to the user.

For further details, please refer to the specific API documentation or contact the backend team.
```

This Markdown README file provides all necessary details to enable frontend developers to effectively work with the backend API. It ensures clarity on data requirements, endpoint usage, and response handling.

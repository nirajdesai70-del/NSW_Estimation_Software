> Source: source_snapshot/docs/03_MODULES/12_USER_MANAGEMENT.md
> Bifurcated into: features/employee/_general/12_USER_MANAGEMENT.md
> Module: Employee/Role > General
> Date: 2025-12-17 (IST)

# User Management Module

**Document:** 12_USER_MANAGEMENT.md  
**Version:** 1.0  
**Last Updated:** December 4, 2025

---

## Module Overview

**Purpose:** Manage system users and roles

**Controllers:** 2 (UserController, RoleController)  
**Models:** 2 (User, Role)  
**Tables:** 2 (users, roles)

---

## Users

### User Table Schema

```sql
users
├── id                INT PRIMARY KEY
├── RoleId            INT FK → roles
├── name              VARCHAR(255) NOT NULL
├── email             VARCHAR(255) UNIQUE NOT NULL
├── password          VARCHAR(255) NOT NULL (Hashed)
├── remember_token    VARCHAR(100)
├── email_verified_at TIMESTAMP
├── Status            TINYINT (0=Inactive, 1=Active)
├── created_at        TIMESTAMP
└── updated_at        TIMESTAMP
```

### Password Security

**Hashing:**
```php
// On creation/update
$user->password = Hash::make($request->password);

// On login
if (Hash::check($inputPassword, $user->password)) {
    // Valid!
}
```

**Algorithm:** bcrypt (cost: 10)  
**Security:** Industry standard, cannot be decrypted

---

## Roles

### Role Table Schema

```sql
roles
├── id          INT PRIMARY KEY
├── Name        VARCHAR(255) NOT NULL
├── Details     TEXT (JSON permissions)
├── created_at  TIMESTAMP
└── updated_at  TIMESTAMP
```

### Permission Structure

**Details column (JSON):**
```json
{
    "quotation": true,
    "product": true,
    "client": true,
    "project": true,
    "user": false,
    "price": true
}
```

**Current Status:** Partially implemented (checks disabled in code)

---

## User Management

**Operations:**
- Create user (hash password)
- Edit user
- Change password
- Assign role
- Activate/deactivate (Status)
- Soft delete

**Access Control:**
- Only admins can manage users
- Users can't edit own role
- Password required on creation
- Email must be unique

---

## Summary

**Authentication:** Laravel built-in ✅  
**Authorization:** Role-based (partial) ⚠️  
**Security:** Password hashing ✅  
**User Roles:** Configurable via JSON

---

**End of Document 12 - User Management**

[← Back](11_PRICING_MODULE.md) | [Next: Reports →](13_REPORTS_EXPORTS.md)


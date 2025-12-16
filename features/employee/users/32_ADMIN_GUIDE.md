> Source: source_snapshot/docs/07_USER_GUIDES/32_ADMIN_GUIDE.md
> Bifurcated into: features/employee/users/32_ADMIN_GUIDE.md
> Module: Employee/Role > Users
> Date: 2025-12-17 (IST)

# Administrator Guide

**Document:** 32_ADMIN_GUIDE.md  
**Version:** 1.0  
**Audience:** System Administrators

---

## 📋 Administrator Responsibilities

### Initial Setup

**1. Environment Configuration**
```bash
# Configure .env file
APP_ENV=production
APP_DEBUG=false
APP_URL=http://your-domain.com

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_DATABASE=nepl_db
DB_USERNAME=db_user
DB_PASSWORD=secure_password
```

**2. Database Setup**
```bash
# Run migrations
php artisan migrate

# Seed initial data (if seeders exist)
php artisan db:seed
```

**3. Create First Admin User**
```sql
INSERT INTO users (name, email, password, Status, created_at, updated_at)
VALUES ('Admin', 'admin@nepl.com', '$2y$...hashed...', 1, NOW(), NOW());
```

**4. Set Permissions**
```bash
chmod -R 755 storage bootstrap/cache
chown -R www-data:www-data storage bootstrap/cache
```

---

### User Management

**Add Users:**
1. Login as admin
2. Go to Users → Create User
3. Fill details, assign role
4. Set Status = Active
5. Save

**Reset Password:**
- Use "Forgot Password" feature
- Or manually update in database:
```php
$user->password = Hash::make('newpassword');
$user->save();
```

---

### Backup Strategy

**Database Backup (Daily Recommended):**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u username -p database_name > backup_$DATE.sql
```

**File Backup:**
```bash
tar -czf backup_files_$DATE.tar.gz \
    storage/app/ \
    public/uploads/ \
    .env
```

---

### Monitoring

**Check Logs:**
```bash
tail -f storage/logs/laravel.log
```

**Monitor Disk Space:**
```bash
du -sh storage/
```

**Check Database Size:**
```sql
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
FROM information_schema.TABLES 
WHERE table_schema = 'your_database'
ORDER BY size_mb DESC;
```

---

### Maintenance Tasks

**Weekly:**
- Review logs for errors
- Check database size
- Backup database

**Monthly:**
- Update product prices
- Review user accounts
- Clean old data (if policy exists)
- Update system (composer update)

**Quarterly:**
- Full system backup
- Security review
- Performance optimization
- User training refresher

---

### Troubleshooting

**Problem: Application Error 500**
- Check storage/logs/laravel.log
- Check file permissions
- Check .env configuration

**Problem: Database Connection Failed**
- Verify MySQL running
- Check .env credentials
- Test connection: `mysql -u user -p`

**Problem: PDF Generation Fails**
- Check DomPDF configuration
- Check storage permissions
- Review laravel.log

---

**End of Document 32 - Admin Guide**

[← Back](31_DISCOUNT_LOGIC.md) | [Next: User Guide →](33_USER_GUIDE.md)


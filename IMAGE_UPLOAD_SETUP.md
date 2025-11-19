# Registration Image Upload Implementation

## Overview
The registration form now accepts profile pictures during user signup. Images are validated, previewed, and saved to the database.

## What Was Implemented

### 1. Database Changes
**File**: `accounts/models.py`
- Added `profile_picture` field to Customer model
- Type: `ImageField` with `upload_to='profile_pictures/'`
- Fields: `null=True, blank=True` (optional)
- Also made `address`, `date_of_birth`, and `id_number` optional for registration

### 2. Template Updates
**File**: `templates/register.html`
- Added `enctype="multipart/form-data"` to form tag (required for file uploads)
- Added `id="profilePreview"` to image preview element
- Added `accept="image/*"` to file input for image validation

### 3. Registration View
**File**: `accounts/views.py`
- Created `register_user()` view function
- Handles multipart/form-data POST requests
- Extracts profile picture from `request.FILES`
- Validates all required fields
- Creates User, Customer, and Account records
- Saves profile picture to `media/profile_pictures/`
- Returns JSON response with success/failure status

### 4. URL Configuration
**File**: `core/urls.py`
- Updated register URL to use `accounts.views.register_user`
- Maintains `name='register'` for Django URL tags

### 5. JavaScript Handler
**File**: `assets/src/js/register.js`
- Image preview functionality
- File type validation (JPEG, PNG, GIF, WEBP)
- File size validation (max 5MB)
- AJAX form submission with FormData
- Success/error modal handling
- Automatic redirect to login on success

### 6. Media Configuration
**File**: `credora_bank/settings.py` (already configured)
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**File**: `credora_bank/urls.py` (already configured)
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 7. Dependencies
- Installed **Pillow** library for image handling
- Required for Django's ImageField

## How It Works

### Registration Flow:
1. User clicks "Click to Upload Profile" → file input opens
2. User selects an image → JavaScript validates:
   - File type (must be image)
   - File size (max 5MB)
   - Shows instant preview
3. User fills out form fields
4. User clicks "Submit Form"
5. JavaScript sends FormData via AJAX to `/register/`
6. Django view (`register_user`):
   - Validates all fields
   - Checks email uniqueness
   - Creates User account
   - Creates Customer profile with phone
   - Saves uploaded image to `media/profile_pictures/`
   - Creates Account with unique 10-digit number
7. Returns JSON response:
   - Success: Shows modal → redirects to login
   - Error: Shows error modal

## File Locations

### Uploaded Images
- **Storage**: `media/profile_pictures/`
- **URL**: `/media/profile_pictures/filename.jpg`
- **Access**: Via `customer.profile_picture.url` in templates

### Database Field
```python
customer = Customer.objects.get(user=request.user)
if customer.profile_picture:
    image_url = customer.profile_picture.url
    # Use in template: <img src="{{ customer.profile_picture.url }}" />
```

## Testing the Feature

### 1. Start Development Server
```bash
cd c:\Users\EMINS\Desktop\work\credora\credora_bank
C:/Users/EMINS/Desktop/work/credora/.venv/Scripts/python.exe manage.py runserver
```

### 2. Test Registration
1. Navigate to: `http://127.0.0.1:8000/register/`
2. Click "Click to Upload Profile"
3. Select an image (JPG, PNG, GIF, or WEBP)
4. Verify image preview appears
5. Fill out all required fields:
   - First Name
   - Last Name
   - Account Type
   - Account Currency
   - Email
   - Phone Number
   - Password
   - Confirm Password
   - Accept Terms checkbox
6. Click "Submit Form"
7. Verify success modal appears
8. Check automatic redirect to login page
9. Verify image saved in `media/profile_pictures/`

### 3. Check Uploaded Image
```python
# In Django shell or view:
from accounts.models import Customer
customer = Customer.objects.last()
print(customer.profile_picture.url)  # /media/profile_pictures/filename.jpg
```

## Form Data Structure

### POST Request Format:
```javascript
FormData {
    'firstName': 'John',
    'lastName': 'Doe',
    'accountType': 'Savings',
    'accountCurrency': 'USD $',
    'email': 'john@example.com',
    'phone': '+1234567890',
    'password': 'securepassword',
    'password-2': 'securepassword',
    'terms': 'on',
    'profilePicture': File (binary data)
}
```

### Response Format:
```json
{
    "success": true,
    "message": "Registration successful! Your account number is 1234567890",
    "account_number": "1234567890"
}
```

## Security Features

1. **File Type Validation**: Only image types accepted
2. **File Size Limit**: 5MB maximum
3. **CSRF Protection**: Token included in all requests
4. **Email Uniqueness**: Prevents duplicate accounts
5. **Server-side Validation**: All fields validated in Django view

## Image Validation

### Client-side (JavaScript):
- File type check: `['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']`
- Size limit: 5MB (5 * 1024 * 1024 bytes)

### Server-side (Django):
- ImageField automatically validates image files
- Pillow library handles image processing
- Invalid files rejected with error message

## Displaying Profile Pictures

### In Templates:
```django
{% if customer.profile_picture %}
    <img src="{{ customer.profile_picture.url }}" alt="Profile Picture" />
{% else %}
    <img src="{% static 'src/images/auth/avatar.png' %}" alt="Default Avatar" />
{% endif %}
```

### In Views:
```python
customer = Customer.objects.get(user=request.user)
context = {
    'profile_image': customer.profile_picture.url if customer.profile_picture else None
}
```

## Troubleshooting

### Issue: Images not uploading
- Check `enctype="multipart/form-data"` on form tag
- Verify Pillow is installed: `pip list | grep -i pillow`
- Check media directory permissions

### Issue: Preview not showing
- Verify `profilePreview` ID exists on img tag
- Check browser console for JavaScript errors
- Ensure `register.js` is loaded

### Issue: 404 on image URLs
- Check MEDIA_URL and MEDIA_ROOT in settings
- Verify media URL pattern in urls.py
- Ensure DEBUG=True for development

## Next Steps

### Optional Enhancements:
1. **Image Cropping**: Add client-side cropping tool
2. **Compression**: Auto-compress images before upload
3. **Multiple Formats**: Support more image formats
4. **Thumbnail Generation**: Create thumbnails for listings
5. **CDN Integration**: Use cloud storage (AWS S3, Cloudinary)

## Migration History
- `0001_initial.py`: Created Customer and Account models
- `0002_customer_profile_picture_*.py`: Added profile_picture field and made fields optional

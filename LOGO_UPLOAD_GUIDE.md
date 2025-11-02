# Logo Upload and Display Guide

This guide explains how to properly upload and display business logos in the Inventory Management System.

## Common Issues and Solutions

### 1. Logo Not Displaying After Upload

**Problem**: The logo appears to upload successfully but doesn't show up in the header or settings page.

**Solutions**:
1. Check that the file was properly uploaded to the media directory
2. Verify that the business settings object has the correct file reference
3. Ensure the media files are being served correctly
4. Check browser console for any 404 errors related to the logo URL

### 2. File Permissions Issues

**Problem**: The logo file exists but can't be accessed due to permissions.

**Solutions**:
1. Ensure the web server has read permissions on the media directory
2. Check that the file permissions allow reading by the web server process

## How Logo Upload Works

### 1. Upload Process
1. User selects a logo file in the Business Settings form
2. File is uploaded to `media/business/logo/` directory
3. File reference is saved in the BusinessSettings model
4. File is served through Django's media file handling

### 2. Display Process
1. BusinessSettings context processor provides settings to all templates
2. Base template checks for `business_settings.business_logo`
3. If a logo exists, it's displayed in the navbar brand area
4. If no logo exists, the default icon and business name are shown

## Troubleshooting Steps

### 1. Check if Logo is Uploaded
```bash
# Check database
python manage.py shell -c "from settings.models import BusinessSettings; s = BusinessSettings.objects.get(id=1); print(f'Logo: {s.business_logo}'); print(f'URL: {s.business_logo.url if s.business_logo else None}')"

# Check file system
ls media/business/logo/
```

### 2. Verify Media Settings
Ensure these settings are correct in `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 3. Check Context Processors
Ensure these are in `settings.py` TEMPLATES configuration:
```python
'context_processors': [
    # ... other processors
    'settings.context_processors.business_settings',
    'settings.context_processors.media_settings',
]
```

### 4. Verify URL Configuration
Ensure media files are served in development in `urls.py`:
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Manual Logo Linking

If files exist in the media directory but aren't linked to the business settings, you can manually link them:

```bash
python link_existing_logo.py
```

## Logo Requirements

### Supported Formats
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- WebP (.webp)

### Recommended Specifications
- Size: 200x200 pixels (will be scaled appropriately)
- File size: Under 1MB
- Format: PNG with transparency for best results

## CSS Customization

The logo is styled with the `.navbar-logo` class in `static/css/style.css`. You can adjust:

```css
.navbar-logo {
    height: 30px;           /* Adjust height */
    width: auto;            /* Maintain aspect ratio */
    margin-right: 10px;     /* Space between logo and text */
    object-fit: contain;    /* Ensure full image is visible */
}
```

## Best Practices

1. **Use appropriate file sizes**: Keep logo files under 1MB
2. **Optimize images**: Compress images before upload
3. **Test after upload**: Always verify the logo displays correctly
4. **Backup settings**: Keep backups of business settings
5. **Clear cache**: Clear browser cache if changes don't appear immediately

## Common Error Messages

### "Logo file not found"
- Check that the file exists in the media directory
- Verify file permissions
- Check the file path in the database

### "Permission denied"
- Ensure web server has read access to media directory
- Check file ownership and permissions

### "Media files not served"
- Verify DEBUG is True for development
- Check MEDIA_URL and MEDIA_ROOT settings
- Ensure static file serving is configured correctly
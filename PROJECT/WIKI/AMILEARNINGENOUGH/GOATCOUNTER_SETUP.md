# GoatCounter Analytics Integration

This MkDocs site is now integrated with GoatCounter for privacy-friendly analytics tracking.

## What's Been Set Up

### 1. Tracking Script
- The GoatCounter tracking script is automatically loaded on all pages
- Your tracking code: `https://learningresource.goatcounter.com/count`

### 2. Analytics Display
- **Homepage**: Shows a total site view counter and link to public dashboard
- **All Pages**: Each page displays an analytics widget at the bottom with:
  - Link to view detailed dashboard
  - Expandable section showing page-specific view counter (when available)

### 3. Configuration
The GoatCounter integration is configured in `mkdocs.yml`:

```yaml
extra:
  goatcounter:
    site: learningresource
    domain: learningresource.goatcounter.com
```

## How to Use

### View Analytics Dashboard
1. Go to [https://learningresource.goatcounter.com/](https://learningresource.goatcounter.com/)
2. View real-time statistics including:
   - Page views per page
   - Total site views
   - Visitor locations (anonymized)
   - Browser and device statistics
   - Referrer information

### Enable Public Statistics Display (Optional)
If you want to show individual page view counters publicly:

1. Go to your GoatCounter settings
2. Enable "Public statistics"
3. The page-specific counters will automatically start working

### Customize Analytics Display
- Edit `docs/overrides/main.html` to modify the analytics widget
- Edit `docs/overrides/stylesheets/goatcounter.css` to change styling
- Modify `docs/index.md` to adjust the homepage analytics section

## Files Created/Modified

```
mkdocs.yml                                  # Added GoatCounter config
docs/overrides/main.html                    # Custom template with analytics
docs/overrides/stylesheets/goatcounter.css  # Analytics styling
docs/index.md                               # Added analytics section
```

## Privacy Features

GoatCounter is designed with privacy in mind:
- ✅ No cookies
- ✅ No tracking across sites
- ✅ No personal data collection
- ✅ Respects Do Not Track
- ✅ GDPR compliant
- ✅ Open source

## Testing

To test the integration:
1. Build and serve your site: `mkdocs serve`
2. Visit different pages
3. Check the GoatCounter dashboard to see if visits are being tracked
4. Verify the analytics widgets appear on each page

## Troubleshooting

**Visits not being tracked?**
- Check that the GoatCounter script loads without errors in browser dev tools
- Verify your GoatCounter site URL is correct
- Ensure JavaScript is enabled

**Analytics widgets not appearing?**
- Check that the custom theme directory is being used
- Verify the `custom_dir: overrides` setting in mkdocs.yml
- Make sure the CSS file path is correct

**Public counters not working?**
- Enable public statistics in your GoatCounter settings
- Wait a few minutes for the setting to take effect 
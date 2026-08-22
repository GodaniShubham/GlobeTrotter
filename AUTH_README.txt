GlobeTrotter auth UI update

Included:
- Refined split login/signup UI
- Odoo logo + GlobeTrotter stacked brand treatment
- Password show/hide control on sign-in and sign-up
- New templates/pages/forgot_password.html
- Forgot password demo behavior

Backend note:
The forgot-password screen is frontend-only in this package. Add a Django URL/view for /forgot-password/ that renders:
    templates/pages/forgot_password.html
No existing authentication model/view was changed here.

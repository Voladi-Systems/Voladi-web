JAZZMIN_SETTINGS = {
    "site_title": "Povulo - Administrator",
    "site_header": "Povulo - Administrator",
    "site_brand": "Povulo",
    "site_icon": "django/images/Logo_Povulo-lights_Cropped.png",
    "login_logo": "django/images/Logo_Povulo-lights.png",
    "site_logo": "django/images/Logo_Povulo-lights_Cropped.png",
    "welcome_sign": "Welcome to the Povulo - Administrator",
    "user_avatar": "fa user-profile fa-user-circle",
    "topmenu_links": [
        {"name": "Povulo - Administrator", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "users.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "admin.LogEntry": "fas fa-file",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-arrow-circle-right",
    "related_modal_active": False,
    "custom_css": "django/css/main.css",
    "show_ui_builder": False,
    "changeform_format": "single",

}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-navy",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": False,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": False,
    "theme": "litera",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False
}

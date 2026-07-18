from django.apps import AppConfig


class FeatureAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # After copying to apps/<feature_name>/, set:
    # name = "apps.<feature_name>"
    name = "apps.REPLACE_ME"

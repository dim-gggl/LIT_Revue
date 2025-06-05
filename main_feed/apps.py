from django.apps import AppConfig


"""
The Class MainFeedConfig permits to configure the way primary keys
are automatically given to instances of our models if not explicitly
implemented inside the constructor
"""
class MainFeedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_feed'

class RouteMainApp:
    def init_app(self, app):
        from app.resources.main_app_resource import main_app_bp

        app.register_blueprint(main_app_bp, url_prefix="/api/v1")

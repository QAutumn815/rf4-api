from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib        import admin
from django.urls           import path, include

from apps.core.views import IndexView, BrowseRecordsView, BrowseRatingsView, BrowseWinnersView

urlpatterns = [
    # Landing page
    path("", IndexView.as_view(), name="index"),
    # API
    path("", include("apps.api.urls")),
    # Frontend browse pages
    path(
        "browse/records/<str:record_type>/<str:region>/<str:category>/",
        BrowseRecordsView.as_view(),
        name="browse_records",
    ),
    path(
        "browse/ratings/<str:region>/",
        BrowseRatingsView.as_view(),
        name="browse_ratings",
    ),
    path(
        "browse/winners/<str:region>/<str:category>/",
        BrowseWinnersView.as_view(),
        name="browse_winners",
    ),
    # Stuff
    path("admin/", admin.site.urls),
    # Open API
    path("docs/",         SpectacularAPIView.as_view(), name="schema"),
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("docs/redoc/",   SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

from django.views.generic import TemplateView, ListView

from apps.core.models import AbsoluteRecord, WeeklyRecord, Rating, Winner


REGIONS    = ["gl", "ru", "de", "us", "fr", "cn", "pl", "kr", "jp", "en"]
CATEGORIES = ["records", "ultralight", "telestick"]


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["endpoints"] = [
            {"method": "POST", "path": "/v1/parse/",
             "description": "异步触发数据抓取"},
            {"method": "DELETE", "path": "/v1/clear/",
             "description": "清空指定表的数据"},
            {"method": "GET", "path": "/v1/records/abs/{region}/{category}/",
             "description": "获取绝对鱼获纪录（按区域和分类）"},
            {"method": "GET", "path": "/v1/records/wk/{region}/{category}/",
             "description": "获取每周鱼获纪录（按区域和分类）"},
            {"method": "GET", "path": "/v1/ratings/{region}/",
             "description": "获取玩家评级（按区域）"},
            {"method": "GET", "path": "/v1/winners/{region}/{category}/",
             "description": "获取比赛优胜者（按区域和分类）"},
        ]
        context["regions"] = REGIONS
        context["categories"] = CATEGORIES
        context["stats"] = {
            "absolute_records": AbsoluteRecord.objects.count(),
            "weekly_records": WeeklyRecord.objects.count(),
            "ratings": Rating.objects.count(),
            "winners": Winner.objects.count(),
        }
        return context


# ---- Browse Views (frontend) ----


class BrowseRecordsView(ListView):
    template_name = "core/browse_records.html"
    paginate_by = 25
    allow_empty = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._record_type = None   # "abs" or "wk"
        self._region = None
        self._category = None
        self._model = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self._record_type = kwargs.get("record_type", "abs")
        # Support GET param overrides so dropdown selectors actually work
        self._region = request.GET.get("region") or kwargs.get("region", "gl")
        self._category = request.GET.get("category") or kwargs.get("category", "records")
        self._model = WeeklyRecord if self._record_type == "wk" else AbsoluteRecord

    def get_queryset(self):
        qs = self._model.objects.all()
        if self._region and self._region != "all":
            qs = qs.filter(region=self._region)
        if self._category and self._category != "all":
            qs = qs.filter(category=self._category)
        # Apply GET-parameter filters
        params = self.request.GET
        fish = params.get("fish", "").strip()
        player = params.get("player", "").strip()
        try:
            min_weight = float(params.get("min_weight", ""))
        except (ValueError, TypeError):
            min_weight = None
        try:
            max_weight = float(params.get("max_weight", ""))
        except (ValueError, TypeError):
            max_weight = None
        date_after = params.get("date_after", "").strip()
        date_before = params.get("date_before", "").strip()

        if fish:
            qs = qs.filter(fish__icontains=fish)
        if player:
            qs = qs.filter(player__icontains=player)
        if min_weight is not None:
            qs = qs.filter(weight__gte=min_weight)
        if max_weight is not None:
            qs = qs.filter(weight__lte=max_weight)
        if date_after:
            qs = qs.filter(date__gte=date_after)
        if date_before:
            qs = qs.filter(date__lte=date_before)

        return qs.order_by("-weight")  # heaviest first

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = "绝对纪录" if self._record_type == "abs" else "每周纪录"
        context.update({
            "title": title,
            "record_type": self._record_type,
            "region": self._region,
            "category": self._category,
            "all_regions": REGIONS,
            "all_categories": CATEGORIES,
        })
        return context


class BrowseRatingsView(ListView):
    template_name = "core/browse_ratings.html"
    paginate_by = 50
    allow_empty = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._region = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self._region = request.GET.get("region") or kwargs.get("region", "gl")

    def get_queryset(self):
        qs = Rating.objects.all()
        if self._region and self._region != "all":
            qs = qs.filter(region=self._region)
        player = self.request.GET.get("player", "").strip()
        if player:
            qs = qs.filter(player__icontains=player)
        return qs.order_by("position")  # lowest position first

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "region": self._region,
            "all_regions": REGIONS,
        })
        return context


class BrowseWinnersView(ListView):
    template_name = "core/browse_winners.html"
    paginate_by = 50
    allow_empty = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._region = None
        self._category = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self._region = request.GET.get("region") or kwargs.get("region", "gl")
        self._category = request.GET.get("category") or kwargs.get("category", "records")

    def get_queryset(self):
        qs = Winner.objects.all()
        if self._region and self._region != "all":
            qs = qs.filter(region=self._region)
        if self._category and self._category != "all":
            qs = qs.filter(category=self._category)
        player = self.request.GET.get("player", "").strip()
        if player:
            qs = qs.filter(player__icontains=player)
        return qs.order_by("position")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "region": self._region,
            "category": self._category,
            "all_regions": REGIONS,
            "all_categories": CATEGORIES,
        })
        return context

from django.db import models


class Record(models.Model):
    weight     = models.DecimalField(verbose_name = "鱼重", max_digits = 16, decimal_places = 3)
    fish       = models.CharField(verbose_name = "鱼种", max_length = 64)
    fish_image = models.URLField(verbose_name = "鱼类图片", max_length = 512, blank = True, default = "")
    location   = models.CharField(verbose_name = "钓点", max_length = 64)
    bait       = models.CharField(verbose_name = "鱼饵", max_length = 128)
    player     = models.CharField(verbose_name = "玩家", max_length = 256)
    date       = models.DateField(verbose_name = "捕获日期")
    region     = models.CharField(verbose_name = "区域", max_length = 4)
    category   = models.CharField(verbose_name = "分类", max_length = 16)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return (
            f"鱼种: {self.fish}\n"
            f"重量: {self.weight}\n"
            f"钓点: {self.location}\n"
            f"鱼饵: {self.bait}\n"
            f"玩家: {self.player}\n"
            f"日期: {self.date}\n"
            f"区域: {self.region}\n"
            f"分类: {self.category}"
        )

    @property
    def as_dict(self) -> dict:
        return {
            "fish"      : self.fish,
            "fish_image": self.fish_image,
            "weight"    : self.weight,
            "location"  : self.location,
            "bait"      : self.bait,
            "player"    : self.player,
            "date"      : self.date,
            "region"    : self.region,
            "category"  : self.category,
        }

    @property
    def weight_in_gram(self) -> int:
        return int(self.weight * 1000)


class AbsoluteRecord(Record):
    class Meta:
        verbose_name = "绝对纪录"
        verbose_name_plural = "绝对纪录"
        db_table     = "core_absolute_records"
        ordering     = ["id"]


class WeeklyRecord(Record):
    class Meta:
        verbose_name = "每周纪录"
        verbose_name_plural = "每周纪录"
        db_table     = "core_weekly_records"
        ordering     = ["id"]

from django.db import models


class Rating(models.Model):
    position = models.PositiveIntegerField(verbose_name = "排名")
    level    = models.PositiveIntegerField(verbose_name = "等级")
    ingame   = models.PositiveIntegerField(verbose_name = "游戏天数")
    region   = models.CharField(verbose_name = "区域", max_length = 4)
    player   = models.CharField(verbose_name = "玩家", max_length = 256)

    class Meta:
        verbose_name = "玩家评级"
        verbose_name_plural = "玩家评级"
        db_table     = "core_rating"
        ordering     = ["id"]

    def __str__(self) -> str:
        return (
            f"排名: {self.position}\n"
            f"玩家: {self.player}\n"
            f"等级: {self.level}\n"
            f"游戏天数: {self.ingame}\n"
            f"区域: {self.region}"
        )

    @property
    def as_dict(self) -> dict:
        return {
            "position": self.position,
            "player"  : self.player,
            "level"   : self.level,
            "ingame"  : self.ingame,
            "region"  : self.region,
        }

    @property
    def ingame_in_days(self) -> float:
        return round(self.ingame / 24, 2)

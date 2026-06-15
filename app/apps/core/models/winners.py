from django.db import models


class Winner(models.Model):
    position = models.PositiveIntegerField(verbose_name = "排名")
    records  = models.PositiveIntegerField(verbose_name = "纪录数")
    score    = models.PositiveIntegerField(verbose_name = "得分")
    player   = models.CharField(verbose_name = "玩家", max_length = 256)
    prize    = models.CharField(verbose_name = "奖品", max_length = 256, blank = True)
    region   = models.CharField(verbose_name = "区域", max_length = 4)
    category = models.CharField(verbose_name = "分类", max_length = 16)

    class Meta:
        verbose_name = "比赛优胜者"
        verbose_name_plural = "比赛优胜者"
        db_table     = "core_winners"
        ordering     = ["id"]

    def __str__(self) -> str:
        return (
            f"排名: {self.position}\n"
            f"玩家: {self.player}\n"
            f"纪录数: {self.records}\n"
            f"得分: {self.score}\n"
            f"奖品: {self.prize}\n"
            f"区域: {self.region}\n"
            f"分类: {self.category}"
        )

    @property
    def as_dict(self) -> dict:
        return {
            "position": self.position,
            "player"  : self.player,
            "records" : self.records,
            "score"   : self.score,
            "prize"   : self.prize,
            "region"  : self.region,
            "category": self.category
        }

from django.db import models

class TechnicalIndicator(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", unique=True)
    description = models.TextField(verbose_name="Описание")
    formula = models.TextField(verbose_name="Формула")
    recommendation = models.TextField(verbose_name="Рекомендации по использованию")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Технический индикатор"
        verbose_name_plural = "Технические индикаторы"

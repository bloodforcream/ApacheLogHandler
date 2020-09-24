from django.db import models
from django.core.validators import MaxValueValidator


class ApacheLog(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес лога')
    log_date = models.DateTimeField(verbose_name='Дата лога')
    http_method = models.CharField(verbose_name='Метод лога', max_length=10)
    uri = models.URLField(verbose_name='URI лога', max_length=1024)
    status_code = models.PositiveIntegerField(verbose_name='Статус код лога', validators=[MaxValueValidator(599)])
    response_size = models.PositiveIntegerField(verbose_name='Размер ответа', blank=True, null=True)

    def __str__(self):
        return f'{self.ip_address} | {self.status_code}'

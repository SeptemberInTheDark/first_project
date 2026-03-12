from django.db import models

# Create your models here.
# Phone с полями id, name, price, image, release_date, lte_exists и slug. Поле id — должно быть основным ключом модели.
class Phone(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.URLField(unique=True)
    release_date = models.DateField()
    lte_exists = models.BooleanField(default=False)
    slug = models.CharField(max_length=150, unique=True)


class Sensor(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name='measurements',
    )
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.sensor} - {self.temperature}'
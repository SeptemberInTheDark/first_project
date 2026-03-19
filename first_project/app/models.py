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



########################################################
class Teacher(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    subject = models.CharField(max_length=10, verbose_name='Предмет')

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    teachers = models.ManyToManyField(
        Teacher,
        related_name='students',
        verbose_name='Учителя',
    )
    group = models.CharField(max_length=10, verbose_name='Класс')

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'

    def __str__(self):
        return self.name



########################################################
class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Раздел')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Scope(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='scopes',
        verbose_name='Статья',
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='scopes',
        verbose_name='Раздел',
    )
    is_main = models.BooleanField(default=False, verbose_name='Основной')

    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статьи'
        ordering = ['-is_main', 'tag__name']

    def __str__(self):
        return f'{self.tag} для "{self.article}"'


# связь Article <-> Tag через Scope
Article.add_to_class(
    'tags',
    models.ManyToManyField(
        Tag,
        through='Scope',
        related_name='articles',
        verbose_name='Разделы',
    ),
)
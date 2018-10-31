from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from trading.models import Portfolio
from django.core.validators import MaxValueValidator, MinValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blnk=True)
    birth_date = models.DateField(null=True, blank=True)
    cash = models.PositiveIntegerField(default=25000, validators=[MinValueValidator(1), MaxValueValidator(10000000)])
    #stock_folio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True, null=True)    #   a profile can have 1 portfolio
    stock_folio = models.ManyToManyField(Portfolio, through='ProfilePortfolioJunction')             #   #   a profile can have multiple portfolio

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, force_insert=False, force_update=False, using=None):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.convert('RGB')
            img.thumbnail(output_size)
            img.save(self.image.path)


class ProfilePortfolioJunction(models.Model):
    owners = models.ForeignKey(Profile, on_delete=models.CASCADE)
    folio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    created = models.DateField(editable=False)
    modified = models.DateField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(StockPortfolioJunction, self).save(*args, **kwargs)

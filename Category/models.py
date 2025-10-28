from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.slug})"

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image:
            try:
                if hasattr(self.image, 'url') and hasattr(self.image, 'path'):
                    import os
                    if os.path.exists(self.image.path):
                        return self.image.url
            except (ValueError, AttributeError):
                pass
        return '/static/images/no-image.svg'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('category:product_detail', kwargs={'pk': self.pk})
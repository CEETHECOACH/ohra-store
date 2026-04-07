from django.db import models


class Product(models.Model):
    ACCENT_CHOICES = [
        ('ac-purple', 'Purple'),
        ('ac-gold',   'Gold'),
        ('ac-red',    'Red'),
        ('ac-pink',   'Pink'),
        ('ac-teal',   'Teal'),
        ('ac-brown',  'Brown'),
        ('ac-sunny',  'Yellow/Sunny'),
        ('ac-rose',   'Rose'),
    ]

    name        = models.CharField(max_length=200)
    brand       = models.CharField(max_length=100, default='Lattafa')
    notes       = models.CharField(max_length=300, help_text='e.g. Strawberry · Vanilla · Musk · 75ml')
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    badge       = models.CharField(max_length=50, blank=True, help_text='e.g. Best Seller, New In')
    accent      = models.CharField(max_length=20, choices=ACCENT_CHOICES, default='ac-gold')
    image       = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active   = models.BooleanField(default=True)
    order       = models.PositiveIntegerField(default=0, help_text='Lower number = shown first')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.name} — {self.brand} — ${self.price}'

    def price_display(self):
        return f'${self.price:.2f}'

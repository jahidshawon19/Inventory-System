from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Issue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    issued_quantity = models.PositiveIntegerField()
    issued_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issue - {self.product.name}"
    

class Return(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    return_quantity = models.PositiveIntegerField()
    return_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return - {self.product.name}"
from django.db import models
from django.urls import reverse


class TypeOfProduct(models.Model):
    """Model for product types such as dog food, cat food, and so on."""

    name = models.CharField(max_length=30, verbose_name='Product type')
    url_name = models.CharField(max_length=30, verbose_name='Product type in URL', default='-')
    image = models.ImageField(upload_to="types_of_prod_img/%Y/%m/%d/", verbose_name='Logo', blank=True)

    class Meta:
        verbose_name = 'Product type'
        verbose_name_plural = 'Product types'

    def __str__(self) -> str:
        return self.name


class FilterGroup(models.Model):
    """Model for a filter group."""

    title = models.CharField(max_length=255, verbose_name='Filter group title')
    type_of_products = models.ManyToManyField(TypeOfProduct, verbose_name='Product types for this filter group')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Title in URL')

    class Meta:
        verbose_name = 'Filter group'
        verbose_name_plural = 'Filter groups'

    def __str__(self) -> str:
        return self.title


class FilterItem(models.Model):
    """Model for an item inside a filter group."""

    name = models.CharField(max_length=255, verbose_name='Filter name')
    filter_group = models.ForeignKey('FilterGroup', on_delete=models.CASCADE, verbose_name='Filter group')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Name in URL')

    class Meta:
        verbose_name = 'Filter item'
        verbose_name_plural = 'Filter items'

    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    """Model for product brands."""

    SEGMENTS = [
        ('eco', 'Economy'),
        ('premium', 'Premium'),
        ('super-premium', 'Super premium')
    ]
    name = models.CharField(max_length=255, verbose_name='Brand name', unique=True)
    image = models.ImageField(upload_to="brand_logos/%Y/%m/%d/", verbose_name='Logo')
    segment = models.CharField(max_length=30, choices=SEGMENTS, verbose_name='Price segment')
    type_of_products = models.ManyToManyField(TypeOfProduct, verbose_name='Product types made by the brand')

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """Model for products."""

    name = models.CharField(max_length=255, verbose_name='Product name')
    vendor_code = models.CharField(max_length=255, verbose_name='Vendor code', unique=True)
    image = models.ImageField(upload_to="product_images/%Y/%m/%d/", verbose_name='Image')
    type_of_product = models.ForeignKey('TypeOfProduct', on_delete=models.CASCADE, verbose_name='Product type')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, verbose_name='Brand')
    description = models.TextField(verbose_name='Product description')
    in_stock = models.BooleanField(default=True, verbose_name='In stock')
    age_of_animal = models.CharField(max_length=255, verbose_name='Animal age', blank=True)
    source_of_protein = models.CharField(max_length=255, verbose_name='Protein source', blank=True)
    is_hit = models.BooleanField(default=False, verbose_name='Hit')
    filter_items = models.ManyToManyField(FilterItem, verbose_name='Filters', blank=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self) -> str:
        return f'{self.name}, #{self.vendor_code}'

    def get_absolute_url(self):
        return reverse('product_view', kwargs={'vendor_code':self.vendor_code})
    
    @staticmethod
    def get_products_by_filters(query_set, filters_ids):
        products = query_set.filter(filter_items__in = filters_ids)
        unique_products = list()
        for pr in products:
            if pr not in unique_products:
                unique_products.append(pr)
        return unique_products
    
    
class Packing(models.Model):
    """Model describing a packing option for a product."""

    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Product for this packing')
    weight = models.IntegerField(verbose_name='Weight (kg)')
    current_price = models.IntegerField(verbose_name='Current price (USD)')
    old_price = models.IntegerField(verbose_name='Old price in USD (if a discount is active)', blank=True, null=True)

    class Meta:
        verbose_name = 'Packing'
        verbose_name_plural = 'Packings'

    def __str__(self) -> str:
        return f'{self.product}, {self.weight} kg, {self.current_price} USD'


class ProductInCart(models.Model):
    """Model for products stored in the client's cart."""
    session_key = models.CharField(max_length=128)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    packing = models.ForeignKey(Packing, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField()

    class Meta:
        verbose_name = 'Cart item'
        verbose_name_plural = 'Cart items'

    def get_full_current_price(self):
        return self.packing.current_price * self.amount
    
    def get_full_old_price(self):
        return self.packing.old_price * self.amount


    
    





    







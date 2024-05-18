from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from random import sample
from io import BytesIO
import string, random
import qrcode
from decimal import Decimal

from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask


class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)

    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters + string.digits, 18))

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/category/')

    def __str__(self):
        return self.name

    # class Meta:
    #     verbose_name_plural = 'Categories'


class Product(CodeGenerate):
    """Maxsulotlar"""
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/product/')
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField(default=0)
    qr_code = models.ImageField(upload_to='media/qrcode/', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        QRcode = qrcode.QRCode()
        # QRcode.add_data(f"http://127.0.0.1:8000/product/detail/{self.code}")
        QRcode.add_data(
            f"Maxsulot Nomi: {self.name},\nCategoryasi: {self.category},\nNarxi: {self.price},\nSoni: {self.quantity}"
        )
        QRcode.make()
        QRimg = QRcode.make_image(
            image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(), color_mask=RadialGradiantColorMask()
        )
        fname = f"qrcode{self.id}.png"
        buffer = BytesIO()
        QRimg.save(buffer, format="PNG")
        self.qr_code.save(fname, File(buffer), save=False)
        QRimg.close()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Products'


class EnterProduct(CodeGenerate):
    """Do'kongdagi Mavjud maxsulotni Ustiga qo'shish yani qolmagan bolsa yana qoshish"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def enter_price(self):
        price = 0
        price = float(self.product.price) * int(self.quantity)
        return price

    def save(self, *args, **kwargs):
        if self.pk:
            obj = EnterProduct.objects.get(pk=self.pk)
            self.product.quantity = int(self.product.quantity) - int(obj.quantity)

        self.product.quantity = int(self.product.quantity) + int(self.quantity)
        self.product.save()

        super(EnterProduct, self).save(*args, **kwargs)


class ExportProduct(CodeGenerate):
    """Do'kondan maxsulotlarni sotilishi yani chiqishi"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        if self.pk:
            obj = ExportProduct.objects.get(pk=self.pk)
            self.product.quantity = int(self.product.quantity) + int(obj.quantity)

        if int(self.product.quantity) > int(self.quantity):
            self.product.quantity = int(self.product.quantity) - int(self.quantity)
            self.product.save()

        super(ExportProduct, self).save(*args, **kwargs)

    @property
    def export_price(self):
        price = 0
        price = float(self.product.price) * int(self.quantity)
        return price

    class Meta:
        verbose_name_plural = 'ExportsProducts'


class ReturnProduct(CodeGenerate):
    """Maxsulotni qaytarib yuborish"""
    product = models.ForeignKey(ExportProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if int(self.product.quantity) >= int(self.quantity):
            self.product.quantity = int(self.product.quantity) - int(self.quantity)
            self.product.save()
            super(ReturnProduct, self).save(*args, **kwargs)

    @property
    def return_price(self):
        price = 0
        price = float(self.product.product.price) * int(self.quantity)
        return price

    def __str__(self):
        return self.product.name

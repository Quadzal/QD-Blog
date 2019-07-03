from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Article(models.Model):
    author   = models.ForeignKey("auth.user", on_delete=models.CASCADE, verbose_name="Yazar", related_name = "articles")
    category = models.ForeignKey("article.category", on_delete=models.CASCADE, verbose_name="Kategori", null=True, related_name="articleList")
    
    title    = models.CharField(max_length= 50, verbose_name= "Başlık", unique= True)
    content  = RichTextField(config_name= "default",   null= True, verbose_name= "İçerik")
    slug     = models.SlugField(db_index=True, blank= True, null= True,  editable= False)
    image    = models.ImageField(verbose_name="Resim", null=True, blank=True)
    created_date = models.DateTimeField(verbose_name= "Oluşturulma Tarihi", auto_now_add= True)

    class Meta:
        verbose_name = "Makaleler"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, null=True, related_name="comments", on_delete=models.CASCADE)
    author  = models.ForeignKey("auth.user", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(verbose_name="Yorum")
    created_date = models.DateTimeField(verbose_name="Gönderildiği Tarih", auto_now_add=True)
    def __str__(self):
        return self.content

class Category(models.Model):
    title = models.CharField(db_index=True, max_length=50, verbose_name="Kategori Adı", unique=True)
    class Meta:
        verbose_name = "Kategoriler"
    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user     = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    
    tel_no   = models.CharField(max_length=11, verbose_name="Telefon Numarası", null=True, blank=True)
    about    = models.TextField(max_length=1000, verbose_name="Biyografi", null=True, blank=True)
    image    = models.ImageField(verbose_name="Profil Fotoğrafı", null=True, blank=True)
    birth_date = models.DateField(verbose_name="Doğum Tarihi", blank=True, null=True)
    class Meta:
        verbose_name = "Profil Bilgileri"

    def __str__(self):
        return "%s Profili" % (self.user.get_full_name() or self.user.get_username())


def create_user_profile(instance, created, **kwargs):
    """
        Eğer Kullanıcı Yeni Oluşturulmuşsa Ona Ait Bir Profilde Oluştur.
    """
    if created:
        UserProfile.objects.create(user=instance)

# Eğer User Modelinde Save Çalışırsa create_user_profile Fonksiyonuda Çalışsın.
post_save.connect(receiver=create_user_profile, sender=User) 

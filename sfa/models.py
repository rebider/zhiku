from django.db import models
from django.db.models.query import QuerySet
from .managers import SoftDeletableManager
from inventory.models import Industry
from public.models import Town
from personnel.models import Staff
# Create your models here.

# 自定义软删除抽象基类
class SoftDeletableModel(models.Model):
    """
    An abstract base class model with a ``is_deleted`` field that
    marks entries that are not going to be used anymore, but are
    kept in db for any reason.
    Default manager returns only not-deleted entries.
    """
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    objects = SoftDeletableManager()

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object (set its ``is_deleted`` field to True).
        Actually delete object if setting ``soft`` to False.
        """
        if soft:
            self.is_deleted = True
            self.save(using=using)
        else:
            return super(SoftDeletableModel, self).delete(using=using, *args, **kwargs)


class CustomerInfo(SoftDeletableModel):
    delete_choice = ((0, '保留'), (1, '删除'))
    purpose_choice = ((0, 'A类客户'), (1, 'B类客户'),(2, 'C类客户'), (3, 'D类客户'),(4, 'k类客户'), (5, 'k1类客户'),(6, 'k2类客户'))
    nid = models.AutoField(primary_key=True)
    category = models.ForeignKey("CustomerCategory", to_field="nid", on_delete=models.CASCADE, verbose_name='客户分类',
                                 db_constraint=False)
    purpose = models.IntegerField(choices=purpose_choice,default=3,verbose_name="意向分类")
    company = models.CharField(max_length=64, verbose_name="公司名称")
    industry = models.ForeignKey(Industry, to_field="nid", on_delete=models.CASCADE, verbose_name='行业',
                                 db_constraint=False)
    business = models.CharField(max_length=64, verbose_name="主营业务" )
    employees = models.IntegerField(verbose_name='公司人数')
    introduce = models.CharField(max_length=512, verbose_name="简介", blank=True, null=True)
    website = models.CharField(max_length=64, verbose_name="网站", blank=True, null=True)
    phone = models.CharField(max_length=16, verbose_name="联系电话", blank=True, null=True)
    town = models.ForeignKey(Town, to_field="nid", on_delete=models.CASCADE, verbose_name='街道',
                               db_constraint = False)
    address = models.CharField(max_length=64, verbose_name="地址", blank=True, null=True)
    remark = models.TextField(max_length=512, verbose_name="备注", blank=True, null=True)
    recorder = models.ForeignKey(Staff, to_field="sid", on_delete=models.CASCADE, verbose_name='录入人',
                                 db_constraint=False)
    is_deleted = models.BooleanField(default=False,verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'customer_info'
        verbose_name = '客户信息'
        verbose_name_plural = '客户信息'

    def __str__(self):
        return self.company

    _insert = ["category","purpose","company" ,"category_id","recorder_id","industry_id", "business""employees","introduce",'website',"remark","address",
                "town_id", "phone"]
    _update = ["category","purpose","company","category_id", "industry_id", "business","employees","introduce",'website',"remark","address",
                "town_id","phone"]


class CustomerCategory(models.Model):
    nid = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=16,verbose_name="类别")

    class Meta:
        db_table = 'customer_category'
        verbose_name = '客户分类'
        verbose_name_plural = '客户分类'

    def __str__(self):
        return self.caption

    _insert = ["caption"]
    _update = ["caption"]


class CustomerAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    customer = models.ForeignKey('CustomerInfo', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='客户')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'customer_attach'
        verbose_name = '客户附件'
        verbose_name_plural = '客户附件'

    def __str__(self):
        return "客户附件:{0}".format(self.name)


class CustomerLicence(models.Model):
    nid = models.AutoField(primary_key=True)
    customer = models.ForeignKey('CustomerInfo', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='客户')
    photo = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'customer_licence'
        verbose_name = '客户营业执照'
        verbose_name_plural = '客户营业执照'

    def __str__(self):
        return "营业执照:{0}".format(self.name)

    _update = ["photo","name"]


class CustomerPhoto(models.Model):
    nid = models.AutoField(primary_key=True)
    customer = models.ForeignKey('CustomerInfo', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='客户')
    photo = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'customer_photo'
        verbose_name = '客户照片'
        verbose_name_plural = '客户照片'

    def __str__(self):
        return "客户照片:{0}".format(self.name)

    _update = ["photo","name"]


class CustomerLinkman(SoftDeletableModel):
    gender_choice = ((0, "男"), (1, "女"))
    marriage_choice = ((0, "未婚"), (1, "已婚"))
    delete_status_choice = ((0, '删除'), (1, '保留'))
    is_lunar = ((0, "公历"), (1, "农历"))

    nid = models.AutoField(primary_key=True)
    customer = models.ForeignKey('CustomerInfo', to_field="nid", on_delete=models.CASCADE, db_constraint=False,
                                   default=1, verbose_name='客户')
    name = models.CharField(max_length=32, verbose_name='联系人')
    gender = models.SmallIntegerField(choices=gender_choice, verbose_name="性别", default=0)
    age = models.SmallIntegerField(verbose_name="年龄", blank=True, null=True)
    marriage = models.SmallIntegerField(choices=marriage_choice, verbose_name="婚姻", default=0)
    mobile = models.CharField(max_length=11, verbose_name="手机号码", blank=True, null=True)
    phone = models.CharField(max_length=16, verbose_name="电话", blank=True, null=True)
    ext_phone = models.CharField(max_length=16, verbose_name="分机", blank=True, null=True)
    birthday = models.DateField(verbose_name="生日", blank=True, null=True)
    is_lunar = models.SmallIntegerField(choices=is_lunar, verbose_name="生日农历or公历", default=0)
    native_place = models.CharField(max_length=64, verbose_name="籍贯", blank=True, null=True)
    is_deleted = models.BooleanField(default=False,verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'customer_linkman'
        verbose_name = '联系人'
        verbose_name_plural = '联系人'

    def __str__(self):
            return self.name

    _insert = ["customer_id", "name", "gender", "age", "marriage", "mobile", "phone", "ext_phone",
               "birthday","is_lunar","native_place"]
    _update = ["customer_id", "name", "gender", "age", "marriage", "mobile", "phone", "ext_phone",
               "birthday","is_lunar","native_place"]


class CustomerLinkmanAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    linkman = models.ForeignKey('CustomerLinkman', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                            verbose_name='联系人')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'customer_linkman_attach'
        verbose_name = '联系人附件'
        verbose_name_plural = '联系人附件'

    def __str__(self):
        return "联系人附件:{0}".format(self.name)


class CustomerLinkmanCard(models.Model):
    nid = models.AutoField(primary_key=True)
    linkman = models.ForeignKey("CustomerLinkman", to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='联系人')
    photo = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'customer_linkman_card'
        verbose_name = '联系人名片'
        verbose_name_plural = '联系人名片'

    def __str__(self):
        return "联系人名片:{0}".format(self.name)

    _update = ["photo","name"]


class CustomerLinkmanPhoto(models.Model):
    nid = models.AutoField(primary_key=True)
    linkman = models.ForeignKey('CustomerLinkman', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='联系人')
    photo = models.CharField(max_length=255, blank=True, null=True, verbose_name='路径')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')

    class Meta:
        db_table = 'customer_linkman_photo'
        verbose_name = '联系人图片'
        verbose_name_plural = '联系人图片'

    def __str__(self):
        return "联系人图片:{0}".format(self.name)

    _update = ["photo","name"]


class CustomerMemo(SoftDeletableModel):
    nid = models.AutoField(primary_key=True)
    customer = models.ForeignKey('CustomerInfo', to_field="nid", on_delete=models.CASCADE, db_constraint=False,
                                 default=1, verbose_name='客户')
    title = models.CharField(max_length=16,verbose_name="标题")
    detail = models.CharField(max_length=16,verbose_name="详细")
    recorder = models.ForeignKey(Staff, to_field="sid", on_delete=models.CASCADE, verbose_name='登记人',
                                 db_constraint=False)
    is_deleted = models.BooleanField(default=False,verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_edit = models.DateTimeField(auto_now=True, verbose_name='最后编辑时间')

    class Meta:
        db_table = 'customer_memo'
        verbose_name = '客户备忘'
        verbose_name_plural = '客户备忘'

    def __str__(self):
        return self.title

    _insert = ["customer_id","title",'detail',"recorder_id"]
    _update = ["customer_id","title",'detail',"recorder_id"]


class CustomerMemoAttach(models.Model):
    nid = models.AutoField(primary_key=True)
    memo = models.ForeignKey('CustomerMemo', to_field='nid', on_delete=models.CASCADE, db_constraint=False,
                              verbose_name='客户备忘')
    attachment = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件路径')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='附件名称')
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name='附件描述')

    class Meta:
        db_table = 'customer_memo_attach'
        verbose_name = '备忘附件'
        verbose_name_plural = '备忘附件'

    def __str__(self):
        return "备忘附件:{0}".format(self.name)
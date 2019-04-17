from django.db import models

# Create your models here.
class MyCharField(models.Field):
    """
    自定义的 char 类型的字段
    """
    def __init__(self, max_length, *args, **kwargs):
        self.max_length = max_length
        super(MyCharField, self).__init__(max_length=max_length, *args, **kwargs)

    def db_type(self, connection):
        return 'char(%s)' % self.max_length

class user(models.Model):
    '''用户表'''
    uid = models.BigAutoField(primary_key=True)  
    uaccount = models.CharField(max_length=255, unique=True)
    unamech = models.CharField(max_length=255, null=True)
    unameen = models.CharField(max_length=255)
    umail = models.CharField(max_length=255, unique=True)
    upassword = models.CharField(max_length=255)
    uphone = MyCharField(max_length=11)
    uall = models.BooleanField()

class college(models.Model):
    '''高校表'''
    coid = models.BigAutoField(primary_key=True)
    coname = models.CharField(max_length=255)
class company(models.Model):
    '''二级单位表'''
    cid = models.BigAutoField(primary_key=True)
    coid = models.ForeignKey(college, on_delete=models.CASCADE)
    dename = models.CharField(max_length=255)
class author(models.Model):
    '''作者字段表'''
    aid = models.BigAutoField(primary_key=True)
    cid = models.ForeignKey(company, on_delete=models.CASCADE)
    aname = models.CharField(max_length=255)
    amail = models.CharField(max_length=255)
class achievement(models.Model):
    '''成果表'''
    user_id = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    abstract = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
class project(models.Model):
    '''项目表'''
    pro_id = models.CharField(max_length=255)
    pro_name = models.CharField(max_length=255)

class project_achievement(models.Model):
    '''项目成果关联表'''
    achievement_id = models.ForeignKey(achievement,on_delete=models.CASCADE)
    pro_id = models.ForeignKey(project,on_delete=models.CASCADE)
    order = models.IntegerField()

class achievement_author(models.Model):
    '''作者与成果关联表'''
    author_id = models.ForeignKey(author,on_delete=models.CASCADE)
    achievement_id = models.ForeignKey(achievement,on_delete=models.CASCADE)
    iscorr = models.BooleanField() #是否是通讯作者
    isfirst = models.BooleanField() #是否是第一作者
    order = models.IntegerField()

class journal_paper(models.Model):
    '''期刊论文表'''
    title = models.CharField(max_length=255)
    jname = models.CharField(max_length=255)
    status = models.BooleanField()
    pubdate = models.DateField()
    volume = models.CharField(max_length=255,null=True)
    issue = models.CharField(max_length=255,null=True)
    pages = models.CharField(max_length=255,null=True)
    indexed = models.CharField(max_length=255,null=True)
    doi = models.CharField(max_length=255,null=True)
    achievement_id = models.ForeignKey(achievement, on_delete=models.CASCADE)

class patent(models.Model):
    '''专利表'''
    country = models.CharField(max_length=255)
    ptype = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    status = models.BooleanField() #申请是flase 授权是true
    number = models.CharField(max_length=255)#申请号/专利授权号
    ipc = models.CharField(max_length=255,null=True)
    cpc = models.CharField(max_length=255,null=True)
    owner = models.CharField(max_length=255,null=True)#专利申请人/专利授权人
    aptime = models.DateField()#申请日期/公开日期
    pubnumber = models.CharField(max_length=255,null=True)
    ssue_begin = models.DateField(null=True)
    ssue_end = models.DateField(null=True)
    transition = models.CharField(max_length=255,null=True)
    price = models.FloatField(null=True)
    achievement_id = models.ForeignKey(achievement, on_delete=models.CASCADE)

class conference_paper(models.Model):
    '''会议论文表'''
    ctype = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    conference_name = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255,null=True)
    country = models.CharField(max_length=255)
    pubdate = models.DateField(null=True)
    proceeding = models.CharField(max_length=255,null=True)
    begin_date = models.DateField()
    end_date = models.DateField()
    pages = models.CharField(max_length=255,null=True)
    indexed = models.CharField(max_length=255,null=True)
    doi = models.CharField(max_length=255,null=True)
    achievement_id = models.ForeignKey(achievement, on_delete=models.CASCADE)

class book(models.Model):
    '''书，著作表'''
    name = models.CharField(max_length=255)
    series = models.CharField(max_length=255,null=True)
    btype = models.CharField(max_length=255)
    isbn = models.CharField(max_length=255)
    edit = models.CharField(max_length=255)
    pubdate = models.DateField()
    publisher = models.CharField(max_length=255)
    country = models.CharField(max_length=255) #国家或地区
    total_words = models.IntegerField()
    lang = models.CharField(max_length=255)
    achievement_id = models.ForeignKey(achievement, on_delete=models.CASCADE)

class chapter(models.Model):
    '''章节表'''
    title = models.CharField(max_length=255)
    book_title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=255,null=True)
    pages = models.CharField(max_length=255,null=True)
    pubdate = models.DateField()
    edit = models.CharField(max_length=255)
    country = models.CharField(max_length=255) #国家或地区
    publisher = models.CharField(max_length=255)
    achievement_id = models.ForeignKey(achievement, on_delete=models.CASCADE)

class degree_paper(models.Model):
    '''学术论文表'''
    title = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    pubdate = models.DateField()
    institution = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    doi = models.CharField(max_length=255,null=True)
    achievement_id = models.ForeignKey(achievement, on_delete=models.CASCADE)
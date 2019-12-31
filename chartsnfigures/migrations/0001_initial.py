# Generated by Django 3.0 on 2019-12-31 07:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('last_mod_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改时间')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='分类名')),
                ('slug', models.SlugField(blank=True, default='no-slug', max_length=60)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chartsnfigures.Category', verbose_name='父级分类')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='链接名称')),
                ('link', models.URLField(verbose_name='链接地址')),
                ('sequence', models.IntegerField(unique=True, verbose_name='排序')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否显示')),
                ('show_type', models.CharField(choices=[('i', '首页'), ('l', '列表页'), ('p', '报告页面'), ('a', '全站'), ('s', '友情链接页面')], default='i', max_length=1, verbose_name='显示类型')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('last_mod_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '友情链接',
                'verbose_name_plural': '友情链接',
                'ordering': ['sequence'],
            },
        ),
        migrations.CreateModel(
            name='SideBar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('sequence', models.IntegerField(unique=True, verbose_name='排序')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('last_mod_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '侧边栏',
                'verbose_name_plural': '侧边栏',
                'ordering': ['sequence'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('last_mod_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改时间')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='标签名')),
                ('slug', models.SlugField(blank=True, default='no-slug', max_length=60)),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WebsiteSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sitename', models.CharField(default='', max_length=200, verbose_name='网站名称')),
                ('site_description', models.TextField(default='', max_length=1000, verbose_name='网站描述')),
                ('site_seo_description', models.TextField(default='', max_length=1000, verbose_name='网站SEO描述')),
                ('site_keywords', models.TextField(default='', max_length=1000, verbose_name='网站关键字')),
                ('cnfreport_sub_length', models.IntegerField(default=300, verbose_name='报告摘要长度')),
                ('sidebar_cnfreport_count', models.IntegerField(default=10, verbose_name='侧边栏报告数目')),
                ('sidebar_comment_count', models.IntegerField(default=5, verbose_name='侧边栏评论数目')),
                ('show_google_adsense', models.BooleanField(default=False, verbose_name='是否显示谷歌广告')),
                ('google_adsense_codes', models.TextField(blank=True, default='', max_length=2000, null=True, verbose_name='广告内容')),
                ('open_site_comment', models.BooleanField(default=True, verbose_name='是否打开网站评论功能')),
                ('beiancode', models.CharField(blank=True, default='', max_length=2000, null=True, verbose_name='备案号')),
                ('analyticscode', models.TextField(default='', max_length=1000, verbose_name='网站统计代码')),
                ('show_gongan_code', models.BooleanField(default=False, verbose_name='是否显示公安备案号')),
                ('gongan_beiancode', models.TextField(blank=True, default='', max_length=2000, null=True, verbose_name='公安备案号')),
                ('resource_path', models.CharField(default='/var/www/resource/', max_length=300, verbose_name='静态文件保存地址')),
            ],
            options={
                'verbose_name': '网站配置',
                'verbose_name_plural': '网站配置',
            },
        ),
        migrations.CreateModel(
            name='CNFReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('last_mod_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改时间')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='标题')),
                ('body', mdeditor.fields.MDTextField(verbose_name='正文')),
                ('pub_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间')),
                ('status', models.CharField(choices=[('d', '草稿'), ('p', '发表')], default='p', max_length=1, verbose_name='报告状态')),
                ('comment_status', models.CharField(choices=[('o', '打开'), ('c', '关闭')], default='o', max_length=1, verbose_name='评论状态')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='浏览量')),
                ('report_order', models.IntegerField(default=0, verbose_name='排序,数字越大越靠前')),
                ('featured_image', models.ImageField(upload_to='report_pictures/%Y/%m/%d/', verbose_name='特色图片')),
                ('report_sourcefile', models.FileField(upload_to='report_files/%Y/%m/%d/', verbose_name='报告源数据文件')),
                ('report_sourcedata', models.TextField(verbose_name='报告源数据')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chartsnfigures.Category', verbose_name='分类')),
                ('tags', models.ManyToManyField(blank=True, to='chartsnfigures.Tag', verbose_name='标签集合')),
            ],
            options={
                'verbose_name': '数据和图表报告',
                'verbose_name_plural': '数据和图表报告',
                'ordering': ['-report_order', '-pub_time'],
                'get_latest_by': 'id',
            },
        ),
    ]

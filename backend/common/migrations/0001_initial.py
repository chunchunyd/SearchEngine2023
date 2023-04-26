# Generated by Django 4.1 on 2023-04-26 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Agent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="代理人名称")),
                ("h_type", models.CharField(max_length=10, verbose_name="代理人类型")),
                (
                    "profession",
                    models.CharField(
                        blank=True, max_length=30, verbose_name="代理人辩护人职业类型"
                    ),
                ),
                (
                    "a_type",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="辩护人或诉讼代理人类型"
                    ),
                ),
            ],
            options={
                "verbose_name": "代理人",
                "verbose_name_plural": "代理人",
            },
        ),
        migrations.CreateModel(
            name="Court",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="法院名称")),
                ("code", models.CharField(max_length=10, verbose_name="法院层级码")),
                ("level", models.CharField(max_length=10, verbose_name="法院级别")),
                ("province", models.CharField(max_length=30, verbose_name="省份")),
                ("city", models.CharField(max_length=50, verbose_name="城市")),
            ],
            options={
                "verbose_name": "法院",
                "verbose_name_plural": "法院",
            },
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "agency",
                    models.CharField(
                        choices=[("1", "法院"), ("2", "检察院"), ("3", "司法行政")],
                        max_length=20,
                        verbose_name="文云制作单位",
                    ),
                ),
                ("doc_type", models.CharField(max_length=30, verbose_name="文书种类")),
                ("full_text", models.TextField(verbose_name="全文")),
            ],
            options={
                "verbose_name": "文书",
                "verbose_name_plural": "文书",
            },
        ),
        migrations.CreateModel(
            name="Judge",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="法官名称")),
                ("full_name", models.CharField(max_length=100, verbose_name="法官全称")),
            ],
            options={
                "verbose_name": "法官",
                "verbose_name_plural": "法官",
            },
        ),
        migrations.CreateModel(
            name="LawReference",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("law_name", models.CharField(max_length=100, verbose_name="法律名称")),
                ("law_clause", models.CharField(max_length=30, verbose_name="条")),
                ("law_clause_item", models.CharField(max_length=30, verbose_name="款")),
                ("law_item", models.CharField(max_length=30, verbose_name="项")),
            ],
            options={
                "verbose_name": "法条引用",
                "verbose_name_plural": "法条引用",
            },
        ),
        migrations.CreateModel(
            name="Party",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="当事人名称")),
                ("name_is_fuzzy", models.BooleanField(verbose_name="当事人名称是否模糊")),
                ("h_type", models.CharField(max_length=10, verbose_name="当事人类型")),
                (
                    "status",
                    models.CharField(blank=True, max_length=10, verbose_name="诉讼身份"),
                ),
                (
                    "nationality",
                    models.CharField(blank=True, max_length=10, verbose_name="国籍"),
                ),
                (
                    "nation",
                    models.CharField(blank=True, max_length=10, verbose_name="民族"),
                ),
                (
                    "gender",
                    models.CharField(blank=True, max_length=10, verbose_name="性别"),
                ),
                ("birthday", models.DateField(blank=True, verbose_name="出生日期")),
            ],
            options={
                "verbose_name": "当事人",
                "verbose_name_plural": "当事人",
            },
        ),
        migrations.CreateModel(
            name="Procuratorate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="检察院名称")),
                (
                    "district_code",
                    models.CharField(max_length=10, verbose_name="行政区划代码"),
                ),
                ("province", models.CharField(max_length=30, verbose_name="省份")),
                ("city", models.CharField(max_length=50, verbose_name="城市")),
                ("county", models.CharField(max_length=50, verbose_name="区县")),
                ("level", models.IntegerField(verbose_name="检察院级别")),
            ],
            options={
                "verbose_name": "检察院",
                "verbose_name_plural": "检察院",
            },
        ),
        migrations.CreateModel(
            name="Prosecution",
            fields=[
                (
                    "document_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="common.document",
                    ),
                ),
                ("case_number", models.CharField(max_length=100, verbose_name="案号")),
                ("case_type", models.CharField(max_length=30, verbose_name="案件类别")),
                ("p_date", models.DateField(verbose_name="(不)起诉日期")),
                (
                    "court",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.court",
                        verbose_name="诉至法院",
                    ),
                ),
                (
                    "defendant",
                    models.ManyToManyField(
                        related_name="prosecution_defendant",
                        to="common.party",
                        verbose_name="被告",
                    ),
                ),
                (
                    "procuratorate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.procuratorate",
                        verbose_name="检察院",
                    ),
                ),
            ],
            options={
                "verbose_name": "检察院文书",
                "verbose_name_plural": "检察院文书",
            },
            bases=("common.document",),
        ),
        migrations.CreateModel(
            name="Judgment",
            fields=[
                (
                    "document_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="common.document",
                    ),
                ),
                ("case_number", models.CharField(max_length=100, verbose_name="案号")),
                ("case_type", models.CharField(max_length=30, verbose_name="案件类别")),
                ("judgment_date", models.DateField(verbose_name="裁判日期")),
                (
                    "court",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.court",
                        verbose_name="法院",
                    ),
                ),
                (
                    "defendant",
                    models.ManyToManyField(
                        related_name="defendant", to="common.party", verbose_name="被告"
                    ),
                ),
                (
                    "defendant_agent",
                    models.ManyToManyField(
                        blank=True,
                        related_name="defendant_agent",
                        to="common.agent",
                        verbose_name="被告代理人",
                    ),
                ),
                ("judge", models.ManyToManyField(to="common.judge", verbose_name="法官")),
                (
                    "law_reference",
                    models.ManyToManyField(
                        to="common.lawreference", verbose_name="法条引用"
                    ),
                ),
                (
                    "plaintiff",
                    models.ManyToManyField(
                        related_name="plaintiff", to="common.party", verbose_name="原告"
                    ),
                ),
                (
                    "plaintiff_agent",
                    models.ManyToManyField(
                        blank=True,
                        related_name="plaintiff_agent",
                        to="common.agent",
                        verbose_name="原告代理人",
                    ),
                ),
            ],
            options={
                "verbose_name": "判决书",
                "verbose_name_plural": "判决书",
            },
            bases=("common.document",),
        ),
    ]
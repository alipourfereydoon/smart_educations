# طرح پایگاه‌داده

برنامه مدل‌های Django را در SQLite اجرا می‌کند. فهرست مرجع مدل‌ها در `education/models.py` است. مقادیر نمره‌های ویژگی و اطمینان در بازهٔ ۰ تا ۱ هستند؛ `feature_json` و `rules_json` برای ویژگی‌های انعطاف‌پذیر JSON هستند.

## موجودیت‌ها و روابط

- **User (Django)** یک‌به‌یک `StudentProfile`؛ پروفایل شامل پایه و زبان ترجیحی است.
- `Questionnaire` یک‌به‌چند `Response`؛ پرسش‌نامه عنوان و وضعیت فعال دارد.
- `Question` شامل دسته‌بندی، نوع پاسخ، حدود مقیاس، ترتیب و پرچم امتیاز معکوس است.
- `StudentProfile` یک‌به‌چند `Response`, `Assessment`, `Recommendation`, `LearningPlan`, `Outcome`.
- `Response` به دانش‌آموز، پرسش و پرسش‌نامه متصل است؛ قید یکتایی (دانش‌آموز، پرسش، پرسش‌نامه) از ثبت پاسخ تکراری جلوگیری می‌کند.
- `Assessment` snapshot ویژگی‌های استخراج‌شده، منبع و نسخهٔ مدل است؛ پرسش‌نامه می‌تواند حذف‌پذیر باشد.
- `InterventionStrategy` کاتالوگ فعالیت‌ها؛ `Recommendation` ارزیابی و راهبرد را به هم وصل می‌کند و وضعیت پیشنهاد را نگه می‌دارد.
- `LearningPlan` یک‌به‌چند `PlanItem`؛ فعالیت می‌تواند به یک recommendation اشاره کند.
- `Outcome` سنجهٔ پیامد؛ `ModelVersion` نسخه و معیارهای مدل؛ `AuditLog` رویدادهای مدیریتی.

### توصیف ERD

```text
User 1──1 StudentProfile 1──* Response *──1 Question
                              *──1 Questionnaire
StudentProfile 1──* Assessment 1──* Recommendation *──1 InterventionStrategy
StudentProfile 1──* LearningPlan 1──* PlanItem *──0..1 Recommendation
StudentProfile 1──* Outcome; PlanItem 0..1──* Outcome
ModelVersion (نسخه‌های مدل)      User 0..1──* AuditLog
```

مدل‌ها indexهایی برای جست‌وجوی پاسخ، تاریخ ارزیابی، فعالیت و لاگ دارند. حذف استراتژی ارجاع‌شده به recommendation با `PROTECT` ممنوع است؛ وابستگی‌های پاسخ/فعالیت از سیاست cascade پیروی می‌کنند.

## SQLite و دادهٔ آزمایشی

SQLite پایگاه پیش‌فرض مناسب اجرای محلی است. ابتدا migrationها را اعمال کنید و سپس `python manage.py seed_demo` را اجرا کنید. دادهٔ seed شامل حساب `ali`، ۱۸ سؤال در شش دسته، پاسخ‌های نمونه، پنج راهبرد (از جمله human review)، ارزیابی و برنامه است. این پاسخ‌ها مصنوعی و صرفاً برای نمایش رابط هستند؛ دادهٔ جمعیت واقعی نیستند.

## مهاجرت به PostgreSQL

1. PostgreSQL بسازید و کاربر محدود به schema برنامه ایجاد کنید؛ رمز را فقط در secret manager بگذارید.
2. در محیط مجازی `pip install dj-database-url psycopg[binary]` را نصب کنید.
3. backend را در `config/settings.py` از `DATABASE_URL` بخوانید، مثلاً با `dj_database_url.config(conn_max_age=600, ssl_require=True)`؛ `DATABASE_URL` را در `.env` یا محیط سرویس تنظیم کنید. مخزن فعلی عمداً همچنان تنظیم SQLite دارد و اتصال production باید پیکربندی شود.
4. قبل از deploy، `python manage.py makemigrations --check --dry-run` و `python manage.py migrate` را اجرا کنید. برای دادهٔ SQLite از dump/ETL کنترل‌شده یا ابزار migration استفاده و تعداد/ارتباط رکوردها را تطبیق دهید؛ صرفاً فایل SQLite را به PostgreSQL کپی نکنید.
5. نسخهٔ پشتیبان، SSL، نقش‌های کم‌دسترسی، مانیتورینگ و rollback را آزمایش کنید. پس از انتقال، نسخهٔ قدیمی را مطابق سیاست نگهداری حذف کنید.

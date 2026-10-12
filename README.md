# یادینو — نمونهٔ آموزشی هوشمند

این بسته یک نمونهٔ توسعه‌ای Django برای نمایش یک چرخهٔ سادهٔ پرسش‌نامه، ساخت نمایهٔ یادگیری، پیشنهاد فعالیت و ثبت بازخورد است. پایگاه‌داده و دادهٔ آموزشی فعلی **دمو و مصنوعی** هستند؛ برای استفادهٔ واقعی باید داده‌ها، رضایت و ارزیابی انسانی فراهم شود.

## پیش‌نیاز و نصب

- Python 3.10 یا جدیدتر (ترجیحاً 3.11/3.12)
- pip و محیط مجازی

```bash
cd smart_education
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env  # در Windows فایل را دستی کپی کنید
```

در `.env` برای محیط توسعه `DEBUG=True` مجاز است. مقدار `SECRET_KEY` را برای هر استقرار عوض کنید و آن را در مخزن عمومی قرار ندهید.

## ساخت پایگاه‌داده و دادهٔ نمونه

```bash
python manage.py makemigrations education
python manage.py migrate
python manage.py seed_demo
```

فرمان `seed_demo` یک دانش‌آموز نمونه، پرسش‌ها، راهبردها، پاسخ‌های ساختگی، یک ارزیابی و برنامه ایجاد می‌کند. مشخصات ورود نمونه در کد فرمان موجود است: `ali / Ali12345!`؛ برای محیط واقعی این گذرواژه را استفاده نکنید.

## آموزش مدل

```bash
python ml_engine/train_model.py
```

این فرمان دادهٔ مصنوعی `ml_engine/training_data.csv` را می‌خواند و خروجی `ml_engine/artifacts/recommender.joblib` و `metrics.json` می‌سازد. مدل صرفاً نمایشی است و نباید دربارهٔ دانش‌آموزان تصمیم‌گیری خودکار یا پرمخاطره کند.

## اجرا

```bash
python manage.py runserver
```

نشانی محلی: <http://127.0.0.1:8000/>. صفحات و endpointها:

| مسیر | روش | توضیح |
|---|---|---|
| `/` | GET | خانه و دانش‌آموز نمونه |
| `/questionnaire/<student_id>/` | GET, POST | نمایش پرسش‌نامه و ثبت پاسخ |
| `/profile/<student_id>/` | GET | نمایه، نمره‌های ویژگی و پیشنهادها |
| `/plan/<student_id>/` | GET | برنامه و فعالیت‌های یادگیری |
| `/api/feedback/<plan_item_id>/` | POST | ثبت JSON بازخورد/وضعیت فعالیت |
| `/admin/` | GET | پنل مدیریتی Django |

جزئیات payload در [docs/API.md](docs/API.md) و طرح داده در [docs/DATABASE.md](docs/DATABASE.md) است.

## استقرار، حریم خصوصی و امنیت

- `DEBUG=False`، `SECRET_KEY` تصادفی، `ALLOWED_HOSTS` محدود، HTTPS و کوکی امن را در تولید تنظیم کنید.
- پنل admin و endpointهای دانش‌آموزی در نمونه برای سادگی احراز هویت/مجوز مالکیت ندارند؛ پیش از استقرار حتماً login، کنترل دسترسی مبتنی بر مالکیت، throttling، ثبت رویداد امن و سیاست نگهداری داده اضافه کنید.
- اعتبارسنجی CSRF برای فرم‌ها و endpoint فعال است؛ درخواست feedback باید CSRF token بفرستد.
- اطلاعات شناسایی‌پذیر را از دادهٔ آموزش جدا کنید، حداقل‌سازی و حذف‌پذیری داده را اجرا کنید، دسترسی را محدود کنید و نسخهٔ پشتیبان رمزگذاری‌شده داشته باشید.
- ارزیابی آموزشی به‌تنهایی تشخیص پزشکی/روان‌شناختی نیست. نتیجه‌ها را توضیح‌پذیر و قابل اعتراض نگه دارید، معلم/خانواده را در حلقه قرار دهید و تفاوت‌های زبانی، فرهنگی، معلولیت و سوگیری را بررسی کنید.

## ساختار

`education/` مدل‌ها، viewها و سرویس‌های Django؛ `templates/` قالب‌ها؛ `static/` CSS/JS راست‌به‌چپ؛ `ml_engine/` مهندسی ویژگی، مدل و دادهٔ مصنوعی؛ `docs/` مستندات فنی. راهنمای ML: [docs/ML.md](docs/ML.md).

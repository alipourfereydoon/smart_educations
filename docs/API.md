# API و صفحات

نمونه مسیرها با پیشوند root تعریف شده‌اند. صفحات Django HTML برمی‌گردانند؛ تنها endpoint فعلی JSON، بازخورد برنامه است. نمونه‌ها از `student_id=1` و `plan_item_id=1` استفاده می‌کنند و شناسهٔ واقعی به seed وابسته است.

## صفحات

- `GET /` — صفحهٔ اصلی.
- `GET /questionnaire/<student_id>/` — فرم پرسش‌های فعال.
- `POST /questionnaire/<student_id>/` — submit فرم HTML با `csrfmiddlewaretoken` و مقدار `q_<question_id>` برای هر سؤال؛ پاسخ‌های معتبر ذخیره و assessment/recommendation ساخته می‌شود.
- `GET /profile/<student_id>/` — پروفایل و پیشنهادها.
- `GET /plan/<student_id>/` — برنامه و آیتم‌ها.

## ثبت بازخورد برنامه

`POST /api/feedback/<plan_item_id>/` با `Content-Type: application/json` و CSRF معتبر:

```json
{"completed": true, "completion_percent": 100, "feedback": "تمرین را کامل کردم."}
```

`completed` بولی، `completion_percent` عدد صحیح ۰ تا ۱۰۰ و `feedback` رشته‌ای تا ۱۰۰۰ نویسه است. پاسخ موفق:

```json
{"ok": true, "completed": true, "completion_percent": 100}
```

خطای JSON نامعتبر با status 400:

```json
{"error": "درخواست JSON نامعتبر است."}
```

شناسهٔ ناموجود 404 است؛ خطای اعتبارسنجی تابع `record_feedback` ممکن است در حال حاضر به خطای سرور تبدیل شود. نسخهٔ تولیدی باید خطاهای ورودی را به پاسخ 400/422 تبدیل کند. endpoint نمونه احراز هویت و بررسی مالکیت آیتم ندارد؛ عمومی‌سازی آن ناامن است. مجوز شیء، rate limit و ثبت امن را اضافه کنید.

### درخواست با curl

```bash
curl -i -X POST http://127.0.0.1:8000/api/feedback/1/ \
  -H 'Content-Type: application/json' -H 'X-CSRFToken: <token>' \
  -b 'csrftoken=<token>; sessionid=<session>' \
  --data '{"completed":true,"completion_percent":100,"feedback":"انجام شد"}'
```

برای فرم‌های مرورگر از token ساخته‌شده توسط `{% csrf_token %}` استفاده کنید؛ غیرفعال کردن middleware راه‌حل نیست.

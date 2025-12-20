🛒 پروژه فروشگاه آنلاین Acron

یک سیستم فروشگاه آنلاین کامل که با Django و MySQL توسعه یافته است و دارای قابلیت‌های مدیریت محصول، سبد خرید، کاربران و سفارش‌گذاری می‌باشد.
📋 فهرست مطالب

    ویژگی‌های پروژه

    پیش‌نیازها

    نصب و راه‌اندازی

    ایجاد داده‌های نمونه

    دستورات مفید

    مدیریت پایگاه داده

    ساختار پروژه

    مشارکت در پروژه

    مجوز

✨ ویژگی‌های پروژه

    ✅ سیستم احراز هویت کاربران

    ✅ مدیریت دسته‌بندی محصولات

    ✅ سیستم تخفیف و promotions

    ✅ سبد خرید و ثبت سفارش

    ✅ سیستم نظردهی و کامنت‌گذاری

    ✅ آدرس‌دهی مشتریان

    ✅ داده‌های نمونه برای تست

    ✅ اتصال به پایگاه داده MySQL

🛠 پیش‌نیازها

قبل از نصب، مطمئن شوید موارد زیر روی سیستم شما نصب شده‌اند:

    پایتون 3.8 یا بالاتر

    MySQL 5.7 یا بالاتر

    Git (برای مدیریت نسخه‌ها)

    Pip (مدیریت پکیج‌های پایتون)

🚀 نصب و راه‌اندازی
۱. کلون کردن مخزن
bash

git clone https://github.com/sinalalebakhsh/acronproject.git
cd acronproject

۲. ایجاد محیط مجازی (اختیاری اما توصیه می‌شود)
bash

python -m venv venv
# در ویندوز:
venv\Scripts\activate
# در مک/لینوکس:
source venv/bin/activate

۳. نصب dependencies
bash

pip install -r requirements.txt

۴. تنظیمات پایگاه داده MySQL

ابتدا وارد MySQL Workbench یا خط فرمان MySQL شوید:
sql

-- ایجاد پایگاه داده جدید
CREATE DATABASE store CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- یا اگر می‌خواهید پایگاه داده قبلی را بازسازی کنید
DROP DATABASE IF EXISTS store;
CREATE DATABASE store CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

سپس فایل settings.py را مطابق با تنظیمات پایگاه داده خود پیکربندی کنید.
۵. اجرای migrations
bash

python manage.py migrate

۶. اجرای سرور توسعه
bash

python manage.py runserver

اکنون می‌توانید پروژه را در آدرس http://localhost:8000 مشاهده کنید.
📊 ایجاد داده‌های نمونه

برای پر کردن پایگاه داده با داده‌های تستی، دستور زیر را اجرا کنید:
bash

python manage.py setup_fake_data

خروجی مورد انتظار:
text

Deleting old data...
Creating new data...
Adding 100 categories...DONE
Adding 10 discounts...DONE
Adding 1000 product...DONE
Adding 100 customers...DONE
Adding customers addresses...DONE
Adding 30 orders...DONE
Adding order items...DONE
Adding product comments...DONE
Adding 100 carts...DONE
Adding cart items...DONE

🔧 دستورات مفید
مدیریت Migration‌ها
bash

# مشاهده SQL تولید شده برای یک migration خاص
python manage.py sqlmigrate store 0001

# ایجاد migration جدید
python manage.py makemigrations

# اعمال تمام migration‌ها
python manage.py migrate

مدیریت کش Git
bash

# حذف فایل‌های __pycache__ از کش git
git rm -r --cached */__pycache__

# پاک کردن کامل کش gitignore و بازنگری فایل‌ها
git rm -r --cached .
git add .
git commit -m "Clear gitignore cache"

اسکریپت خودکار Git
bash

# دادن مجوز اجرا به اسکریپت
chmod +x git-automate.sh

# اجرای اسکریپت
./git-automate.sh

🗄️ مدیریت پایگاه داده
ابزارهای مورد نیاز

    MySQL Workbench

    MySQL Benchmarks

کوئری‌های کاربردی
sql

-- مشاهده آخرین نظرات
SELECT * FROM store.store_comment ORDER BY id DESC;

-- مشاهده محصولات و دسته‌بندی آن‌ها
SELECT p.name, c.name as category_name 
FROM store_product p 
JOIN store_category c ON p.category_id = c.id;

-- مشاهده سفارشات کاربران
SELECT u.username, o.order_date, o.total_amount 
FROM store_order o 
JOIN auth_user u ON o.user_id = u.id;

📁 ساختار پروژه
text

acronproject/
├── manage.py
├── requirements.txt
├── git-automate.sh
├── README.md
├── .gitignore
├── store/                      # اپلیکیشن اصلی فروشگاه
│   ├── migrations/             # فایل‌های migration
│   ├── models.py              # مدل‌های پایگاه داده
│   ├── views.py               # view functions
│   ├── urls.py                # URL routing
│   ├── admin.py               # تنظیمات پنل ادمین
│   └── tests.py               # تست‌ها
├── templates/                  # فایل‌های قالب HTML
├── static/                     # فایل‌های استاتیک (CSS, JS, images)
└── media/                      # فایل‌های آپلود شده توسط کاربران

🤝 مشارکت در پروژه

ما از مشارکت‌های شما استقبال می‌کنیم! برای مشارکت:

    مخزن را Fork کنید

    یک Branch جدید ایجاد کنید (git checkout -b feature/feature-name)

    تغییرات خود را Commit کنید (git commit -m 'Add some feature')

    تغییرات را Push کنید (git push origin feature/feature-name)

    یک Pull Request باز کنید

دستور العمل‌های Commit

    از پیام‌های commit توصیفی استفاده کنید

    تغییرات مربوطه را در یک commit قرار دهید

    قبل از commit، کد خود را تست کنید

📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است. برای مشاهده جزئیات کامل، فایل LICENSE را مطالعه کنید.
📞 پشتیبانی

برای گزارش مشکلات یا پیشنهاد ویژگی‌های جدید، لطفاً از بخش Issues استفاده کنید.

توسعه‌یافته با ❤️ توسط تیم Acron

آخرین بروزرسانی: مارس ۲۰۲۴

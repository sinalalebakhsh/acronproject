# تابع محاسبه gcd با الگوریتم اقلیدس
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# تابع پیدا کردن کوچک‌ترین عدد نسبت به هم اول با phi
def smallest_coprime(phi):
    for e in range(2, phi):  # از 2 شروع می‌کنیم چون 1 خیلی ساده است
        if gcd(e, phi) == 1:
            return e   # اولین عددی که gcd=1 شد همون کوچک‌ترین e است
    return None  # اگر چیزی پیدا نشد (نادیده گرفتن حالت نادر)

# مثال
phi = 20
e = smallest_coprime(phi)
print(f"کوچک‌ترین عدد نسبت به {phi} که می‌تواند e باشد: {e}")


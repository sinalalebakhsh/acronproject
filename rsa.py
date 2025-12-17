# تابع محاسبه gcd با الگوریتم اقلیدس
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# تابع پیدا کردن کوچک‌ترین عدد نسبت به هم اول با phiφ
def smallest_coprime(phiφ):
    for e in range(2, phiφ):  # از 2 شروع می‌کنیم چون 1 خیلی ساده است
        if gcd(e, phiφ) == 1:
            return e   # اولین عددی که gcd=1 شد همون کوچک‌ترین e است
    return None  # اگر چیزی پیدا نشد (نادیده گرفتن حالت نادر)


q = int(input('q:'))
p = int(input('p:'))
n = q * p # حاصلضرب دو عدد اول


phiφ = (q-1) * (p-1)
e = smallest_coprime(phiφ)


# پیدا کردن کوچک‌ترین d که (e*d) % phiφ == 1
d = None # کلید خصوصی 
for x in range(1, phiφ):
    if (e * x) % phiφ == 1:
        d = x
        break

public_key = (e, n, ) 
private_key = (d, n, ) 


message = int(input('message:')) #123


#  مرحله 1: تبدیل پیام به محدوده n  
# 123 mod 33 = 24
m = message % n # چون باید کوچکتر از n ب




# مرحله 2: رمزنگاری با کلید عمومی e 
# رمزنگاری: c = m^e mod n
cipher = pow(m, e, n)  # pow با سه آرگومان: پایه، توان، مد
# هیچ‌کس از روی 30 نمی‌فهمه 123 بوده.


"""
تو یک قانون مخفی داری که فقط خودت می‌دونی:
«هر چی اومد، به توان 7 برس و بعد باقی‌مانده تقسیم بر 33 رو بگیر»


# رمزگشایی دستی: m = c^d mod n
decrypted = 1  # شروع از 1 برای ضرب مکرر


for i in range(d):
    decrypted = (decrypted * cipher) % n  # هر بار ضرب و گرفتن باقی‌مانده
    # توضیح: با این روش عدد خیلی بزرگ نمی‌شود

"""
# مرحله 3: رمزگشایی با کلید خصوصی d
decrypted = pow(cipher, d, n)  # m = c^d mod n



def reconstruct_message(decrypted, n, message):
    """
    decrypted: عدد بعد از رمزگشایی (داخل محدوده n)
    n: حاصلضرب دو عدد اول (محدوده RSA)
    message: حد بالایی پیام اصلی (مثلاً 123 یا هر عددی که می‌دانیم پیام اصلی نباید بیشتر از آن باشد)
    
    خروجی: پیام اصلی
    """
    # محاسبه k خودکار: تعداد دفعاتی که n داخل پیام اصلی جا شده
    k = 0
    while decrypted + k * n <= message:
        k += 1
    k -= 1  # آخرین k که عدد از حد بالاتر نرفت

    # بازسازی پیام اصلی
    message = decrypted + k * n
    return message



print('q: ', q) # 3
print('p: ', p) # 11
print('message: ', message) #123

print('n = q * p: ', n) 
print('__________________________')
print('φ(n) phiφ = (q-1) * (p-1): ',phiφ)
print('__________________________')
print(f"e = smallest_coprime for {phiφ} = {e}")
print('__________________________')
print(f"secret_number d: {d}")
print('__________________________')
print('public_key: (e, n, ) ', public_key)
print('__________________________')
print('private_key: (d, n, ) ', private_key)
print('__________________________')
print('cipher = pow(m, e, n): ', cipher)
print('__________________________')

print('can not geast 123 from 30')
print('__________________________')
print(f"decrypted: {decrypted}")
print('__________________________')
print(f"decrypted message: {message}")  # خروجی: 123


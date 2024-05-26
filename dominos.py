import sqlite3
conn=sqlite3.connect('my.db')
b=conn.cursor()
#b.execute('create table Domuser(name char,phno number,email char)')
#b.execute('create table cart(phno number,cartvalues char)')
#print('Completed')
d={
    'veg':{'Margerita':129,'cheese_and_corn':169,'peppi_paneer':260,'veg_loaded':210,'tomato_tangi':170},
    'non_veg':{'pepper_barbeque':199,'non_veg_loaded':169,'chicken_sausage':200},
    'snacks' :{'garlic_bread':120,'zingy':59,'c_cheese_balls':170},
    'desserts':{'choco_lava':100,'mousse_cake':169},
    'drinks':{'coke':90,'pepsi':78,'sprite':50}
}

login_status = False
cart = {}
pnum = ''
mode = 0

def valid_phno(phno):
    s=str(phno)
    return len(s)==10 and '6'<=s[0]<='9' and s.isnumeric()

def check_phno(phno):
    l = list(b.execute('select phno from Domuser'))
    return (phno,) in l

def valid_email(e):
    s = e[-10:]
    return s in ['@gmail.com','@yahoo.com'] and 'a' <= e[0]<= 'z' and e[0:-10].isalnum()

def check_email(e):
    l = list(b.execute('select email from Domuser'))
    return (e,) in l

def Dominos():
    print('Enter 1: signup')
    print('Enter 2: login')
    ch=int(input('Enter your choice'))
    if ch == 1:
        while True:
            print('Please Fill Your Details')
            name=input('Enter name: ')
            while True:
                phno = int(input('Enter phno: '))
                if valid_phno(phno):
                    break
                else:
                    print('Invalid phno')
            while True:
                email = input('Enter email: ')
                if valid_email(email):
                    break
                else:
                    print('Invalid email')
            m,n=check_email(email),check_phno(phno)
            if m==False and n==False:
                b.execute(f'insert into Domuser values("{name}","{phno}","{email}")')
                conn.commit()
                print('Signup successful')
                break
            elif m==True:
                print('Email already Exixts')
            else:
                print('phno already Exists')
    else:
        login()
def get_otp(a):
    global login_status
    import random
    while True:
        otp=random.randint(100000,999999)
        print('your otp is: ',otp)
        print('An OTP has been sent to Your ',a)
        tp =  int(input('Enter OTP: '))
        if tp==otp:
            print('Logged in Successfully')
            login_status = True
            break
        else:
            print('Incorrect OTP')
def login():
    global pnum,login_status
    if login_status==True:
        return 'Already logged in'
    print('Enter 1:login with phno')
    print('Enter 2:login with email')
    c=int(input('Enter your choice: '))
    if c==1:
        pnum=int(input('Enter phno: '))
        if check_phno(pnum):
            get_otp(pnum)
        else:
            print('Phno doesnt exist')
    else:
        email=input('Enter email: ')
        pnum=list(b.execute(f'select phno from Domuser where email="{email}"'))[0][0]
        if check_email(email):
            get_otp(email)
        else:
            print('Email Doesnt Exists')
def logout():
    global login_status
    login_status=False
    print('Logged out successfully')

def order(new=0):
    global mode
    if login_status==True:
        print('Enter 1: Dine in')
        print('Enter 2: Take away')
        print('Enter 3: Home Delivery')
        ch=int(input('Enter choice: '))
        mode=ch
        out={}
        di=list(d)
        while True:
            print('Enter 1: veg')
            print('Enter 2: Non-Veg')
            print('Enter 3: Snacks')
            print('Enter 4 : Desserts')
            print('Enter 5: Drinks')
            print('Enter 6: End')
            c=int(input('Enter your item: '))
            if 1<=c<=6:
                if c==6:
                    break
                m=list(d)[c-1]
                m=list(d[m])
                for i in range(1,len(m)+1):
                    print(f'Enter {i}: {m[i-1]} ')
                choice=int(input('Enter choice: '))
                q=int(input('Enter quantity: '))
                if 1<=choice<=len(m):
                    out[m[choice-1]]=[q,q*d[di[c-1]][m[choice-1]]]
                    print('Item added')
                else:
                    print('Invalid choice')
            else:
                print('Invalid choice')
            cart.update(out)
            if cart!={} and new==0:
                b.execute(f'Insert into cart values("{pnum}","{cart}")')
                conn.commit()
            else:
                print('Login is Required')

def dis_bill():
    if login_status==True:
        if mode==1:
            total_amt=0
        elif mode==2:
            print('Parcel charges of 25Rs. will be include')
            total_amt=25
        elif mode==3:
            print('Parcel charges of 25Rs and Delivery charges of Rs 50 will be included')
            total_amt=75
        print('Item','Quantity','Price')
        for i in cart:
            print(i,' '*(20-len(i)),cart[i][0],' '*4,cart[i][1])
            total_amt+=cart[i][1]

        print('Total Bill: ',total_amt)
    else:
        print('Login is Required')


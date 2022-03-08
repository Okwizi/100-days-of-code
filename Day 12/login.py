email_list = "Michael"
reg_list = 4047

def login_email(email_):
    while email_ != email_list:
        return "Incorrect email"
        break


def login_reg(reg_):
    while reg_ != reg_list:
        return "Incorrect password"
        break


email = input(print("Enter email: "))
email_out = login_email(email)
print(email_out)
if email_out == "Incorrect email":
    print("Nah fam")
else:
    reg = int(input(print("Enter password: ")))
    reg_out = login_reg(reg)
    if reg_out == "Incorrect password":
        print(reg_out)
    else:
        print("Successful login")
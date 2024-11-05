import datetime

birthDay = int(input("Enter your birth Date: "));
birthMonth = int(input("Enter your birth Month: "));
birthYear = int(input("Enter your birth Year: "));

birth = datetime.date(birthYear, birthMonth, birthDay);
print("Birth", birth);

today = datetime.date.today();
print("Today", today);

if(
    today.month == birth.month
    and today.day >= birth.day
    or today.month > birth.month
) :
    nextBirthYear = today.year + 1;

else: nextBirthYear = today.year

nextBirthYear = datetime.date(
    nextBirthYear, birth.month, birth.day
)

print("Next Birthday: ", nextBirthYear);

diff = nextBirthYear - today

print("Days left for next birthday: ", diff.days);
import json
import smtplib, os, requests
from colorama import init

init()
with open("days_logged.txt", mode="r") as z:
    j = json.load(z)
if not j:
    goal_c = True
    while goal_c:
        question = input("Do you have a goal for the month? Answer 'yes' or 'no': ").strip().lower()
        if question == "yes":
            while True:
                goal = input("Write your goal for the month: ").strip().title()
                if len(goal) > 0:
                    with open("monthly_goal.txt", mode="w") as q:
                        q.write(goal)
                    goal_c = False
                    break
                else:
                    print("The field can not be empty, please write your goal for the month.")
                    continue
        elif question == "no":
            print("Let's proceed.")
            goal_c = False
        else:
            print("Response not valid, answer 'yes' or 'no'.")
            goal_c = True

with open("monthly_goal.txt", mode="r") as y:
    achieve = y.read()
if achieve:
    print("\033[4mHELLO AND WELCOME TO YOUR MONTHLY EXPENSE TRACKER.\033[0m".center(95))
    print(f"You can keep track of your daily expense(s), which will sum up to your monthly expenses.\nREMEMBER YOUR "
          f"FINANCIAL GOAL FOR THE MONTH: \033[4m{achieve.upper()}\033[0m")
else:
    print("HELLO AND WELCOME TO YOUR MONTHLY EXPENSE TRACKER".center(87))
    print(f"You can keep track of your daily expense(s), which will sum up to your monthly expenses.")

NUMBERS = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
try:
    with open("days_logged.txt", "r") as z:
        logged_days = json.load(z)
except (FileNotFoundError, ValueError, SyntaxError, json.JSONDecodeError):
    logged_days = []
if not logged_days:
    d_num = 0
else:
    d_num = int(logged_days[-1][3:])

##notification message
def send_ntfy():
    topic = os.environ.get('NTFY_TOPIC')
    text = "Hey Michael, your monthly expense evaluation has been done, saved and sent to your email. Check it out."
    requests.post(
        f"https://ntfy.sh/{topic}",
        data=text.encode('utf-8'),
        headers={"Title": "Monthly Expense Summary now ready!"},
        timeout=30
    )

def nothing_spent():
    monthly_expense = []
    daily = {}
    day = input("What day do you want to log? e.g. 'day1', 'day2'...'day30' or 'day31' max: ").lower().strip().replace(" ", "")
    if day in logged_days:
        print("You have already logged this day")
    elif day[:3] == "day" and int(day[3:]) not in NUMBERS:
        print("This is not a valid day to log, log a day between 1 - 30 or 31, in this format 'day1'...'day31'")
        nothing_spent()
    elif int(day[3:]) - d_num > 1 and day[:3] == "day":
        print(f"You have not logged day{d_num+1} yet, it is recommended to log all the days prior to {day}\n"
              f"to get a more accurate monthly evaluation. You can log everything now given you have\na record of what "
              f"you spent on the un-logged day(s).")
        if logged_days:
            print(f"NOTE: Your last entry is {logged_days[-1]}.")
        else:
            print("NOTE: Your next entry is supposed to be day1.")
        nothing_spent()
    elif day[:3] == "day" and int(day[3:]) in NUMBERS:
        if int(day[3:]) == 1:
            print("This is your first entry for a new month, let's go. Remember try to keep your monthly expenses as low"
                  "as possible.")
        logged_days.append(day)
        total_cost = "total_cost"
        price = "Price"
        things_bought = ["nothing"]
        costs = 0.0
        cost = 0.0
        daily[day] = things_bought
        daily[price] = costs
        daily[total_cost] = cost
        monthly_expense.append(daily)
        with open("days_logged.txt", "w") as t:
            json.dump(logged_days, t, indent=2)
    else:
        print("Your response is not valid, type in this format: 'day1', 'day2'...'day30' or 'day31' max.")
        nothing_spent()
    return monthly_expense


def log_a_day():
    monthly_expense = []
    daily = {}
    items = []
    costs = []
    total_cost = "total_cost"
    price = "Price"
    day = input("What day do you want to log? e.g. 'day1', 'day2'...'day30' or 'day31' max: ").lower().strip().replace(" ", "")
    if day in logged_days:
        print("You have already logged this day")
    elif day[:3] == "day" and int(day[3:]) not in NUMBERS:
        print("This is not a valid day to log, log a day between 1 - 30 or 31, in this format 'day1'...'day31'")
        log_a_day()
    elif int(day[3:]) - d_num > 1 and day[:3] == "day":
        print(f"You have not logged day{d_num + 1} yet, it is recommended to log all the days prior to {day}\n"
              f"to get a more accurate monthly evaluation. You can log everything now given you have\na record of what "
              f"you spent on the un-logged day(s).")
        if logged_days:
            print(f"NOTE: Your last entry is {logged_days[-1]}.")
        else:
            print("NOTE: Your next entry is supposed to be day1.")
        log_a_day()
    elif day[:3] == "day" and int(day[3:]) in NUMBERS:
        logged_days.append(day)
        with open("days_logged.txt", "w") as t:
            json.dump(logged_days, t, indent=2)
        if int(day[3:]) == 1:
            print("This is your first entry for a new month, let's go. Remember, try to keep your monthly expenses as low "
                  "as possible.")
        total_items = int(input("How many items did you spend money on? "))
        for x in range(total_items):
            while True:
                item = input("Mention an item you spent money on: ")
                if len(item) == 0:
                    print("Please type an item")
                    continue
                else:
                    break
            amount = round(float(input("How much for the item?: ")), 2)
            costs.append(amount)
            items.append(item)

        cost = sum(costs)
        daily[day] = items
        daily[price] = costs
        daily[total_cost] = cost
        monthly_expense.append(daily)
    else:
        print("Your response is not valid, type in this format: 'day1', 'day2'...'day30' or 'day31' max.")
        log_a_day()
    return monthly_expense

def check_total_expenses():
    with open("record.txt", "r") as g:
        content = json.load(g)
    total = 0
    for x in content:
        daily_cost = x['total_cost']
        total += daily_cost
    return total


def daily_price(number):
    with open("record.txt", "r") as c:
        contents = json.load(c)

    day = f"day{number}"
    key_to_find = day
    found_index = 0

    for index, record in enumerate(contents):
        if key_to_find in record:
            #found_dict = record
            found_index = index
            break

    daily_cost = contents[found_index]["total_cost"]
    return daily_cost

def daily_items(number):
    with open("record.txt", "r") as v:
        contents = json.load(v)

    day = f"day{number}"
    key_to_find = day

    #found_dict = None
    found_index = 0

    for index, record in enumerate(contents):
        if key_to_find in record:
            # found_dict = record
            found_index = index
            break

    daily_items_list = contents[found_index][day]
    #
    n = 1
    print(f"On Day{number}, the item(s) you spent money on were:")
    for x in daily_items_list:
        print(f"{n}.", x.capitalize()+".")
        n += 1

def monthly_expenses():
    with open("record.txt", "r") as p:
        label = json.load(p)
    total = 0
    for x in label:
        daily_total = x["total_cost"]
        total += daily_total

    monthly_items = []
    # first_key = list(label[0].keys())[0]  # 'day12'
    # d = int(first_key[3:])  # Skip 'day', get '12', convert to 12
    for n in label:
        day = list(n.keys())[0]
        item = n[day]
        monthly_items.append(item)

    avg = total/len(label)
    months_year = input("What month & year did you check this expenses for? e.g. "
                      "'march2026': ").lower().strip().replace(" ", "")
    m_generated = float(input("How much did you make this month?: "))

    with open("monthly_goal.txt", mode="r") as p:
        monthly_goal = p.read()
    if ((1/2) * m_generated) > total:
        message = (f"{months_year[:-4].capitalize()} Expenses: ₦{total:,}\nDaily Average Spend: ₦{avg:,}\nItems Bought: "
                   f"{monthly_items}\n\nAdded Note: "
                   f"Hey Michael, it is that time of the month again for your review "
                   f"and based on the figures, you did well in your expenses, keep it up. You made "
                   f"a total of ₦{m_generated}, spent a total of ₦{total}, with an average daily spend of ₦{avg:,} and "
                   f"saved ₦{(m_generated - total):,} keep it up.\n\nYour goal for the month was: {monthly_goal.upper()}")
    else:
        message = (f"{months_year[:-4].capitalize()} Expenses: ₦{total:,}\nDaily Average Spend: ₦{avg:,}\nItems Bought: "
                   f"{monthly_items}\n\nAdded Note: "
                   f"Hey Michael, it is that time of the month again for your review "
                   f"and based on the figures, your expenses is way more than your income can handle "
                   f"either you up your monthly income or cut your expenses, you should consider "
                   f"increasing your income and at same time, keep your expenses low. You made "
                   f"a total of ₦{m_generated:,}, spent a total of ₦{total:,}, with an average daily spend of ₦{avg:,} and "
                   f"saved ₦{(m_generated - total):,}. Up your game, you are getting whooped in the area of finance"
                   f"\n\nYour goal for the month was: {monthly_goal.upper()}")


    while True:
        print("Sending mail...")
        try:
            my_email = "romeoclimate@gmail.com"
            password = os.environ.get('GMAIL_APP_PASSWORD')
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(from_addr=my_email,
                                    to_addrs="newsnotifications1@gmail.com",
                                    msg=f"Subject:Expense Summary for {months_year[:-4].capitalize()}, {months_year[-4:]}.\n\n{message}")
            print("Mail sent.")
            break
        except requests.exceptions.ConnectionError as e:
            print(f"Error while sending mail: No Internet Connection.\nThe error message is: \n'{e}'")
            continue
        except requests.exceptions.RequestException as e:
            print(f"Error while sending mail: Network/Server issue.\nThe error message is: \n'{e}'")
            continue
        except Exception as e:
            print(f"Error while sending mail:\n\nThe error message is: \n{e}")
            continue
    try:
        send_ntfy()
        print("Phone notification sent as well.")
    except requests.exceptions.ConnectionError as e:
        print(f"Phone Notification: No Internet Connection.\n\nThe error message is: \n'{e}'")
    except requests.exceptions.RequestException as e:
        print(f"Phone Notification: Network/Server issue.\n\nThe error message is: \n'{e}'")
    return total, monthly_items, avg, months_year

print("What would you like to do today?")
cycle = True
while cycle:
    user_act = input("a.) Log a day.\nb.) Check total expense so far.\nc.) Check a particular "
                     "day's total expense.\nd.) Check monthly expenses.\ne.) Check a particular "
                     "day's total items bought.\nf.) View your entire log.\ng.) Exit the program. "
                     "\nType a, b, c, d, e, f or g: ").lower().strip().replace(" ", "")
    if user_act == "a":
        cycle1= True
        while cycle1:
            ask = input("Did you spend money today? answer: yes/no: ").lower().strip().replace(" ", "")
            if ask == "yes":
                addition = log_a_day()
                if not addition:
                    print("Note: If you end the program here, this your current session won't record any log.")
                    cycle1 = False
                else:
                    try:
                        with open("record.txt", "r") as f:
                            data = json.load(f)
                    except (FileNotFoundError, ValueError, SyntaxError, json.JSONDecodeError):
                        data = []

                    data.extend(addition)
                    with open("record.txt", "w") as f:
                        json.dump(data, f, indent=2)
                    print("Your daily log has been successful.")
                    cycle1 = False
                    cycle = False
            elif ask == "no":
                addition = nothing_spent()
                if not addition:
                    print("Note: If you end the program here, this your current session won't record any log.")
                    cycle1 = False
                else:
                    try:
                        with open("record.txt", "r") as f:
                            data = json.load(f)
                    except (FileNotFoundError, ValueError, SyntaxError, json.JSONDecodeError):
                        data = []

                    data.extend(addition)
                    with open("record.txt", "w") as f:
                        json.dump(data, f, indent=2)
                    print("Your daily log has been successful.")
                    print("NOTE: Your items bought is saved as 'nothing', Price of item as 0.0, while total cost is 0.0")
                    cycle1 = False
                    cycle = False
            else:
                print("Sorry, your response is not recognised, carefully, answer with yes or no")
                cycle1 = True

    elif user_act == "b":
        try:
            total_expense = check_total_expenses()
            print(f"Your total expenses so far is: ₦{total_expense:,}")
        except (FileNotFoundError, ValueError, SyntaxError, json.JSONDecodeError):
            print("No expenses logged yet. Please log a day first.")
        cycle = False
    elif user_act == "c":
        try:
            specific_day = int(input("What day's total expenses do you want to check? E.g. 1, 2 etc: ").replace(" ", ""))
            if specific_day in NUMBERS:
                with open("days_logged.txt", "r") as z:
                    logged_days = json.load(z)
                real_day = f"day{specific_day}"
                if real_day in logged_days:
                    day_cost = daily_price(specific_day)
                    print(f"You spent a total of ₦{day_cost:,} on Day{specific_day}.")
                else:
                    print("You have not logged this day yet.")
            else:
                print("The number you entered is not valid.")
        except (FileNotFoundError, ValueError, SyntaxError, json.JSONDecodeError):
            print("No expenses logged yet. Please log a day first.")
        except IndexError:
            print("That day doesn't exist in your records.")
        cycle = False
    elif user_act == "d":
        try:
            monthly_spend, monthly_purchase, avg_day_spend, month_year = monthly_expenses()
            print(f"Your monthly expenses summed up to ₦{monthly_spend:,} "
                  f"with an average daily spend of ₦{avg_day_spend:,}. What you spent money on during the course of "
                  f"this period are: {monthly_purchase:,}")

            try:
                with open("monthly_data_storage.json", "r") as i:
                    monthly_data = json.load(i)
            except (FileNotFoundError, ValueError, SyntaxError, json.JSONDecodeError):
                monthly_data = {
                    month_year: {
                        "monthly_total_spent": monthly_spend,
                        "monthly_total_items": monthly_purchase
                    }
                }
                with open("monthly_data_storage.json", "w") as i:
                    json.dump(monthly_data, i, indent=4)
                    with open("record.txt", "w") as f:
                        json.dump([], f)
                    with open("days_logged.txt", "w") as k:
                        json.dump([], k)
            else:
                monthly_saved_data = {
                    month_year: {
                        "monthly_total_spent": monthly_spend,
                        "monthly_total_items": monthly_purchase
                    }
                }
                monthly_data.update(monthly_saved_data)
                with open("monthly_data_storage.json", "w") as i:
                    json.dump(monthly_data, i, indent=4)
                with open("record.txt", "w") as f:
                    json.dump([], f)
                with open("days_logged.txt", "w") as k:
                    json.dump([], k)
        except (FileNotFoundError, ValueError, SyntaxError, json.JSONDecodeError):
            print("No expenses logged yet. Please log a day first.")
        cycle = False
    elif user_act == "e":
        try:
            specific_day = int(input("What day's items do you want to check? E.g. 1, 2 etc: ").replace(" ", ""))
            if specific_day in NUMBERS:
                with open("days_logged.txt", "r") as z:
                    logged_days = json.load(z)
                real_day = f"day{specific_day}"
                if real_day in logged_days:
                    daily_items(specific_day)
                else:
                    print("You have not logged this day.")
            else:
                print("The number you entered is not valid.")
        except (FileNotFoundError, ValueError, SyntaxError, json.JSONDecodeError):
            print("No expenses logged yet. Please log a day first.")
        except IndexError:
            print("That day doesn't exist in your records.")
        cycle = False
    elif user_act == "f":
        try:
            with open("record.txt", "r") as y:
                whole_log = json.load(y)
            # rich.print(whole_log)
            print(json.dumps(whole_log, indent=2))
        except (FileNotFoundError, SyntaxError, json.JSONDecodeError):
            print("No valid records found. Please log a day first.")
    elif user_act == "g":
        break
    else:
        print("Sorry, response not valid, type either: a, b, c,d, e or f")
        continue

    while True:
        to_continue = input("Would you like to perform another operation?: carefully answer yes/no: ").lower().strip()
        if to_continue == "yes":
            cycle = True
            break
        elif to_continue == "no":
            cycle = False
            break
        else:
            print("Response not valid, please enter yes/no: ")
            continue
try:
    with open("record.txt", "r") as h:
        check = json.load(h)
    if len(check) >= 30:
        ask = input(f"You have {len(check)} entries already, would you like to check monthly expense? yes/no: ").lower().strip().replace(" ", "")
        if ask == "yes":
            monthly_cost, monthly_purchase, avg_day_spend, month_year = monthly_expenses()
            print(f"Your monthly expenses summed up to ₦{monthly_cost:,} "
                  f"with an average daily spend of ₦{avg_day_spend:,}. What you spent money on during "
                  f"the course of this period are: {monthly_purchase}")
            try:
                with open("monthly_data_storage.json", "r") as i:
                    monthly_data = json.load(i)
            except (FileNotFoundError, ValueError, SyntaxError, json.JSONDecodeError):
                monthly_data = {
                    month_year: {
                        "monthly_total_spent": monthly_cost,
                        "monthly_total_items": monthly_purchase
                    }
                }
                with open("monthly_data_storage.json", "w") as i:
                    json.dump(monthly_data, i, indent=4)
                    with open("record.txt", "w") as f:
                        json.dump([], f)
                    with open("days_logged.txt", "w") as k:
                        json.dump([], k)
            else:
                monthly_saved_data = {
                    month_year: {
                        "monthly_total_spent": monthly_cost,
                        "monthly_total_items": monthly_purchase
                    }
                }
                monthly_data.update(monthly_saved_data)
                with open("monthly_data_storage.json", "w") as i:
                    json.dump(monthly_data, i, indent=4)
                with open("record.txt", "w") as f:
                    json.dump([], f)
                with open("days_logged.txt", "w") as k:
                    json.dump([], k)
except (FileNotFoundError, ValueError, SyntaxError, json.JSONDecodeError):
    print("No data logged yet")
print("End of program.", end="")

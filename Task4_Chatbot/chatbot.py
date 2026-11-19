# Multi Intent Rule Based Chatbot
# A terminal chatbot with menus ( Orders, Billing, Tech Support), session state,
# text normalization, global commands and fallback handling.

import re

#---text normalization---
def clean(text):
    #lowercase the text and remove punctuation and extra spaces.
    return re.sub(r"[^a-z0-9 ]","",text.lower()).strip()

# ----session state   
session={"state":"main",  # which menu the user in
         "name":"",       # the user's name
         "fails":0,       # consecutive fallback replies
         "messages":0}    # nuumber of messages the user sent

#---Menu texts---
MAIN_MENU = ("\n1. Orders\n2. Billing\n3. Tech Support\nType menu, help, or agent anytime.")

ORDERS_MENU="Orders: track, cancle or return. Type back for thr main menu."
BILLING_MENU = "Billing: invoice, payment or refund. Type back for the main menu."
TECH_MENU= "Tech Support: password, app crash or contact an agent. Type back for the main menu."

# State name -> its menu text ( used by the help command)
MENUS={"main":MAIN_MENU,"orders":ORDERS_MENU,"billing":BILLING_MENU, "tech":TECH_MENU}

# -------Handlers ( one function per state)
def orders_menu(text):
    words=text.split()
    if "back" in words or "menu" in words:
        session["state"]="main"
        return MAIN_MENU
    elif "track" in words or "where" in words or "status" in words:
        return "your order is on the way and should arrive in 2 to 3 days"
    elif "cancle" in words:
        return " you can only cancle your order in next 30 mintues."
    elif "return" in words or "refund" in words:
        return "return policy available in 7 days"
    else:
        return "Sorry i did not get that." +ORDERS_MENU

def billing_menu(text):
     words=text.split()
     if "back" in words or "menu" in words:
          session["state"]="main"
          return MAIN_MENU
     elif "invoice" in words or "bill" in words:
          return "we are pleased to hear your concern"
     elif "payment" in words or "pay" in words:
          return "pay on choice"
     elif "refund" in words:
          return "plz Wait for 5 to 7 woring days"
     else:
          return "Sorry, I did not get that." + BILLING_MENU

def tech_menu(text):
     words=text.split()
     if "back" in words or "menu" in words:
               session["state"]="main"
               return MAIN_MENU
     elif "password" in words or "login" in words:
               return "password reset"
     elif "crash" in words or "error" in words or "bug" in words:
               return "Restart your app"
     elif "agent" in words or "contact" in words:
               return "plz call on helpline 0123.Or text on 1234567"
     else:
               return "Sorry, I did not get that." + TECH_MENU

def main_menu(text):
    words=text.split()
    if text=="1" or "order" in words or "orders" in words:
        session["state"]="orders"
        return ORDERS_MENU
    elif text=="2" or "bill" in words or "billing" in words or "payment" in words:
        session["state"]="billing"
        return BILLING_MENU
    elif text=="3" or "tech" in words or "support" in words:
        session["state"]="tech"
        return TECH_MENU
    else:
        return "Sorry, I did not understand. "+ MAIN_MENU

# Function dictionary: routes the user's input to the handler of the current state
handlers= {"main":main_menu,"orders":orders_menu,"billing":billing_menu, "tech":tech_menu}

#----- Start of the conversation
session["name"]=input("Bot: Hi! What is your name? ").strip()
print(f"How can I help you today? {session['name']}")
print("Bot: ", MAIN_MENU)

#----Main loop----
while True:
    user=clean(input(("You: ")))
    words=user.split()

    # Empty input
    if user=="":
         print("Bot: Please type something.")
         continue

    # Exit command
    if user in ("bye","exit","quit"):
            print(f"goodbye {session['name']}! Have a nice day.")
            break

    session["messages"] += 1

    # Global commands work in every state, small talk comes next
    if user== "menu":
         session["state"]="main"
         reply= MAIN_MENU
    elif user== "help":
         reply="Options: " + MENUS[session["state"]]
    elif user == "agent":
         reply= "Connecting you to a human agent. Please email support@example.com or call 123 456."
    elif set(words) & {"hello", "hi", "hey"}:
         reply = f"Hello {session['name']}! How can i help?"
    elif set(words) & {"thanks", "thank", "thanku", "thank you"}:
         reply = "you are welcome! Anything else?"
    else:
        # Route to the handler of the current state
         reply=handlers[session["state"]](user)

    # Fallback counter: count replies that start with "Sorry"
    if reply.startswith("Sorry"):
         session["fails"] += 1
    else:
         session["fails"] = 0

    # After 3 failed replies in a row, suggest help and go back to the main menu
    if session["fails"] >= 3:
         reply += "\nIt seems I am not helping. Type 'agent' to contact a human, or 'menu' to start again."
         session["fails"]=0
         session["state"]="main"

    print(f"Bot [{session['state']}]:", reply)
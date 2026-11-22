# Multi Intent Rule Based Chatbot
# A terminal chatbot with menus (Orders, Billing, Tech Support), session state,
# text normalization, global commands and fallback handling.

import re


# ---- Text normalization ----
def clean(text):
    # Lowercase the text and remove punctuation and extra spaces.
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()


# ---- Session state ----
session = {
    "state": "main",   # which menu the user is in
    "name": "",        # the user's name
    "fails": 0,        # consecutive fallback replies
    "messages": 0,     # number of messages the user sent
}

# ---- Menu texts ----
MAIN_MENU = "\n1. Orders\n2. Billing\n3. Tech Support\nType menu, help, or agent anytime."

ORDERS_MENU = "Orders: track, cancel or return. Type back for the main menu."
BILLING_MENU = "Billing: invoice, payment or refund. Type back for the main menu."
TECH_MENU = "Tech Support: password, app crash or contact an agent. Type back for the main menu."

# State name -> its menu text (used by the help command)
MENUS = {"main": MAIN_MENU, "orders": ORDERS_MENU, "billing": BILLING_MENU, "tech": TECH_MENU}


# ---- Handlers (one function per state) ----
def orders_menu(text):
    words = text.split()
    if "back" in words or "menu" in words:
        session["state"] = "main"
        return MAIN_MENU
    elif "track" in words or "where" in words or "status" in words:
        return "Your order is on the way and should arrive in 2 to 3 days."
    elif "cancel" in words or "cancle" in words:
        return "You can only cancel your order within 30 minutes."
    elif "return" in words or "refund" in words:
        return "Our return policy allows returns within 7 days."
    else:
        return "Sorry, I did not get that. " + ORDERS_MENU


def billing_menu(text):
    words = text.split()
    if "back" in words or "menu" in words:
        session["state"] = "main"
        return MAIN_MENU
    elif "invoice" in words or "bill" in words:
        return "We are pleased to hear your concern."
    elif "payment" in words or "pay" in words:
        return "You can pay by the method of your choice."
    elif "refund" in words:
        return "Please wait for 5 to 7 working days."
    else:
        return "Sorry, I did not get that. " + BILLING_MENU


def tech_menu(text):
    words = text.split()
    if "back" in words or "menu" in words:
        session["state"] = "main"
        return MAIN_MENU
    elif "password" in words or "login" in words:
        return "Use the Forgot Password link on the login page to reset your password."
    elif "crash" in words or "error" in words or "bug" in words:
        return "Please restart your app."
    elif "agent" in words or "contact" in words:
        return "Please call the helpline on 0123 or text 1234567."
    else:
        return "Sorry, I did not get that. " + TECH_MENU


def main_menu(text):
    words = text.split()
    if text == "1" or "order" in words or "orders" in words:
        session["state"] = "orders"
        return ORDERS_MENU
    elif text == "2" or "bill" in words or "billing" in words or "payment" in words:
        session["state"] = "billing"
        return BILLING_MENU
    elif text == "3" or "tech" in words or "support" in words:
        session["state"] = "tech"
        return TECH_MENU
    else:
        return "Sorry, I did not understand. " + MAIN_MENU


# Function dictionary: routes the user's input to the handler of the current state
handlers = {"main": main_menu, "orders": orders_menu, "billing": billing_menu, "tech": tech_menu}

# ---- Start of the conversation ----
session["name"] = input("Bot: Hi! What is your name? ").strip()
print(f"Bot: Hi {session['name']}! How can I help you today?")
print("Bot:", MAIN_MENU)

# ---- Main loop ----
while True:
    user = clean(input("You: "))
    words = user.split()

    # Empty input
    if user == "":
        print("Bot: Please type something.")
        continue

    # Exit command
    if user in ("bye", "exit", "quit"):
        print(f"Bot: Goodbye {session['name']}! You sent {session['messages']} messages. Have a nice day.")
        break

    session["messages"] += 1

    # Global commands work in every state, small talk comes next
    if user == "menu":
        session["state"] = "main"
        reply = MAIN_MENU
    elif user == "help":
        reply = "Options: " + MENUS[session["state"]]
    elif user == "agent":
        reply = "Connecting you to a human agent. Please email support@example.com or call 123 456."
    elif set(words) & {"hello", "hi", "hey"}:
        reply = f"Hello {session['name']}! How can I help?"
    elif set(words) & {"thanks", "thank", "thanku"}:
        reply = "You are welcome! Anything else?"
    else:
        # Route to the handler of the current state
        reply = handlers[session["state"]](user)

    # Fallback counter: count replies that start with "Sorry"
    if reply.startswith("Sorry"):
        session["fails"] += 1
    else:
        session["fails"] = 0

    # After 3 failed replies in a row, suggest help and go back to the main menu
    if session["fails"] >= 3:
        reply += ("\nIt seems I am not helping. Type 'agent' to contact a human, "
                  "or 'menu' to start again.")
        session["fails"] = 0
        session["state"] = "main"

    print(f"Bot [{session['state']}]:", reply)
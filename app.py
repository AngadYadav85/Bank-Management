import json
import random
import string
from pathlib import Path
import streamlit as st

DATABASE_PATH = "database.json"


# -------------- Data layer --------------
def load_data():
    if Path(DATABASE_PATH).exists():
        try:
            return json.loads(Path(DATABASE_PATH).read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
    return []


def save_data(data):
    Path(DATABASE_PATH).write_text(json.dumps(data, indent=2), encoding="utf-8")


def account_generate():
    # 8 letters + 4 digits, then shuffled, like your original
    alpha = random.choices(string.ascii_letters, k=8)
    num = random.choices(string.digits, k=4)
    acc = alpha + num
    random.shuffle(acc)
    return "".join(acc)


# -------------- Utility --------------
def find_user(data, accno, pin):
    # Return the user dict if match is found, else None
    for u in data:
        if str(u.get("AccountNo")) == str(accno) and str(u.get("pin")) == str(pin):
            return u
    return None


def ensure_state():
    if "data" not in st.session_state:
        st.session_state.data = load_data()


def refresh_persist():
    save_data(st.session_state.data)


# -------------- UI Components --------------
def ui_create_user():
    st.header("Create Account")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, step=1)
        email = st.text_input("Email")

    with col2:
        use_auto_acc = st.checkbox("Auto-generate Account Number", value=True)
        if use_auto_acc:
            account_no = account_generate()
            st.text_input("Account Number (auto)", value=account_no, disabled=True)
        else:
            account_no = st.text_input("Account Number")

        pin = st.text_input("PIN (4 digits)", type="password", max_chars=4)

    if st.button("Create"):
        # Validations per your rules
        if name.strip() == "" or email.strip() == "":
            st.error("Name and Email are required.")
            return
        try:
            age = int(age)
        except ValueError:
            st.error("Age must be a number.")
            return
        if age < 12:
            st.error("Sorry, you must be at least 12 to create an account.")
            return
        if not pin.isdigit() or len(pin) != 4:
            st.error("PIN must be exactly 4 digits.")
            return
        if not use_auto_acc and account_no.strip() == "":
            st.error("Please enter an account number or enable auto-generate.")
            return

        # Ensure unique account number
        exists = any(str(u.get("AccountNo")) == str(account_no) for u in st.session_state.data)
        if exists:
            st.error("Account number already exists. Try a different one or auto-generate.")
            return

        user = {
            "name": name.strip(),
            "age": age,
            "email": email.strip(),
            "AccountNo": str(account_no),
            "pin": str(pin),   # store as string for consistent matching
            "balance": 0
        }
        st.session_state.data.append(user)
        refresh_persist()
        st.success(f"Account created successfully. Account No: {account_no}")


def ui_deposit():
    st.header("Deposit Money")

    accno = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    amount = st.number_input("Amount to deposit", min_value=1, step=1)

    if st.button("Deposit"):
        user = find_user(st.session_state.data, accno, pin)
        if not user:
            st.error("No such user exists.")
            return
        user["balance"] = int(user.get("balance", 0)) + int(amount)
        refresh_persist()
        st.success(f"Deposit successful. New balance: {user['balance']}")


def ui_withdraw():
    st.header("Withdraw Money")

    accno = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    amount = st.number_input("Amount to withdraw", min_value=1, step=1)

    if st.button("Withdraw"):
        user = find_user(st.session_state.data, accno, pin)
        if not user:
            st.error("No such user exists.")
            return
        if int(amount) > int(user.get("balance", 0)):
            st.error("Insufficient balance.")
            return
        user["balance"] = int(user.get("balance", 0)) - int(amount)
        refresh_persist()
        st.success(f"Withdrawal successful. New balance: {user['balance']}")


def ui_show_details():
    st.header("Show Details")

    accno = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)

    if st.button("Fetch Details"):
        user = find_user(st.session_state.data, accno, pin)
        if not user:
            st.error("No data found.")
            return
        # Display user (mask PIN)
        safe_user = dict(user)
        safe_user["pin"] = "****"
        st.json(safe_user)


def ui_update_details():
    st.header("Update Details")

    st.caption("You cannot change balance, account number, or age.")

    accno = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)

    if "update_user" not in st.session_state:
        st.session_state.update_user = None

    if st.button("Load User"):
        user = find_user(st.session_state.data, accno, pin)
        if not user:
            st.error("No such user found.")
        else:
            st.session_state.update_user = user
            st.success("User loaded. Edit below.")

    if st.session_state.update_user:
        u = st.session_state.update_user
        # Show uneditable basics
        st.write(f"Account: {u['AccountNo']} | Age: {u['age']} | Balance: {u['balance']}")
        name = st.text_input("New name (leave blank to keep)", value=u["name"])
        email = st.text_input("New email (leave blank to keep)", value=u["email"])
        new_pin = st.text_input("New PIN (4 digits, leave blank to keep)", type="password")

        if st.button("Save Updates"):
            # Apply changes only if provided
            if name.strip():
                u["name"] = name.strip()
            if email.strip():
                u["email"] = email.strip()
            if new_pin.strip():
                if not new_pin.isdigit() or len(new_pin) != 4:
                    st.error("PIN must be exactly 4 digits.")
                    return
                u["pin"] = str(new_pin)
            refresh_persist()
            st.success("Details updated.")


def ui_delete_account():
    st.header("Delete Account")

    accno = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password", max_chars=4)
    confirm = st.checkbox("I understand this will permanently delete the account.")

    if st.button("Delete"):
        user = find_user(st.session_state.data, accno, pin)
        if not user:
            st.error("No such user found.")
            return
        if not confirm:
            st.warning("Please confirm deletion first.")
            return
        st.session_state.data.remove(user)
        refresh_persist()
        st.success("Account deleted.")


# -------------- Main App --------------
def main():
    st.set_page_config(page_title="Simple Bank", page_icon="🏦", layout="centered")
    st.title("🏦 Simple Bank")

    ensure_state()

    # Sidebar navigation
    page = st.sidebar.radio(
        "Go to",
        ["Create Account", "Deposit", "Withdraw", "Show Details", "Update Details", "Delete Account"]
    )

    if page == "Create Account":
        ui_create_user()
    elif page == "Deposit":
        ui_deposit()
    elif page == "Withdraw":
        ui_withdraw()
    elif page == "Show Details":
        ui_show_details()
    elif page == "Update Details":
        ui_update_details()
    elif page == "Delete Account":
        ui_delete_account()

    # Optional: show a small table of accounts (mask PINs)
    with st.expander("Admin view: all accounts (masked PIN)"):
        masked = []
        for u in st.session_state.data:
            masked.append({
                "name": u["name"],
                "age": u["age"],
                "email": u["email"],
                "AccountNo": u["AccountNo"],
                "pin": "****",
                "balance": u["balance"],
            })
        st.dataframe(masked, use_container_width=True)


if __name__ == "__main__":
    main()

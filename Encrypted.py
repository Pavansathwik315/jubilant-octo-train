import os
import json
from datetime import datetime
from cryptography.fernet import Fernet

# Key file to store encryption key
KEY_FILE = "secret.key"
NOTES_FILE = "notes.json"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt_note(note, key):
    f = Fernet(key)
    return f.encrypt(note.encode()).decode()

def decrypt_note(encrypted_note, key):
    f = Fernet(key)
    return f.decrypt(encrypted_note.encode()).decode()

def save_note():
    key = load_key()
    note = input("📝 Enter your note: ")
    encrypted = encrypt_note(note, key)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            notes = json.load(f)
    else:
        notes = []

    notes.append({"time": timestamp, "note": encrypted})

    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)
    print("✅ Note saved and encrypted!")

def read_notes():
    if not os.path.exists(NOTES_FILE):
        print("📂 No notes found.")
        return

    key = load_key()
    with open(NOTES_FILE, "r") as f:
        notes = json.load(f)

    print("\n🔓 Decrypted Notes:\n" + "-" * 30)
    for entry in notes:
        try:
            decrypted = decrypt_note(entry["note"], key)
            print(f"[{entry['time']}] {decrypted}")
        except:
            print(f"[{entry['time']}] 🔒 Unable to decrypt note (corrupted or wrong key)")
    print("-" * 30)

def main():
    print("=" * 40)
    print("🛡 Encrypted Notes CLI App")
    print("=" * 40)

    while True:
        print("\nChoose an option:")
        print("1. Write a note")
        print("2. Read notes")
        print("3. Exit")
        choice = input("➡ Enter choice (1/2/3): ").strip()

        if choice == '1':
            save_note()
        elif choice == '2':
            read_notes()
        elif choice == '3':
            print("👋 Exiting. Stay secure!")
            break
        else:
            print("⚠ Invalid choice. Try again.")

if _name_ == "_main_":
    main()
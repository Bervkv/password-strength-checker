import string
import math
import sys

def basic_checks(password: str) -> dict:
    results = {
        "length_ok": None,
        "has_upper": None,
        "has_lower": None,
        "has_digit": None,
        "has_symbol": None,
    }

    if (len(password) >= 12):
        results["length_ok"] = True
    else:
        results["length_ok"] = False


    has_upper = any(character.isupper() for character in password)


    has_lower = any(character.islower() for character in password)


    has_digit = any(character.isdigit() for character in password)
    
    has_symbol = False

    for character in password:
        if character in string.punctuation:
            has_symbol = True


    results["has_upper"] = has_upper
    results["has_lower"] = has_lower
    results["has_symbol"] = has_symbol
    results["has_digit"] = has_digit

    return results


def calculate_entropy(password: str) -> float:
    pool_size = 0
    if any(character.isupper() for character in password):
        pool_size += 26
    if any(character.islower() for character in password):
        pool_size+= 26
    if any(character.isdigit() for character in password):
        pool_size+=10
    if any(character in string.punctuation for character in password):
            pool_size += len(string.punctuation)

    if pool_size == 0:
        return 0.0
    
    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)

def load_common_passwords(filepath: str) -> set:
    common_passwords = set()
    with open(filepath) as f:
        for line in f:
            common_passwords.add(line.strip())
    
    return common_passwords

def is_common_password(password: str, common_passwords: set) -> bool:
    return password.lower() in common_passwords

def rate_password(password: str, common_passwords: set) -> dict:
    checks = basic_checks(password)
    entropy = calculate_entropy(password)
    is_common = is_common_password(password, common_passwords)

    if is_common:
        strength = "VERY WEAK (found in common password list!)"
    elif entropy < 28:
        strength = "WEAK"
    elif entropy < 36:
        strength = "MODERATE"
    elif entropy < 60:
        strength = "STRONG"
    else:
        strength = "VERY STRONG"

    return {
        "password_length": len(password),
        "checks": checks,
        "entropy_bits": entropy,
        "is_common_password": is_common,
        "strength": strength,
    }

def print_report(password: str, result: dict) -> None:
        print("\n--- Password Strength Report ---")
        print(f"Length: {result['password_length']}")
        print("Composition:")
        for check, passed in result["checks"].items():
            symbol = "✓" if passed else "✗"
            print(f"  [{symbol}] {check}")
        print(f"Estimated entropy: {result['entropy_bits']} bits")
        print(f"Found in common password list: {result['is_common_password']}")
        print(f"Overall strength: {result['strength']}")
        print("---------------------------------\n")


def main():
    common_passwords = load_common_passwords("common_passwords.txt")

    if len(sys.argv) > 1:
        # password passed as a command-line argument, e.g. python3 checker.py "mypassword"
        password = sys.argv[1]
        result = rate_password(password, common_passwords)
        print_report(password, result)
    else:
        # no argument given — run interactively instead
        print("Password Strength Checker (type 'quit' to exit)")
        while True:
            password = input("\nEnter a password to check: ")
            if password.lower() == "quit":
                break
            result = rate_password(password, common_passwords)
            print_report(password, result)


if __name__ == "__main__":
    main()
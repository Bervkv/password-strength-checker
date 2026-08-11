# Password Strength Checker

A command-line tool that evaluates password strength using two independent
methods because relying on just one gives a false sense of security.

## Why two checks, not one?

Most "password strength" tools only check composition rules (length,
uppercase, symbols). That's not enough: a password like `Password1!`
satisfies every rule a typical form enforces, but it's still one of the
first passwords a real attacker would try.

This tool combines:

1. **Entropy calculation** — estimates brute-force resistance mathematically,
   based on the character pool used and password length.
2. **Common password lookup** — checks the password (case-insensitively)
   against a list of the 10,000 most common leaked passwords, from
   [SecLists](https://github.com/danielmiessler/SecLists), because entropy
   math alone can't catch passwords that look random on paper but are
   actually well-known to attackers.

## What I learned building this

- Entropy math assumes characters were picked randomly — it *overestimates*
  security for human-chosen passwords, which is exactly why the wordlist
  check exists as a second, independent layer, not a replacement.
- Even a 10,000-entry wordlist misses passwords a larger list (like the
  14-million-entry rockyou.txt) would catch — no blocklist is ever
  complete, which is a real limitation of this whole category of defense,
  not just this tool.
- Debugging Python's `any()` + generator expression pattern taught me the
  difference between checking a whole string (`password.isupper()`) vs.
  checking each character individually — a distinction that matters a lot
  in security-adjacent code where "close enough" logic causes real bugs.

## Usage

```bash
# Interactive mode
python3 checker.py

# Or check a single password directly
python3 checker.py "your-password-here"
```

## Example output

```
--- Password Strength Report ---
Length: 8
Composition:
  [✗] length_ok
  [✗] has_upper
  [✓] has_lower
  [✗] has_digit
  [✗] has_symbol
Estimated entropy: 37.6 bits
Found in common password list: True
Overall strength: VERY WEAK (found in common password list!)
---------------------------------
```

## Next steps

- Swap the 10k wordlist for the larger rockyou.txt for more thorough checking
- Add a check for keyboard-walk patterns (`qwerty`, `1qaz2wsx`)
- Add a Levenshtein-distance check to catch near-misses of common passwords
  (e.g. `p@ssword` when `password` is in the list)

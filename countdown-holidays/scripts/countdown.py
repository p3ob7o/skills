#!/usr/bin/env python3
"""Calculate days until Halloween and New Year's Eve from today."""

from datetime import date


def days_until(target_month: int, target_day: int) -> tuple[int, int]:
    """Return (days_remaining, target_year) for the next occurrence of a date."""
    today = date.today()
    target = date(today.year, target_month, target_day)
    if target < today:
        target = date(today.year + 1, target_month, target_day)
    return (target - today).days, target.year


def main():
    halloween_days, halloween_year = days_until(10, 31)
    nye_days, nye_year = days_until(12, 31)

    print(f"Today is {date.today().strftime('%B %d, %Y')}.")
    print()

    if halloween_days == 0:
        print("It's Halloween today!")
    else:
        print(f"Days until Halloween ({halloween_year}): {halloween_days}")

    if nye_days == 0:
        print("It's New Year's Eve today!")
    else:
        print(f"Days until New Year's Eve ({nye_year}): {nye_days}")


if __name__ == "__main__":
    main()

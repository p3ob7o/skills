---
name: countdown-holidays
description: "Calculate and display the number of days remaining until Halloween (October 31) and New Year's Eve (December 31). This skill should be used when the user asks how many days until Halloween or New Year's Eve, or asks for a holiday countdown. Triggers: days until Halloween, days until New Year's, holiday countdown, when is Halloween, when is New Year's Eve, countdown."
---

# Countdown to Holidays

Display the number of days from today until Halloween (Oct 31) and New Year's Eve (Dec 31).

## Usage

Run the countdown script to get today's date and the days remaining:

```bash
python3 scripts/countdown.py
```

The script automatically handles the case where a holiday has already passed this year by counting to the next year's occurrence. If today is the holiday itself, it announces that instead of showing a countdown.

Present the output to the user as-is.

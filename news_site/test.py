from datetime import datetime

# Get the current date and time
now = datetime.now()

# Print the current date and time
print("Current date and time:", now)

# If you want to format the date and time, you can use strftime
formatted_now = now.strftime("%Y-%m-%d %I:%M:%S %p")
print("Formatted date and time:", formatted_now)


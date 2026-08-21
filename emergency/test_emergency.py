import time

from emergency_handler import EmergencyHandler


handler = EmergencyHandler(cooldown_seconds=3)


print("First HELP:")
print(handler.process("HELP"))

print("\nImmediate HELP:")
print(handler.process("HELP"))

print("\nWaiting 3 seconds...")
time.sleep(3)

print("\nHELP after cooldown:")
print(handler.process("HELP"))

print("\nHELLO:")
print(handler.process("HELLO"))
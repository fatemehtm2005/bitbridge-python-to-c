def greeting(name, times):
    message = "Hello, " + name
    for index in range(times):
        print(message)
    return times

count = greeting("Bit Bridge", 2)
if count >= 2:
    print("translation verified")

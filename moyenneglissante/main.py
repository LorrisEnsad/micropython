while True:
    lightval = light.read()
    buffer.pop(0)
    buffer.append(lightval)
    summ = 0
    for i in range(MAX):
        summ+=buffer[i]
    average = summ/MAX
    print(average)
    time.sleep(0.1)
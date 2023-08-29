import time
import llwpbAPI

api=llwpbAPI.API("model")

while True:
    prompt=input("Prompt: ")

    ps=""
    for w in api.generate(prompt, 10).split(" "):
        ps+=w+" "
        time.sleep(0.2)
        print(ps, end="\r")
    print("\n")
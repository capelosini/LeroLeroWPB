# import time
import llwpbAPI

api=llwpbAPI.API("Models/LOTR_PTBR_model")

while True:
    prompt=input("Prompt: ")

    # ps=""

    genText=api.generate(prompt, 10)

    print(genText+"\n")

    # for w in genText.split(" "):
    #     ps+=w+" "
    #     time.sleep(0.2)
    #     print(ps, end="\r")
    # print("\n")
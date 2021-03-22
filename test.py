import termcolor2
import colorama
colorama.init()

myText = input("Type a text : ")
color = input("What color you want? : ")

print(termcolor2.colored(myText, color))
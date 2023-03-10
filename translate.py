def iscapital(string):
    if not string: return False
    return string[0].isupper()
def join(arr, x, seps=False):
    res = arr[0]
    for j, i in enumerate(arr[1:]):
        y = x
        if seps:
            y = x[j]
        res += y + i
    return res
def split_array(string, arr):
    seps = []
    words = []
    word = ""
    for i, char in enumerate(string):
        if char in arr:
            seps.append(char)
            words.append(word)
            word = ""
        else: word += char
        if i == len(string)-1:
            words.append(word)
    return words, seps

olutonq = {}
ukrainian = {}

words_str = open("words.txt", "r", encoding="utf-8").read()

for line in words_str.split("\n"):
    word, translate = line.split(" - ")
    olutonq[word.lower()] = translate.lower().split("/")
    for tr in translate.lower().split("/"):
        ukrainian[tr] = word.lower()

# from pprint import pprint

# pprint(olutonq)
# #pprint(olutonq, sort_dicts = False)
# print()
# print(len(olutonq))
# print()

def translate(text):
    results = []

    text_words, seps = split_array(text, [" ", "\n", ",", ".", "!", "?", ":", ";", "+", "-", "*", "/", "\\", "#", "@", "_", "(", ")", "$", "&", "[", "]", "{", "}", "%", "|", "`", "~", "•", "√", "π", "÷", "×", "¶", "∆", "£", "€", "¢", "^", "°", "=", "©", "®", "™", "℅", "'", '"', "<", ">"])
    if text.lower() in olutonq:
        wordt = olutonq[text.lower()]
        return " / ".join(wordt)   
    while len(text_words):
        for i in range(len(text_words), 0, -1):
            c = join(text_words[:i], seps[:i-1], True)
            wordt = c.lower()
            if wordt in olutonq:
                wordt = olutonq[wordt][0]
                break
            elif wordt in ukrainian:
                wordt = ukrainian[wordt]
                break

        if c.isupper():
            wordt = wordt.upper()
        elif iscapital(c):
            wordt = wordt.capitalize()

        results.append(wordt)

        for j in range(i):
            text_words.pop(0)
    return " " + join(results, seps, 1)

if __name__ == "__main__":
    while 1:
        print(translate(input(" ")))
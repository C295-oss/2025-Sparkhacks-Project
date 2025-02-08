def parse(text: str):
    parsedInfo = dict()
    print("text is ready")

    for line in text:
        match line:
            case "/# ":
                _,_,rest = text.partition("/# ")
                parsedInfo["/#"] = rest

            case "/## ":
                _,_,rest = text.partition("/## ")
                parsedInfo["/##"] = rest

            case "/### ":
                _,_,rest = text.partition("/### ")
                parsedInfo["/###"] = rest

            case "/p ":
                _,_,rest = text.partition("/p ")
                parsedInfo["/p"] = rest

            case "/img ":
                _,_,rest = text.partition("/img ")
                parsedInfo["/img"] = rest

            case "/a ":
                _,_,rest = text.partition("/a ")
                parsedInfo["/a"] = rest

            case "/br ":
                _,_,rest = text.partition("/br ")
                parsedInfo["/br"] = rest

            case "/--- ":
                parsedInfo["/---"] = "/---"

            case "!background_color ":
                _,_,rest = text.partition("!background_color ")
                parsedInfo["!background_color"] = rest

            case "!font-color ":
                _,_,rest = text.partition("!font-color ")
                parsedInfo["!font-color"] = rest       

            case _:
                print("Something wrong with code...")
    

    for first, second in parsedInfo:
        print(f"{first} : {second}")

    return parsedInfo

from bot.chatbot import Chatbot
from bot.disposition import Disposition

if __name__ == "__main__":

    profile = {
        "NAME": "Vicky",
        "GENDER": "女",
        "YEAROFBIRTH": "1995",
        "MONTHOFBIRTH": "10",
        "DAYOFBIRTH": "10",
        "DESCRIBE": ["身材纤细高挑性感"]
    }

    chatbot = Chatbot(profile, Disposition.COLD)
    user = "Human"
    history_list = []
    input_txt = input( user + ": " )
    while input_txt != "exit":
        input_item = {
            "speaker" : user,
            "content" : input_txt
        }
        output = chatbot.chat(input_item, history_list)
        history_list.append(input_item)
        history_list.append(output)
        print( output["speaker"] + "：" + output["content"] )
        input_txt = input( user + ": " )

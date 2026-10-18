from chatbot import offline_reply


def test_greeting():
    reply = offline_reply("hello")
    assert "Hello" in reply


def test_python_question():
    reply = offline_reply("Explain Python")
    assert "Python" in reply


def test_assistant_name():
    reply = offline_reply("What is your name?")
    assert "AI Chatbot Assistant" in reply


def test_unknown_question():
    reply = offline_reply("Something unusual")
    assert "offline demo mode" in reply
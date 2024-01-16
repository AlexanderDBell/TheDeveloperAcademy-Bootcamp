import textwrap

def request_word(part_of_speech: str) -> str:
    if part_of_speech[0].lower() in ['a','e','i','o','u']:
        article = 'an'
    else:
        article = 'a'
    word = input(f'Please enter {article} {part_of_speech}. ')
    return word

script = f"Today every student has a computer small enough to fit into his {request_word('noun')}. He can solve any math problem simply by pushing the computer's little {request_word('plural noun')}. Computer's can add, multiply, divide, and {request_word('verb (present tense)')}. They can also {request_word('verb (present tense)')} better than a human. Some computers are {request_word('part of body (plural)')}. Others have a/an {request_word('adjective')} screen that shows all kinds of {request_word('plural noun')} and {request_word('adjective')} figures."

print(textwrap.fill(script, 72))
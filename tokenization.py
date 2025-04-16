import tiktoken

encoder = tiktoken.encoding_for_model('gpt-4o')

print("Vocab Size",encoder.n_vocab) #200019

text = "The cat sat on the mat."
tokens = encoder.encode(text)

print("Tokens:", tokens) #  [976, 9059, 10139, 402, 290, 2450, 13]

my_tokens =  [976, 9059, 10139, 402, 290, 2450, 13]
decoded = encoder.decode([976, 9059, 10139, 402, 290, 2450, 13])
print(decoded)
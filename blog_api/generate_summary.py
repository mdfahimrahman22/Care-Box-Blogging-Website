import re


def summarize_text(text):
    sentences = re.split('[.!?]', text)
    firstFewSentences = '. '.join(sentences[:3])
    word_list = text.split()
    numOfWords = len(word_list)
    return numOfWords, firstFewSentences

# summarize_text('''Before you start writing your blog post, make sure you have a clear understanding of your target audience. To do so, take the following steps. To discover your audience, ask questions like: Who are they? Are they like me, or do I know someone like them? What do they want to know about? What will resonate with them?''')

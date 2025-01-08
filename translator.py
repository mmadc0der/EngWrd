import asyncio
from googletrans import Translator

async def translate(word: str) -> dict:
    '''
    Translates any word or phrase and autodetects language
    '''
    translator = Translator()
    
    # Detect the language of the input word
    detected = await translator.detect(word)  # Use await here
    src_lang = detected.lang
    
    # Determine target language based on source language
    if src_lang == 'en':
        target_lang = 'ru'
    elif src_lang == 'ru':
        target_lang = 'en'
    else:
        return "Unsupported language. Please enter English or Russian."

    # Translate the word
    translation = await translator.translate(word, src=src_lang, dest=target_lang)
    
    return {
        "original": word,
        "detected_language": src_lang,
        "translated_word": translation.text,
        "possible_mistakes": translation.extra_data['possible-mistakes'][1] if translation.extra_data['possible-mistakes'] else None, 
        "meaning": translation.extra_data['definitions'][0][1][0][0] if translation.extra_data['definitions'] else None
    }

# Example usage in an async context
async def main():
    word_to_translate = input("Enter a word in English or Russian: ")
    result = await translate(word_to_translate)  # Use await here

    print(f"Original Word: {result['original']}")
    print(f"Detected Language: {result['detected_language']}")
    print(f"Translated Word: {result['translated_word']}")
    if result['meaning']:
        print(f"Meaning: {result['meaning']}")
    if result['possible_mistakes']:
        print('Possible mistakes:', result['possible_mistakes'])

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())

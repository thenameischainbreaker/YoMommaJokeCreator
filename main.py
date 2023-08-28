# INF360 - Programming in Python
# John Lewis
# Final Project
"""
This is a OpenAI joke generator that generates Yo Momma jokes using prompt injection.
There is a read and rate function as well as a joke generate function.
Generated jokes are stored in a jokes.txt in the same directory as the main module.
Do not make changes to jokes.txt directly.
"""



import json
import random
import pprint
#import pip
import hashlib
import openai
import logging
import sys
import traceback

def main():
    #intro
    try:
        open('jokes.txt', 'a').close()
        if "--debug" in sys.argv:
            logging.basicConfig(level=logging.DEBUG)
        input("Welcome to the Yo Momma joke creator, powered by ChatGPT.")
        input("One of the tests of a real AI should be to make real humans laugh.")
        input("I need your help reading and creating new jokes.")
        input("Together let's find out the hidden power of ChatGPT.")
        selector()
    except UnboundLocalError as e:
        logging.critical(f"Exception type: {type(e).__name__}")
        logging.critical(f"Exception message: {str(e)}")
        logging.critical("This error is due to openai installing the first time.\nPress any key to go to main menu.")
        selector()
    except Exception as e:
    # blanket exception handling and restart the program
        logging.critical(f"Exception type: {type(e).__name__}")
        logging.critical(f"Exception message: {str(e)}")
        logging.critical("Press any key to restart the program.")
        traceback.print_exc()
        selector()
    
    


def selector(option=0):
    while(True):
        print("Select from one of the following options:")
        print("Option 1: Read/Rate Jokes")
        print("Option 2: Generate new Jokes")
        print("Option 3: Exit Program")
        option = input("Type 1 for option 1, 2 for option 2, 3 for option 3.")
        if option == '1':
            reader()
            logging.debug('reader function returned.')
        elif option == '2':
            creator()
            logging.debug('creator function returned.')
        elif option == '3':
            logging.debug('Program shutting down.')
            break
        else:
            continue
        
#function for read/rate function of program   
def reader():    
    print("Help to rate ChatGPT jokes, but please go easy on in since it\nis not a professional comedian.")
    print("When presented a joke first say whether it makes semantical sense,\nor if the butt of the joke makes sense given the setup.")
    print("You can keep going until you exit, or have selected all of the jokes in the pool.")
    #open('jokes.txt', 'a').close()
    with open('jokes.txt','r') as file:
        json_string = file.read()
        

        if json_string:
            json_unrated_jokes = json.loads(json_string)
        else:
            json_unrated_jokes = []

    #json_unrated_jokes = json.loads(json_string)
    json_rated_jokes = []
    answer =  input("Do you want another joke? yes/no ")
    while(answer == 'yes'):
        #if no more jokes left break loop
        if len(json_unrated_jokes) == 0:
           print('You read/rated all the jokes!')
           input()
           break
        # generate a random index
        random_index = random.randrange(len(json_unrated_jokes))
        #get a random joke
        popped_value = json_unrated_jokes.pop(random_index)
        #print the subject
        print('Subject: ' + popped_value['subject'])
        #print the joke content
        print('ChatGPT: ' + str(popped_value['text']))
        #rate the joke
        print('Now rate the joke.')
        rating = -1
        while(rating < 0 or rating >3):      
            print('Rate the joke a 0 if the joke makes no semantic sense or there are obvious errors.')
            print('Rate the joke a 1 if the joke is not funny but at least makes sense.')
            print('Rate the joke a 2 if the joke is mildly amusing.')
            print('Rate the joke a 3 if the joke is genuinely funny.')
            try:
                rating = int(input('Would rate this joke a 0,1,2 or 3? '))   
            except():
                input('Invalid input or something went wrong.')
                rating = -1
                
        popped_value['rating'] =  rating     
        json_rated_jokes.append(popped_value)      

        answer =  input("Do you want another joke? yes/no ")
    #combine the two lists and write to file, with unrated jokes first    
    combined_list = json_unrated_jokes + json_rated_jokes
    #open('jokes.txt', 'a').close()
    with open("jokes.txt", "w") as file:
        json.dump(combined_list,file, indent=4)
    #return to main menu
    return
#function for joke generation portion of program    
def creator():
    #import openai package if installed, if not present install
    try:
        import openai
    except ImportError:
    # Install openai package if not installed
     #   pip.main(['install', 'openai'])
        logging.critical('Try installing openai module using\npip install package-name to use this feature.')
    except Exception as e:
        logging.critical(e)
        logging.critical('Error importing openai package. Try installing openai module using\npip install package-name to use this feature.')
        return
        
    
    #burner api key
    burner_api_key = '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'
    #set api key
    openai.api_key = burner_api_key
    #generate joke list
    generated_jokes = []
    #generator instructions
    print('The joke generator uses a burner API key to make requests.')
    print('Use the joke generator to help give subject ideas for a ChatGPT joke.')
    print('Unfortuately OpenAI has blocked the ability of ChatGPT to make jokes,\nand particularly "Yo Momma" jokes.')
    print('This tool uses prompt injection to create a "Yo Momma" joke, which\nwill generally work, unless the subject is offensive in itself.')
    print('ChatGPT can still produce some offensive content in this mode, so if\nthe content is offensive, type "yes" to delete the joke.')
    print('Answering "yes" to "make the joke petty" may improve the chances of a good joke.')
    print('When you exit, changes will be automatically saved.')
    make_another_joke = input('Generate another joke? yes/no ')
    while(make_another_joke == 'yes'):
       
        #ask for subject
        subject = input('Input a subject to help ChatGPT make a joke, such as Chinese restaurant.')
        #petty joke
        make_petty = input('Make the joke petty? yes/no ')
        #ternary statement
        petty_text = 'petty' if make_petty == 'yes' else ''

        #generate http request
        prompt=f"Write a {petty_text} {subject} joke in the style of the Yo Momma show using AAVE"
        response = openai.ChatCompletion.create(
        #response = openai.Completion.create(    
        #model="text-davinci-003",
        model="gpt-4",    
        #prompt=f"Write a {petty_text} {subject} joke in the style of the Yo Momma show using AAVE",
        messages=[{"role": "user", "content": f"{prompt}"}],
        temperature=0.71,
        max_tokens=256,
        top_p=1,
        #best_of=5,
        frequency_penalty=0.46,
        presence_penalty=1.42
        )

        #get joke text from response
        joke_text = response['choices'][0]['message']['content']
        #joke_text = resopnse['choices'][0]['text']
        joke_text = joke_text.replace("\n", "")
        input('ChatGPT: ' + joke_text)
        #Did ChatGPT create a joke
        did_chatgpt_create_a_joke = input('Did ChatGPT create a joke? yes/no')
        if did_chatgpt_create_a_joke != 'yes':
            continue
        #Was joke offensive
        offensive = input('Is the joke offensive? yes/no')
        if offensive == 'yes':
            continue
        #create new json object
        new_joke_json = {
        "id": None,
        "text": None,
        "rating": None,
        "subject": None
        }
        #create hash id of response
        my_hash = hashlib.md5()
        my_hash.update(joke_text.encode('utf-8'))
        new_joke_hash = my_hash.hexdigest()
        #set values of new json object and append to generated jokes array
        new_joke_json["id"] = new_joke_hash
        new_joke_json["text"] = joke_text
        new_joke_json["subject"] = subject
        generated_jokes.append(new_joke_json)
        make_another_joke = input('Generate another joke? yes/no ')
    print('Saving changes...')

    #overwrite jokes.txt with appended new jokes
    #open('jokes.txt', 'a').close()
    with open('jokes.txt','r') as file:
        json_string = file.read()

        if json_string:
            json_stored_jokes = json.loads(json_string)
        else:
            json_stored_jokes = []
    #json_stored_jokes = json.loads(json_string)
    combined_list = generated_jokes + json_stored_jokes

    
    with open("jokes.txt", "w") as file:
        json.dump(combined_list,file, indent=4)
    input('Changes saved!')
    #return to main menu
    return

    
    
    
        

        
        
    
    



main()
    

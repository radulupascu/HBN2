import openai
import pandas as pd
import multiprocessing

def generate_features_csv(start_index, finish_index):
    openai.api_key = 'sk-proj-HnFAJvvZM1tTuvNvzD1aT3BlbkFJRoEm33ygzFPeafn0OjNd'

    messages = [ {"role": "system", "content":  
                "I will give you a bunch of urls to products and/or services. For every link I send you, I need you to reply only it's UNSPSC segment (8 digits), it's segment name, it's UNSPSC family (8 digits), it's family name, it's UNSPSC class (8 digits), it's class name, it's commodity code (8 digits) and it's commodity name. Reply in this format: (segment, segment name, family, family name, class, class name, commodity, commodity name). Please only provide answers in this format, or output \"(None, None, None, None, None, None, None, None)\" if you can't find anything, but please try your best not to come up with nothing."
}]
    
    df = pd.read_csv('./url_product_extraction_input_dataset.csv')
    
    nr = 0
    lista = []

    for link in df.iloc[start_index:finish_index, 0]:
        message = link
        if message: 
            messages.append( 
                {"role": "user", "content": message}, 
            ) 
            chat = openai.ChatCompletion.create( 
                model="gpt-4", messages=messages 
            ) 
        reply = chat.choices[0].message.content 
        #print(reply)
        lista.append(reply.strip('()').split(','))
        messages.append({"role": "assistant", "content": reply}) 
        nr += 1
        print(str(nr) + "/" + str(finish_index - start_index) + " samples generated.")
    
    csv_file = pd.DataFrame(columns=["segment", "segment name", "family" , "family name" ,"class", "class name" ,"commodity", "commodity name"])
    new_df = pd.DataFrame(lista, columns=csv_file.columns)
    csv_file = pd.concat([csv_file, new_df], ignore_index=True)
    csv_file.to_csv("./train_dataset.csv", mode='a', header=False, index=False)

if __name__ == "__main__":
    # noWorkers = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(noWorkers)
    # for i in range(0, 1000, 20):
    #     pool.apply_async(func=generate_features_csv, args=(i, i+20))

    # pool.close()
    # pool.join()
    generate_features_csv(0, 10)
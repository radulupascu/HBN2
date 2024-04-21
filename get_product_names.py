import ollama
import pandas as pd
import multiprocessing
import time

pre_prompt = "Please analyze the provided URL and predict the product or service name it leads to. If you cannot identify the product or service, please respond with \"None\". I need you to respond only with your best guess, or just say \"None\" if you can't decide. Please do not reply with any additional words. Try to match your responses as closely as possible to the words in the URL. For each URL, I need your response on a newline. Do not echo the input you get."

modelfile = """
FROM llama3
PARAMETER temperature 0.08
PARAMETER num_ctx 1024
PARAMETER repeat_last_n 0
PARAMETER seed 1
SYSTEM {pre_prompt}
""".format(pre_prompt=pre_prompt)

ollama.create(model="llama3", modelfile=modelfile)

messages = [
  {
    'role': 'system',
    'content': pre_prompt,
  },
]

batch_size = 3

def get_product_names(start_index):

  

  df = pd.read_csv('./url_product_extraction_input_dataset.csv')
      
  lista = []
  for link in df.iloc[start_index:start_index + batch_size, 0]:
    lista.append(link)
  #print(lista)
      
  user_input = '\n'.join(lista)

  messages.append(
      {
          'role': 'user',
          'content': user_input,
      },
  )

  response = ollama.chat(model="llama3", messages=messages)

  messages.append(
      {
          'role': 'assistant',
          'content': response['message']['content'],
      },
  )
  #lista.append(response['message']['content'] + ",")

  lista_csv = []

  #print(response['message']['content'])

  for i in range(0, len(lista)):
    lista_csv.append(response['message']['content'].split('\n')[i].split(',')[0])

  csv_file = pd.DataFrame(columns=["product_name"])
  new_df = pd.DataFrame(lista_csv, columns=csv_file.columns)
  csv_file = pd.concat([csv_file, new_df], ignore_index=True)
  csv_file.to_csv("./product_names.csv", mode='a', header=False, index=False)


if __name__ == "__main__":

  start_time = time.time()

  noWorkers = multiprocessing.cpu_count()
  pool = multiprocessing.Pool(noWorkers)
  for i in range(0, 100, batch_size):
    pool.apply_async(func=get_product_names, args=(i))

  pool.close()
  pool.join()
  #get_product_names(0)
  # for i in range(0, 102, batch_size):
  #   get_product_names(i)
  end_time = time.time()
  elapsed_time = end_time - start_time
  print(f"Timp petrecut: {elapsed_time} seconds")

  
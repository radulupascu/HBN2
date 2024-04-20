import ollama
import pandas as pd
import multiprocessing

pre_prompt = "Please analyze the provided URL and predict the product or service name it leads to. If you cannot identify the product or service, please respond with \"None\". I need you to respond only with your best guess, or just say \"None\" if you can't decide. Please do not reply with any additional words. Try to match your responses as closely as possible to the words in the URL."

modelfile = """
FROM llama3
PARAMETER temperature 0.08
PARAMETER num_ctx 2048
PARAMETER repeat_last_n 0
PARAMETER tfs_z 2.0
SYSTEM {pre_prompt}
""".format(pre_prompt=pre_prompt)

ollama.create(model="llama3", modelfile=modelfile)

messages = [
  {
    'role': 'system',
    'content': pre_prompt,
  },
]

def get_product_names(start_index, finish_index):
  df = pd.read_csv('./url_product_extraction_input_dataset.csv')
      
  nr = 0
  lista = []

  for link in df.iloc[start_index:finish_index, 0]:
      user_input = link

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

      print(response['message']['content'])

if __name__ == "__main__":
  # noWorkers = multiprocessing.cpu_count()
  # pool = multiprocessing.Pool(noWorkers)
  # for i in range(0, 1000, 20):
  #     pool.apply_async(func=get_product_names, args=(i, i+20))

  # pool.close()
  # pool.join()
  get_product_names(20, 50)
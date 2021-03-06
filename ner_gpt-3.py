from transformers import GPT2Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
print(tokenizer("conry guy")['input_ids'])
tokenizer.convert_ids_to_tokens([3516])

#generate list of prompt examples and produce prompt string
num_test_samples = 50
num_prompt_samples = 5


prompt_indices = random.sample(range(len(sentence_maps)), num_test_samples + num_prompt_samples)


sentence_indices = []
for i in range(len(prompt_indices)):
  sentence_indices.append(prompt_indices[i])
  prompt_indices[i] *= 2
test_sentence_indices = sentence_indices[num_prompt_samples:]
prompts = []
for i in range(num_test_samples):
  prompts.append("")

lastval = prompt_indices[-1]

test_sentence_token_sets = []

for test_prompt_idx in range(len(prompts)):

  for ex_idx in prompt_indices[:num_prompt_samples]:

    #add sample sentences and outputs to prompt string
    prompts[test_prompt_idx] += output[ex_idx] + '\n' + output[ex_idx + 1] + '\n\n'

  #add test example to end of prompt
  prompts[test_prompt_idx] += output[prompt_indices[num_prompt_samples + test_prompt_idx]] + '\n' + 'Drugs:'

  #add set of tokens in prompt to list of sets
  test_sentence_token_set = set()
  for key in sentence_maps[int(prompt_indices[num_prompt_samples + test_prompt_idx]/2)]:
    test_sentence_token_set.add(key)
  test_sentence_token_sets.append(test_sentence_token_set)

  print("tokens in test set", test_sentence_token_set)
  
#print(prompt_token_sets[:5])

#GENERATE PREDICTIONS
predictions_maps = []
counter = 0
for prompt in prompts:
  predictions_map = dict()
  #constrain potential output to tokens in test sentence using logit bias
  logit_biases = {}
  for word in test_sentence_token_sets[counter]:
    tokens = tokenizer(word)['input_ids']
  #   for token in tokens:
  #     if token[0] == 'Ġ':
  #       token = token[1:]
  #     if token not in logit_biases:
  #       logit_biases[token] = 0
  # print(logit_biases)
  #use API to generate completion
  sample = openai.Completion.create(engine="davinci",
                          prompt=prompt,
                          max_tokens=10,
                          temperature=0,
                          # logit_bias = logit_biases,
                          presence_penalty=-0.001,
                          stop=["\n", "<|endoftext|>"])
  prediction = sample['choices'][0]['text']
  #print(prediction)
  prediction_tokens = prediction.replace(",","").split()
  for token in prediction_tokens:
    if token.lower() in test_sentence_token_sets[counter]: #ensures token is in test sentence
      print("YES")
      if token.lower() in predictions_map:
        # print(token.lower())
        # print(predictions_map)
        predictions_map[token.lower()] += 1
      else:
        predictions_map[token.lower()] = 1
  predictions_maps.append(predictions_map)
  counter += 1

# LLM-D Test Data Generator

## Generating Test Data

```
python test-data-generator.py
```

This should generate two files:

```
prefix_caching_5000_pairs_side_by_side.csv
guidellm_formatted_prompts.csv
```

We will use `guidellm_formatted_prompts.csv` as our data source for GuideLLM.

## Running GuideLLM

```
guidellm benchmark --target http://<gateway-hostname>/<namespace>/<llm-d-instance> \
    --model openai/gpt-oss-20b \
    --processor <tokenizer-path> \ # for disconnected environment
    --data guidellm_formatted_prompts.csv \
    --rate-type concurrent \
    --rate 500,250,100,50,25,10,5,1 \
    --max-seconds 120
```



guidellm benchmark run --target <url> --model openai/gpt-oss-20b \ --processor <tokenizer path> --rate-type concurrent \ 	
--rate 1,5,10,25,50,100,250,500  --max-seconds 120 \
--data "prompt_tokens=512,output_tokens=256"
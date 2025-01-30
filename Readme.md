# Credit Cards Recommendation System using RAG development

## Overview

This is a simple RAG (Retrival Augmented Generation) Application which utilises the architecture of LLM to answer the questions for a specific context.
This application demonstrates the use of LLM and vector data store to store data and retrieve relevant data for answering the user queries.
We are using simple credit card data for recommending credit card to users based on specific question like spending information etc.

## High Level Design

![Screenshot 2025-01-29 at 2.36.18 PM.png](Screenshot%202025-01-29%20at%202.36.18%E2%80%AFPM.png)

### Components :

#### Data Crawlers

These are the sole data providers for us to collect the relevant data we are going to use for answering questions. 
I am using a simple factory pattern to define schema of crawlers and using a runner class which is registering each 
crawler dynamically using python decorators. This will automatically add new crawler that is created as long as it follows
the naming and coding conventions of this package.

#### LLM Models 

There can be many LLM model combinations that can be used. For demonstration purpose, I am using a couple of LLM models 
and embedding models. This also follows the same coding style and have multiple implementations of IModelFunction which are registered automatically  
as and when they are created. Each implementation has two major methods 1. Prepare Model 2. Recommend

The first method is used by scheduler to refresh the data and load the data in vector data store. The second is used at runtime to answer the use queries.

#### Job Scheduler

Job scheduler is a simple scheduler which is doing some async processing like 
1. Crawling for data to keep the data relevant and updated in document store
2. Refresh the models by training them with latest data at every specific interval

### Prerequisite
In order to run this application, follow the below SOP :

1. Ensure that you install all the requirements from requirements.txt file by running `pip3 install -r requirements.txt`
2. Download Ollama : https://ollama.com/
3. Pull the following models by running command `ollama pull <model_name>`:
   1. `bge-m3` - used for embeddings
   2. `deepseek-r1:8b`
   3. `deepseek-r1:70b`
   4. `mistral`
   5. `nomic-embed-text`- used for embeddings
4. Run `python3 setup.py rebuild` to build the application
5. Run `crm` to launch the server at `http://127.0.0.1:5000/`   
6. To test the model, use the following CURL command :
   1. `curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"query": "<your query>"}'`

### Example :

#### Request :

```commandline
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d 
'{"query": "Which card will be best for me considering that my monthly spends are as follows : ~0.1 Million on online shopping, ~0.1 Million on travelling and ~0.05 Million INR on groceries and other stuff."}'
```

#### Response :

```commandline
<think>

Okay, I need to figure out which HDFC credit card would be best for the user based on their spending habits. Let me break down their monthly expenses: approximately Rs. 0.1 million on online shopping, Rs. 0.1 million on travel, and Rs. 0.05 million on groceries and other things. That adds up to about Rs. 0.35 million per month.

First, looking at the Paytm HDFC Bank Select Credit Card. It offers up to a 10% cashback on personal spends of Rs. 8 lakh annually. So, if the user meets that threshold, they can get good cashback. But their monthly spend is around Rs. 0.35 million, which is about 3.5 lakhs annually. Wait, no, actually, 0.35 million per month times 12 months would be Rs. 4.2 million. That's way more than the 8 lakh mentioned. Hmm, maybe I miscalculated. Oh, wait, perhaps the user spends around Rs. 3.5 lakhs a year in total, not per month. Let me check that again.

Wait, the user's monthly spends are 0.1 million on online shopping, which is Rs. 10,000, 0.1 million on travel (another Rs. 10,000), and 0.05 million on groceries (Rs. 5,000). So total per month is about Rs. 25,000, or Rs. 3 lakh annually. The Select card gives 10% cashback up to Rs. 80,000 a year. If the user spends more than that, they get a higher cashback rate. But their total spend is around Rs. 3 lakh, which might not hit the Rs. 8 lakh threshold for the maximum cashback. However, the cashback is still better than some other options.

Next, the Paytm HDFC Bank Mobile Credit Card offers up to 5% cashback on spends of Rs. 2.5 lakh annually. The user's total spend is about Rs. 3 lakh, which is just above this threshold, so they'd get 5% cashback on the first Rs. 2.5 lakh and maybe a lower rate beyond that. The features include a waived annual fee if they meet certain spends each month, like Rs. 1,000 for the first 30 days and Rs. 25,000 in a year. Their monthly spend is Rs. 25k, which meets the renewal fee waiver but maybe not the monthly fee waiver unless they hit higher spends.

Then there's the HDFC HOG Diners Club Credit Card, which offers lounge access and other perks like fuel surcharge waivers. However, it doesn't mention a specific cashback percentage that would be beneficial for online shopping or groceries. The welcome bonus is Rs. 2500 as a gift card if they spend Rs. 1.5 lakh in 90 days, but the user's monthly spend might make that easy to reach.

Looking at the fees, the Mobile Credit Card has an annual fee of Rs. 149 with some waived fees upon certain spends. The Select card probably has a higher annual fee, maybe around Rs. 1000 or more. The HOG card might have a higher fee too, given its premium features like lounge access.

The user's main spending areas are online shopping, travel, and groceries. The Mobile Credit Card offers cashback on these categories, which is beneficial. The Select card has better cashback rates but only if the user meets a higher annual spend threshold. Since the user's total annual spend is around Rs. 3 lakh, they might just qualify for the higher cashback with the Select card.

But wait, let me double-check the features again. The Select card mentions saving up to 10% on personal spends of Rs. 8 lakh annually. So if the user's total annual spend is around Rs. 3-4 lakh, they would get 10% cashback on that amount. That could be quite significant for their online shopping and travel expenses.

On the other hand, the Mobile card offers 5% cashback up to Rs. 2.5 lakh and then maybe a lower rate beyond that. So if the user spends more than Rs. 2.5 lakh in a year, they get better cashback only on part of it.

Considering all this, the Select card might be better for higher cashback rates, but I need to make sure the user's total annual spend is sufficient to trigger those rates. If their total is around Rs. 3-4 lakh, the 10% cashback would apply to that entire amount, which is beneficial. The Mobile card's 5% on up to Rs. 2.5k and then maybe 3% or something else beyond that might not be as good.

But I'm a bit confused because the user's monthly spends are around Rs. 25k, so annually it's about Rs. 3 lakh. The Select card's 10% on Rs. 8 lakh would mean they get 10% cashback on their entire spend, which is more than what the Mobile card offers.

So, after considering all factors, I think the Paytm HDFC Bank Select Credit Card might be better for this user because of the higher cashback rate that applies to their total annual spending.

</think>

The best credit card for you based on your spending habits is the **Paytm HDFC Bank Select Credit Card**. Here's why:

1. **Cashback Benefits**: The card offers a 10% cashback on personal spends up to Rs. 8 lakh annually. Given your total annual spend of around Rs. 3-4 lakh, this card will provide a higher cashback rate compared to the Paytm HDFC Bank Mobile Credit Card.

2. **Eligibility**: Your total annual spend of approximately Rs. 3 lakh falls within the threshold for the higher cashback rate offered by the Select Credit Card.

3. **Features**: While the HOG Diners Club Credit Card offers premium perks like lounge access, it doesn't provide significant cashback benefits that align with your spending priorities. The Mobile Credit Card, though considered, has lower cashback rates and may not offer as much benefit given your total spend.

Thus, the Paytm HDFC Bank Select Credit Card is the most suitable choice for you due to its higher cashback rate on your annual expenditure.
```

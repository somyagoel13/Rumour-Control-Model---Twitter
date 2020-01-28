from searchtweets import ResultStream, gen_rule_payload, load_credentials

premium_search_args = load_credentials("twitter_keys.yaml",
                                       yaml_key="search_tweets_api",
                                       env_overwrite=False)

rule = gen_rule_payload("UNSC", results_per_call=100) # testing with a sandbox account
#print(rule)

#from searchtweets import collect_results

# tweets = collect_results(rule,
#                          max_results=100,
#                          result_stream_args=premium_search_args)

#[print(tweet.all_text, end='\n\n') for tweet in tweets[0:10]];

rs = ResultStream(rule_payload=rule,
                  max_results=4500,
                  max_pages=45,
                  **premium_search_args)

tweets=list(rs.stream())

import json

with open('tweets5.txt','w') as f:
    json.dump(tweets,f)
print(len(tweets))

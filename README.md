# To Run 
just run docker compose -f docker-compose.yml up -d 
> Be ready for a 7GB cuda image (just docker things, I guess)
# Observations 
1. Aggregated results are the averages of the 3 clients training results:
```fish
❯ CLIENT1
{"w":3.002659797668457,"b":1.7167261838912964}
❯ CLIENT2
{"w":2.9628801345825195,"b":1.705855131149292}
❯ CLIENT3
{"w":2.99751877784729,"b":1.6673948764801025}
Aggregated:
{"w":2.9876862366994223,"b":1.696658730506897}⏎
```

# Reflect 
1. If i trained for more epochs(I only did 100), the aggregated results would be closer to the centralized training results (`w=3.5`, `b=2.0`)

2. Didn't see any GPU stress test, instead got a warning that the GPU is under utilized. Very Fast training next time I will try more epochs. 

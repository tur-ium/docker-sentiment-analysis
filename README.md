# Aim
The aim of this project is create a dockerized sentiment analyser, with containerized test suites. Each test suite runs in a separate container.

There are three types of test:
1. Authentication: Can users log in, and also be rejected if they do not provide the correct credentials? We try two real users Alice and Bob, and a third user that does not exist (Clementine)
2. Authorization: Do users see access to the correct services? Alice can access v1 and v2, Bob can only access v1.
3. Sentiment: Do we get a positive number (indicating positive sentiment) if we send a sentence with a positive sentiment "life is beautiful", and a negative score if sending a less rosy sentimnent "that sucks"?

# Set up and run
```sh
bash setup.sh
```

# Notes
This project uses pytest for running the tests. You should see the output of the tests in `log.txt` in the top-level directory.

For more details, you can check the logs named `api_test.log` created in each of the individual test suites, which are organized as sub-directories under `tests/`

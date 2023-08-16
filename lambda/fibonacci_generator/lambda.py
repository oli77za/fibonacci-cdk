import json
import logging

def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def handler(event, _context):
    n = int(event['input'])
    result = {"inputNumber": n, "result": fibonacci(n), "function": "fibonacci"}
    logging.info(result)
    return result

#!/usr/bin/env python3
import os

import aws_cdk as cdk

from fibonacci_cdk.fibonacci_cdk_stack import FibonacciCdkStack


app = cdk.App()

FibonacciCdkStack(app, "dev-FibonacciCdkStack", stage="dev")
FibonacciCdkStack(app, "test-FibonacciCdkStack", stage="test")

app.synth()

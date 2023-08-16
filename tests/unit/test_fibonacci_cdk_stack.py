import aws_cdk as core
import aws_cdk.assertions as assertions

from fibonacci_cdk.fibonacci_cdk_stack import FibonacciCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in fibonacci_cdk/fibonacci_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = FibonacciCdkStack(app, "fibonacci-cdk")
    template = assertions.Template.from_stack(stack)

    snapshot = """
    {
      "Resources": {
        "MyQueue": {
          "Type": "AWS::SQS::Queue",
          "Properties": {
            "VisibilityTimeout": 300
          }
        }
      }
    }
    """
    assert template.to_json() == snapshot
#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

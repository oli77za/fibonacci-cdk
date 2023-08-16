from aws_cdk import (
    # Duration,
    Stack,
    Tags,
    # aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Fn,
    aws_s3_assets as s3_assets,
    aws_iam as iam,
)
from constructs import Construct
from .stepfunctions import Stepfunctions
from .network import Network
from .storage import Storage


class FibonacciCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, stage: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        Tags.of(self).add('Stage', stage)
        self.stage = stage

        # network = Network(self, 'Network')
        # storage = Storage(self, 'Storage', vpc=network.vpc, security_group=network.security_group)

        fibonacci_lambda = _lambda.Function(
            self, 'FibonacciLambdaHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda/fibonacci_generator'),
            handler='lambda.handler',                        
        )

        # Create the Step Functions state machine
        stepfunctions = Stepfunctions(
            self, 'FibonacciStateMachine', fibonacci_lambda=fibonacci_lambda)

        workflow_starter_lambda = _lambda.Function(
            self, 'WorkflowStarterLambdaHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda/workflow_starter'),
            handler='lambda.handler',
            environment={
                'STATE_MACHINE_ARN': stepfunctions.state_machine.state_machine_arn,
            }
        )

        # Grant the lambda to be invoked by API Gateway
        workflow_starter_lambda.grant_invoke(iam.ServicePrincipal('apigateway.amazonaws.com'))

        # Override the logical ID of the default child of the lambda function
        workflow_starter_lambda.node.default_child.override_logical_id('WorkflowStarterLambdaHandler')

        # Give the Lambda permission to start the state machine
        stepfunctions.state_machine.grant_start_execution(workflow_starter_lambda)


        apiAsset = s3_assets.Asset(self, "ApiAsset", path="api/api-docs.yml")
        data = Fn.transform("AWS::Include", {"Location": apiAsset.s3_object_url})

        apigw.SpecRestApi(
            self, 'FibonacciRestApi',
            api_definition=apigw.ApiDefinition.from_inline(data),            
        )

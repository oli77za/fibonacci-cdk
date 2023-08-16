from constructs import Construct
from aws_cdk import (
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
    Duration,
)


class Stepfunctions(Construct):

    def __init__(self, scope: Construct, construct_id: str, fibonacci_lambda, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        fibonacci_task = sfn_tasks.LambdaInvoke(
            self, 'InvokeFibonacciLambda',
            lambda_function=fibonacci_lambda,
            input_path='$',
            result_path='$.fibonacciResult',
        )

        initial_counter_task = sfn.Pass(
            self, 'InitialCounter',
            result_path='$.counter',
            result=sfn.Result.from_number(0),
        )

        increment_counter_task = sfn.Pass(
            self, 'IncrementCounter',
            parameters={
                'counter.$': 'States.MathAdd($.counter, 1)',
                'fibonacciResult.$': '$.fibonacciResult',
            },
        )

        get_joke_task = sfn.Pass(self, 'GetJoke')

        wait_1_sec_task = sfn.Wait(self, 'Wait 1 sec',
                                   time=sfn.WaitTime.duration(Duration.seconds(1)))

        check_more_jokes_task = sfn.Choice(self, 'more jokes?')

        publish_result_task = sfn.Pass(self, 'Publish result')

        chain = sfn.Chain.start(fibonacci_task)\
            .next(initial_counter_task)\
            .next(increment_counter_task)\
            .next(get_joke_task)\
            .next(wait_1_sec_task)\
            .next(check_more_jokes_task\
                  .when(sfn.Condition.number_less_than_equals_json_path('$.counter', '$.fibonacciResult.Payload.result'), increment_counter_task)\
                  .otherwise(publish_result_task))

        self.state_machine = sfn.StateMachine(
            self, 'FibonacciStateMachine',
            definition_body=sfn.DefinitionBody.from_chainable(chain)
        )

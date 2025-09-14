from mara_pipelines.commands.bash import RunBash
from mara_pipelines.pipelines import Pipeline, Task

# Initialize pipeline object
pipeline = Pipeline(
    id='demo',
    description='A pipeline that pings localhost 3 times')

# Add task to the pipeline - ping localhost three times
pipeline.add(Task(id='ping_localhost', description='Pings localhost',
                  commands=[RunBash('ping -c 3 localhost')]))
import luigi


class BaseTask(luigi.Task):

    force = luigi.BoolParameter()

    def complete(self):
        outputs = luigi.task.flatten(self.output())
        for output in outputs:
            if self.force and output.exists():
                output.remove()
        return all(map(lambda result: result.exists(), outputs))


class HelloTask(BaseTask):

    def run(self):
        with open('hello.txt', 'w') as hello_file:
            hello_file.write('Hello')

    def output(self):
        return luigi.LocalTarget('hello.txt')


if __name__ == "__main__":
    luigi.run()

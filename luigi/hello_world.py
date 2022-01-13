import luigi
import time


class HelloTask(luigi.Task):

    def run(self):
        with open('hello.txt', 'w') as hello_file:
            hello_file.write('Hello')

    def output(self):
        return luigi.LocalTarget('hello.txt')


class WorldTask(luigi.Task):

    def run(self):
        time.sleep(10)
        with open('world.txt', 'w') as world_file:
            world_file.write('World')

    def output(self):
        return luigi.LocalTarget('world.txt')


class HelloWorldTask(luigi.Task):

    def run(self):
        with open('hello.txt', 'r') as hello_file:
            hello = hello_file.read()
        with open('world.txt', 'r') as world_file:
            world = world_file.read()
        with open('hello_world.txt', 'w') as hello_world_file:
            content = "{} {}".format(hello, world)
            hello_world_file.write(content)

    def requires(self):
        return [HelloTask(), WorldTask()]

    def output(self):
        return luigi.LocalTarget('hello_world.txt')


if __name__ == "__main__":
    luigi.run()

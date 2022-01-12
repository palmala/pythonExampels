import luigi
import time

class HelloTask(luigi.Task):

    def run(self):

        with open('hello.txt', 'w') as hello_file:
            hello_file.write('Hello')
            hello_file.close()

    def output(self):
        return luigi.local_target('hello.txt')


class WorldTask(luigi.Task):

    def run(self):
        time.sleep(10)
        with open('world.txt', 'w') as world_file:
            world_file.write('World')
            world_file.close()

    def output(self):
        return luigi.local_target('world.txt')

class HelloWorldTask(luigi.task):

    def run(self):
        with open('hello.txt', 'r') as hello_file:
            hello = hello_file.read()
        with open('world.txt', 'r') as world_file:
            world = world_file.read()
        with open('helloworld.txt', 'w') as helloworld_file:
            content = "{} {}".format(hello, world)
            helloworld_file.write(content)
            helloworld_file.close()
    
    def requires(self):
        return [HelloTask(), WorldTask()]

    def output(self):
        return luigi.local_target('helloworld.txt')


if __name__ == "__main__":
    luigi.run()

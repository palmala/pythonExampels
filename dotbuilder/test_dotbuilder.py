import unittest
from dotbuilder import DotBuilder

example = {
    'VMS/eqrisk/buildManager': ['VMS/odg/sdlcservices'],
    'VMS/odg/rvwebtools': ['VMS/odg/sdlcservices', 'VMS/eqrisk/buildManager'],
    'VMS/odg/sdlcservices': ['VMS/odg/rvwebtools']
}


class TestDotBuild(unittest.TestCase):
    def test_parsing(self):
        subject = DotBuilder(example)
        subject.calculate_instability()
        subject.calculate_violations()
        print(subject.get_stats())

        with open("test.dot", "w") as resultdot:
            resultdot.write(str(subject))


if __name__ == "__main__":
    unittest.main()

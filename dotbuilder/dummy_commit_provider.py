from commit_provider import CommitProvider
from collections import defaultdict


class DummyCommitProvider(CommitProvider):

    def __init__(self):
        self.DUMMY_VALUES = defaultdict(int)
        self.DUMMY_VALUES['C'] = 4
        self.DUMMY_VALUES['E'] = 7

    def get_number_of_commits(self, component):
        return self.DUMMY_VALUES[component]

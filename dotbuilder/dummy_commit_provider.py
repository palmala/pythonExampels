from commit_provider import CommitProvider


class DummyCommitProvider(CommitProvider):
    DUMMY_VALUES = {
        'componentA': 3,
        'componentB': 0,
        'componentC': 5,
    }

    def __init__(self):
        pass

    def get_number_of_commits(self, component):
        return self.DUMMY_VALUES[component]

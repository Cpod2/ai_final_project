"""Task Definitions"""


def task_fixup():
    """Run Formatters"""
    return {
        "actions": [
            "isort --profile=black .",
            "pyupgrade --py311-plus",
            "black .",
            "mdformat .",
        ]
    }


def task_test():
    """Run Tests"""
    return {"actions": ["pylint --recursive=y ."]}

if __name__ == "__main__":
    from .assignment import Assignment
    from .content import Content
    from .quiz import Quiz
    
    q = Quiz()
    print(q.context("2022_1001025"))
def test_can_import_solution():
    import solution.solution as sol
    assert callable(getattr(sol, "predict", None))

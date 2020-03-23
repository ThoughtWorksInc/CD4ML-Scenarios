from cd4ml.decision_tree import main


def run_simple_model():
    print('Run Simple Model')
    main(model=Model.RANDOM_FOREST, seed=8675309)

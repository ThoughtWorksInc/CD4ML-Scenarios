from cd4ml import tracking
from cd4ml.read_data import stream_data, get_encoder
from cd4ml.splitter import get_cutoff_dates, train_filter
from cd4ml.train import train_model
from cd4ml.validate import validate


def run_ml_model(pipeline_params, encoder, track, date_cutoff, seed=None):
    target_name = 'unit_sales'

    train_stream = (row for row in stream_data(pipeline_params) if train_filter(row, date_cutoff))
    encoded_train_stream = encoder.encode_data_stream(train_stream)

    print('Encoding data')
    # batch step, read it all in
    encoded_train_data = list(encoded_train_stream)

    print('Getting target')
    # read it all in
    target = [row[target_name] for row in stream_data(pipeline_params) if train_filter(row, date_cutoff)]

    model_name = pipeline_params['model_name']
    params = pipeline_params['model_params'][model_name]

    track.log_ml_params(params)
    track.log_pipeline_params(pipeline_params)

    trained_model, params = train_model(encoded_train_data, target, model_name, params, seed=seed)

    return trained_model, params


def run_all(pipeline_params):
    # pass in pipeline_params so you maintain top level
    # programmatic control over all of the pipeline

    encoder = get_encoder(pipeline_params, write=True, read_from_file=False)
    date_cutoff, max_date = get_cutoff_dates(pipeline_params)

    # For testing/debugging
    run_all_models = False

    with tracking.track() as track:
        if run_all_models:
            # This is mostly for testing/debugging right now, not fully supported
            # models will overwrite each other and only the last one will show up in
            # ML flow. Turning this on can demonstrate that all models can run
            # They might not all pass the acceptance threshold though

            all_model_names = sorted(list(pipeline_params['model_params'].keys()))
            print('All model names')
            print(all_model_names)
        else:
            all_model_names = [pipeline_params['model_name']]

        for model_name in all_model_names:
            pipeline_params['model_name'] = model_name
            trained_model, params = run_ml_model(pipeline_params, encoder, track, date_cutoff)
            validate(pipeline_params, trained_model, encoder, track, date_cutoff, max_date)

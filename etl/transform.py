from datetime import datetime

def convert_unix_to_timestamp(unix_timestamp_ms):
    """
    Converts a Unix timestamp in milliseconds to a PostgreSQL-compatible timestamp.
    """
    return datetime.utcfromtimestamp(unix_timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')

def calculate_shift_cost(shifts):
    """
    Calculates the total cost for each shift by summing the costs of allowances and award interpretations.
    Also converts Unix timestamps to PostgreSQL-compatible timestamps.
    """
    for shift in shifts:
        total_cost = (
            sum(a['cost'] for a in shift['allowances']) +
            sum(a['cost'] for a in shift['award_interpretations'])
        )
        shift['cost'] = total_cost
        # Convert Unix timestamps to PostgreSQL timestamps
        shift['start'] = convert_unix_to_timestamp(shift['start'])
        shift['finish'] = convert_unix_to_timestamp(shift['finish'])
    return shifts

def extract_models(shifts):
    """
    Extracts nested models (breaks, allowances, and award interpretations) from shifts.
    Also converts Unix timestamps to PostgreSQL-compatible timestamps.
    """
    all_breaks = []
    all_allowances = []
    all_awards = []
    for shift in shifts:
        shift_id = shift['id']
        # Extract breaks (rename 'paid' to 'is_paid' for database compatibility)
        all_breaks.extend([{
            'id': b['id'],
            'shift_id': shift_id,
            'start': convert_unix_to_timestamp(b['start']),
            'finish': convert_unix_to_timestamp(b['finish']),
            'is_paid': b['paid']
        } for b in shift['breaks']])
        # Extract allowances
        all_allowances.extend([{
            'id': a['id'],
            'shift_id': shift_id,
            'allowance_value': a['value'],
            'allowance_cost': a['cost']
        } for a in shift['allowances']])
        # Extract award interpretations
        all_awards.extend([{
            'id': a['id'],
            'shift_id': shift_id,
            'award_date': a['date'],
            'award_units': a['units'],
            'award_cost': a['cost']
        } for a in shift['award_interpretations']])
    return all_breaks, all_allowances, all_awards


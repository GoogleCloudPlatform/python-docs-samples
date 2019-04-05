class Query:
    def __init__(self,
                 uuid,
                 name=None,
                 description=None,
                 owner=None,
                 topic=None,
                 timestamp=None,
                 schedule=None,
                 steps=None,
                 send_notification=False,
                 last_execution_date=None,
                 last_execution_result=None,
                 last_execution_status=None):
        self.uuid = uuid
        self.name = name
        self.description = description
        self.owner = owner
        self.topic = topic
        self.timestamp = timestamp
        self.schedule = schedule
        self.steps = steps
        self.send_notification = send_notification
        self.last_execution_date = last_execution_date
        self.last_execution_result = last_execution_result
        self.last_execution_status = last_execution_status


class SimpleQuery:
    def __init__(self,
                 uuid,
                 name,
                 description,
                 timestamp,
                 owner,
                 mark,
                 next_run=None,
                 last_execution_date=None,
                 last_execution_result=None,
                 last_execution_status=None,
                 send_notification=False):
        self.uuid = uuid
        self.name = name
        self.description = description
        self.timestamp = timestamp
        self.owner = owner
        self.mark = mark
        self.next_run = next_run
        self.last_execution_result = last_execution_result
        self.last_execution_date = last_execution_date
        self.last_execution_status = last_execution_status
        self.send_notification = send_notification


class Threshold:
    def __init__(self, operator, value):
        self.operator = operator
        self.value = value


class ReadTime:
    def __init__(self, _type, value, zone):
        self._type = _type
        self.value = value
        self.zone = zone

    def get_type(self):
        return self._type


class Step:
    def __init__(self, uuid, order, kind,
                 in_join=None, out_join=None, read_time=None,
                 compare_duration=None, threshold=None, filter_=None,
                 last_execution_status=None, last_execution_result=None):
        self.uuid = uuid
        self.order = order
        self.kind = kind
        self.in_join = in_join
        self.out_join = out_join
        self.read_time = read_time
        self.compare_duration = compare_duration
        self.threshold = threshold
        self.filter = filter_
        self.last_execution_status = last_execution_status
        self.last_execution_result = last_execution_result

    def key_for_exception():
        return 'filter'

    def threshold_satisfied(self, response_size):
        if self.threshold:
            threshold_value = int(self.threshold.value)
            options = {
                'lt': response_size < threshold_value,
                'le': response_size <= threshold_value,
                'eq': response_size == threshold_value,
                'ne': response_size != threshold_value,
                'ge': response_size >= threshold_value,
                'gt': response_size > threshold_value
            }
            return options.get(self.threshold.operator, lambda: False)
        return False


class ExecutionResult:
    def __init__(self, result_size, scc_query_link):
        self.result_size = result_size
        self.scc_query_link = scc_query_link

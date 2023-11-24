Traceback (most recent call last):
File "/home/student/IdeaProjects/CSC8112-IoT/task3_cloud_operator.py", line 76, in <module>
channel.start_consuming()
File "/home/student/IdeaProjects/CSC8112-IoT/venv/lib/python3.8/site-packages/pika/adapters/blocking_connection.py", line 1883, in start_consuming
self._process_data_events(time_limit=None)
File "/home/student/IdeaProjects/CSC8112-IoT/venv/lib/python3.8/site-packages/pika/adapters/blocking_connection.py", line 2044, in _process_data_events
self.connection.process_data_events(time_limit=time_limit)
File "/home/student/IdeaProjects/CSC8112-IoT/venv/lib/python3.8/site-packages/pika/adapters/blocking_connection.py", line 851, in process_data_events
self._dispatch_channel_events()
File "/home/student/IdeaProjects/CSC8112-IoT/venv/lib/python3.8/site-packages/pika/adapters/blocking_connection.py", line 567, in _dispatch_channel_events
impl_channel._get_cookie()._dispatch_events()
File "/home/student/IdeaProjects/CSC8112-IoT/venv/lib/python3.8/site-packages/pika/adapters/blocking_connection.py", line 1510, in _dispatch_events
consumer_info.on_message_callback(self, evt.method,
File "/home/student/IdeaProjects/CSC8112-IoT/task3_cloud_operator.py", line 43, in callback
formatted_Timestamp = [timestamp.strftime('%Y-%m-%d') for timestamp in Timestamp]
File "/home/student/IdeaProjects/CSC8112-IoT/task3_cloud_operator.py", line 43, in <listcomp>
formatted_Timestamp = [timestamp.strftime('%Y-%m-%d') for timestamp in Timestamp]
AttributeError: 'str' object has no attribute 'strftime'

Process finished with exit code1
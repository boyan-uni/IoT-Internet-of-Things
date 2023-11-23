/home/student/IdeaProjects/CSC8112-IoT/venv/bin/python /home/student/IdeaProjects/CSC8112-IoT/task32.py
Timestamp: 2023-08-30 20:00:00, Value: 4.499041666666667
After rename columns
Index(['ds', 'y'], dtype='object')
Traceback (most recent call last):
File "/home/student/IdeaProjects/CSC8112-IoT/task32.py", line 95, in <module>
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
File "/home/student/IdeaProjects/CSC8112-IoT/task32.py", line 73, in callback
predictor.train()
File "/home/student/IdeaProjects/CSC8112-IoT/ml_engine.py", line 37, in train
self.__trainer.fit(self.__train_data)
File "/home/student/IdeaProjects/CSC8112-IoT/venv/lib/python3.8/site-packages/prophet/forecaster.py", line 1217, in fit
model_inputs = self.preprocess(df, **kwargs)
File "/home/student/IdeaProjects/CSC8112-IoT/venv/lib/python3.8/site-packages/prophet/forecaster.py", line 1132, in preprocess
raise ValueError('Dataframe has less than 2 non-NaN rows.')
ValueError: Dataframe has less than 2 non-NaN rows.

Process finished with exit code 1

import time

import socketio


# since dataset is using the socketio to recieve
# so here it will start a socket client to wait for msg
class DatasetFileTaskManager(object):
    # default waiting time 20s for the wait
    DEFAULT_WAIT_TIME = 20

    # initialization
    source_geid = None

    def connect_handler(self):
        # print('Connected!')
        pass

    def set_notification(self, data):

        # print(data)
        # we might recieve other unrelated message(in case later the dataset is shared
        # or multiple scripts are running). the checking condition is:
        # 1. status is FINISH
        # 2. action is the same
        # 3. session_id is the same
        # 4. the geid IS in the record map
        # then we will try to pop the key out to say job done
        # if the key not exist then nothing happened
        source_geid = data['payload']['source']['global_entity_id']
        # print(self.source_map)
        # print(source_geid, self.source_map.get(source_geid))
        # print(data['payload']['session_id'], self.session_id)
        # print(data['payload']['status'])
        # print(data['payload']['action'], self.action)
        # print()
        if (
            data['payload']['session_id'] == self.session_id
            and data['payload']['status'] == 'FINISH'
            and data['payload']['action'] == self.action
            and self.source_map.get(source_geid)
        ):

            self.file_notification_msg.append(data)
            self.source_map.pop(source_geid)
            # print(source_geid)

    ########################################################################################

    def __init__(self, socketio_endpoint, dataset_geid, source_geids: list, action, session_id):
        self.namespace = '/' + dataset_geid
        # since we might have batch operation so make a dict
        # to keep track if all job are finished
        self.source_map = {x: 1 for x in source_geids}
        self.action = action
        self.session_id = session_id
        self.file_notification_msg = []
        self.sio = socketio.Client()

        # open the event
        self.sio.on('connect', self.connect_handler, namespace=self.namespace)
        self.sio.on('DATASET_FILE_NOTIFICATION', self.set_notification, namespace=self.namespace)
        # connect to socket server
        self.sio.connect(socketio_endpoint, namespaces=[self.namespace])

    def wait_response(self):
        # we set the timeout for this waiting
        for _ in range(self.DEFAULT_WAIT_TIME):
            # here if we have all job done then exit
            if len(self.source_map) == 0:
                self._disconnect()
                return self.file_notification_msg
            time.sleep(1)

        # raise the error if we timeout
        self._disconnect()
        raise Exception('TIMEOUT FOR SOCKETIO, Job %s are not finished' % (str(self.source_map)))

    def _disconnect(self):
        self.sio.disconnect()


import json
from .jsonrpc import *

STATEMACHINE_RPC_VERSION = '2.0'


class SMInternalError(RPCError):
    def __init__(self, msg, error_code = -20000):
        super(SMInternalError, self).__init__()
        self.message = msg
        self.jsonrpc_error_code = error_code
        

#TODO: do we need to override request and response just for the version?
#todo: do we need to override parse_subrequest at all?

class StateMachineRPCRequest(JSONRPCRequest):

    version = STATEMACHINE_RPC_VERSION

    def _to_dict(self):
        print self.params
        jdata = {
            'jsonrpc':self.version,
            'id':self.unique_id,
            'function':self.function,
            'params':self.params
        }
        return jdata

class StateMachineRPCProtocol(JSONRPCProtocol):
    """JSONRPC protocol implementation.
    """

    _ALLOWED_REPLY_KEYS = sorted(['id', 'jsonrpc', 'error', 'result', 'function'])
    _ALLOWED_REQUEST_KEYS = sorted(['id', 'jsonrpc', 'function', 'params'])

    version = STATEMACHINE_RPC_VERSION

    def __init__(self, *args, **kwargs):
        super(StateMachineRPCProtocol, self).__init__(*args, **kwargs)

    def create_request(self, event, event_data=None):

        request = StateMachineRPCRequest()
        request.unique_id = self._get_unique_id()
        request.version = self.version

        request.function = event
        request.params = event_data if event_data is not None else {}
        return request

    def parse_reply(self, data):
        try:
            rep = json.loads(data)
        except Exception as e:
            raise InvalidReplyError(e)

        for k in rep.keys():
            if not k in self._ALLOWED_REPLY_KEYS:
                raise InvalidReplyError('Key not allowed: %s' % k)

        if not 'jsonrpc' in rep:
            raise InvalidReplyError('Missing jsonrpc (version) in response.')

        if rep['jsonrpc'] != STATEMACHINE_RPC_VERSION:
            raise InvalidReplyError('Wrong JSONRPC version')

        if not 'id' in rep:
            raise InvalidReplyError('Missing id in response')

        if 'error' in rep:
            response = JSONRPCErrorResponse()
            error = rep['error']
            response.error = error['message']
            response._jsonrpc_error_code = error['code']
        else:
            response = JSONRPCSuccessResponse()
            response.result = rep.get('result', None)
            
        response.version = rep['jsonrpc']
        response.function = rep["function"]
        response.unique_id = rep['id']
        return response


    def _parse_subrequest(self, req):
        for k in req.keys():
            if not k in self._ALLOWED_REQUEST_KEYS:
                raise JSONRPCInvalidRequestError(k + ' is not a valid request key')

        if req.get('jsonrpc', None) != STATEMACHINE_RPC_VERSION:
            raise JSONRPCInvalidRequestError('json rpc version unmatched')

        if not 'function' in req:
            raise JSONRPCInvalidRequestError('no event name in the request')

        request = StateMachineRPCRequest()
        request.method = str(req['function']).lower()
        request.version = req['jsonrpc']
        request.params = req.get('params', None)
        request.unique_id = req.get('id', None)
        return request


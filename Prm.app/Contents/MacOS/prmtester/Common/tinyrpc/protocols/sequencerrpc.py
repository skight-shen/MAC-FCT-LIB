from jsonrpc import *
import json


class SequencerRPCRequest(JSONRPCRequest):
    def _to_dict(self):
        jdata = {
            'jsonrpc' : JSONRPCProtocol.JSON_RPC_VERSION,
            'id' : self.unique_id,
            'method' : self.method,
            'args' : self.args,
            'kwargs' : self.kwargs
        }

        return jdata


class SequencerRPCProtocol(JSONRPCProtocol):
    """JSONRPC protocol implementation.
    """

    def __init__(self, *args, **kwargs):
        super(SequencerRPCProtocol, self).__init__(*args, **kwargs)

    def create_request(self, verb, line):

        request = SequencerRPCRequest()
        request.unique_id = self._get_unique_id()

        request.method = verb
        if line is None:
            request.args = []
        else:
            request.args = [line]
        request.kwargs = {}

        return request

    def parse_reply(self, data):
        try:
            rep = json.loads(data)
        except Exception as e:
            raise InvalidReplyError(e)

        for k in rep.keys():
            if not k in JSONRPCProtocol._ALLOWED_REPLY_KEYS:
                raise InvalidReplyError('Key not allowed: %s' % k)

        if not 'jsonrpc' in rep:
            raise InvalidReplyError('Missing jsonrpc (version) in response.')

        if rep['jsonrpc'] != JSONRPCProtocol.JSON_RPC_VERSION:
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

        response.unique_id = rep['id']
        response.method = rep.get('method', None)
        
        return response


    def _parse_subrequest(self, req):
        for k in req.keys():
            if not k in JSONRPCProtocol._ALLOWED_REQUEST_KEYS:
                raise JSONRPCInvalidRequestError(k + ' is not a valid request key')
        
        if req.get('jsonrpc', None) != JSONRPCProtocol.JSON_RPC_VERSION:
            raise JSONRPCInvalidRequestError('json rpc version unmatched')

        if not 'method' in req:
            raise JSONRPCInvalidRequestError('no verb in the request')

        request = SequencerRPCRequest()
        request.method = str(req["method"])
        request.version = req['jsonrpc']
        request.args = req.get('args', None)
        request.kwargs = req.get('kwargs', None)

        request.unique_id = req.get('id')

        return request

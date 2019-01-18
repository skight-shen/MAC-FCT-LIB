from .jsonrpc import *


class TERPCServerError(FixedErrorMessageMixin, ServerError):
    jsonrpc_error_code = -40001
    message = 'Test Engine Internal error'

    def __init__(self, msg=''):
        super(TERPCServerError, self).__init__()
        if msg:
            self.message = msg

class TERPCRequest(JSONRPCRequest):
    def _to_dict(self):
        jdata = {
            'jsonrpc' : JSONRPCProtocol.JSON_RPC_VERSION,
            'id' : self.unique_id,
            'method' : self.method,
            'args' :  self.args,
            'kwargs' : self.kwargs
        }
        return jdata


class TERPCProtocol(JSONRPCProtocol):

    '''
    if no error, the reply should be: dict(id='some_id', jsonrpc='version', result=PASS/FAIL, returned='some value'}
    if the function call expects a result, meaning Param2 is not emptied, then returned should have the returned value,
    otherwise there should be no returned
    if error, the reply should be: dict(id='some_id', 'jsonrpc'='version', 'error'=dict(code=error_code, message='error message'}
    '''

    def __init__(self, *args, **kwargs):
        super(TERPCProtocol, self).__init__(*args, **kwargs)

    def create_request(self, function, params, unit='', timeout=3000):
        request = TERPCRequest()

        request.unique_id = self._get_unique_id()
        request.method = function
        if params is None:
            request.args = []
        else:
            request.args = params

        request.kwargs = {"timeout":timeout, "unit": unit}

        return request

    def parse_reply(self, data):
        #receive variable value
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
            response.version=rep['jsonrpc']
            response.unique_id = rep['id']
            response._jsonrpc_error_code = error['code']
        else:
            response = JSONRPCSuccessResponse()
            response.result = rep.get('result', None)
            response.unique_id = rep.get('id')
            response.version = rep.get('jsonrpc')

        response.unique_id = rep['id']
        response.method = rep.get("method", None)
        return response


    def _parse_subrequest(self, req):
        for k in req.keys():
            if not k in JSONRPCProtocol._ALLOWED_REQUEST_KEYS:
                raise JSONRPCInvalidRequestError('key in request not allowed')

        if req.get('jsonrpc', None) != JSONRPCProtocol.JSON_RPC_VERSION:
            raise JSONRPCInvalidRequestError('json rpc version unmatched')

        if 'method' not in req:
            raise JSONRPCInvalidRequestError('missing function in request')


        request = TERPCRequest()
        request.method = str(req['method'])
        request.unique_id = req.get('id')
        request.args = req.get('args', [])
        request.version = req.get('jsonrpc')
        request.kwargs = req.get('kwargs', {})

        return request


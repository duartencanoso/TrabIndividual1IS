# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import produtos_pb2 as produtos__pb2

GRPC_GENERATED_VERSION = '1.71.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in produtos_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ProdutoServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListarProdutos = channel.unary_unary(
                '/catalogo.ProdutoService/ListarProdutos',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=produtos__pb2.ListaProdutos.FromString,
                _registered_method=True)
        self.AdicionarProduto = channel.unary_unary(
                '/catalogo.ProdutoService/AdicionarProduto',
                request_serializer=produtos__pb2.Produto.SerializeToString,
                response_deserializer=produtos__pb2.ProdutoResponse.FromString,
                _registered_method=True)
        self.RemoverProduto = channel.unary_unary(
                '/catalogo.ProdutoService/RemoverProduto',
                request_serializer=produtos__pb2.ProdutoId.SerializeToString,
                response_deserializer=produtos__pb2.ProdutoResponse.FromString,
                _registered_method=True)
        self.ListarProdutosStream = channel.unary_stream(
                '/catalogo.ProdutoService/ListarProdutosStream',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=produtos__pb2.Produto.FromString,
                _registered_method=True)


class ProdutoServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ListarProdutos(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AdicionarProduto(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoverProduto(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListarProdutosStream(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProdutoServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListarProdutos': grpc.unary_unary_rpc_method_handler(
                    servicer.ListarProdutos,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=produtos__pb2.ListaProdutos.SerializeToString,
            ),
            'AdicionarProduto': grpc.unary_unary_rpc_method_handler(
                    servicer.AdicionarProduto,
                    request_deserializer=produtos__pb2.Produto.FromString,
                    response_serializer=produtos__pb2.ProdutoResponse.SerializeToString,
            ),
            'RemoverProduto': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoverProduto,
                    request_deserializer=produtos__pb2.ProdutoId.FromString,
                    response_serializer=produtos__pb2.ProdutoResponse.SerializeToString,
            ),
            'ListarProdutosStream': grpc.unary_stream_rpc_method_handler(
                    servicer.ListarProdutosStream,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=produtos__pb2.Produto.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'catalogo.ProdutoService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('catalogo.ProdutoService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ProdutoService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListarProdutos(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/catalogo.ProdutoService/ListarProdutos',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            produtos__pb2.ListaProdutos.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AdicionarProduto(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/catalogo.ProdutoService/AdicionarProduto',
            produtos__pb2.Produto.SerializeToString,
            produtos__pb2.ProdutoResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def RemoverProduto(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/catalogo.ProdutoService/RemoverProduto',
            produtos__pb2.ProdutoId.SerializeToString,
            produtos__pb2.ProdutoResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ListarProdutosStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/catalogo.ProdutoService/ListarProdutosStream',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            produtos__pb2.Produto.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: video.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bvideo.proto\x12\x05video\"\x81\x01\n\x05Image\x12\x11\n\ttimestamp\x18\x01 \x02(\x01\x12\x0c\n\x04\x63ols\x18\x02 \x02(\x05\x12\x0c\n\x04rows\x18\x03 \x02(\x05\x12\x10\n\x08\x63hannels\x18\x04 \x02(\x05\x12\x0e\n\x06\x66ormat\x18\x05 \x02(\t\x12\x13\n\x0bimage_bytes\x18\x06 \x02(\x0c\x12\x12\n\nchannel_id\x18\x07 \x02(\x05\"%\n\x05Video\x12\x1c\n\x06\x66rames\x18\x01 \x03(\x0b\x32\x0c.video.Image')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'video_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_IMAGE']._serialized_start=23
  _globals['_IMAGE']._serialized_end=152
  _globals['_VIDEO']._serialized_start=154
  _globals['_VIDEO']._serialized_end=191
# @@protoc_insertion_point(module_scope)

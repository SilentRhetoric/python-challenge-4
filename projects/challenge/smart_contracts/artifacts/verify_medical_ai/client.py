# flake8: noqa
# fmt: off
# mypy: disable-error-code="no-any-return, no-untyped-call, misc, type-arg"
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
# requires: algokit-utils@^1.2.0
import base64
import dataclasses
import decimal
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.v2client import models
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AtomicTransactionResponse,
    SimulateAtomicTransactionResponse,
    TransactionSigner,
    TransactionWithSigner
)

_APP_SPEC_JSON = r"""{
    "hints": {
        "record_ai_info(string,string,string,uint64,bool,bool)void": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "get_ai_info()(string,string,string,uint64,bool,bool)": {
            "read_only": true,
            "structs": {
                "output": {
                    "name": "AiInfo",
                    "elements": [
                        [
                            "name",
                            "string"
                        ],
                        [
                            "used_model",
                            "string"
                        ],
                        [
                            "medical_degree",
                            "string"
                        ],
                        [
                            "mcat_score",
                            "uint64"
                        ],
                        [
                            "residency_training",
                            "bool"
                        ],
                        [
                            "medical_license",
                            "bool"
                        ]
                    ]
                }
            },
            "call_config": {
                "no_op": "CALL"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMudmVyaWZ5X21lZGljYWxfYWkuY29udHJhY3QuVmVyaWZ5TWVkaWNhbEFJLmFwcHJvdmFsX3Byb2dyYW06CiAgICAvLyBzbWFydF9jb250cmFjdHMvdmVyaWZ5X21lZGljYWxfYWkvY29udHJhY3QucHk6MTMKICAgIC8vIGNsYXNzIFZlcmlmeU1lZGljYWxBSShBUkM0Q29udHJhY3QpOgogICAgdHhuIE51bUFwcEFyZ3MKICAgIGJ6IG1haW5fYmFyZV9yb3V0aW5nQDYKICAgIG1ldGhvZCAicmVjb3JkX2FpX2luZm8oc3RyaW5nLHN0cmluZyxzdHJpbmcsdWludDY0LGJvb2wsYm9vbCl2b2lkIgogICAgbWV0aG9kICJnZXRfYWlfaW5mbygpKHN0cmluZyxzdHJpbmcsc3RyaW5nLHVpbnQ2NCxib29sLGJvb2wpIgogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMAogICAgbWF0Y2ggbWFpbl9yZWNvcmRfYWlfaW5mb19yb3V0ZUAyIG1haW5fZ2V0X2FpX2luZm9fcm91dGVAMwogICAgZXJyIC8vIHJlamVjdCB0cmFuc2FjdGlvbgoKbWFpbl9yZWNvcmRfYWlfaW5mb19yb3V0ZUAyOgogICAgLy8gc21hcnRfY29udHJhY3RzL3ZlcmlmeV9tZWRpY2FsX2FpL2NvbnRyYWN0LnB5OjI4CiAgICAvLyBAYXJjNC5hYmltZXRob2QoKQogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIE9uQ29tcGxldGlvbiBpcyBOb09wCiAgICB0eG4gQXBwbGljYXRpb25JRAogICAgYXNzZXJ0IC8vIGlzIG5vdCBjcmVhdGluZwogICAgLy8gc21hcnRfY29udHJhY3RzL3ZlcmlmeV9tZWRpY2FsX2FpL2NvbnRyYWN0LnB5OjEzCiAgICAvLyBjbGFzcyBWZXJpZnlNZWRpY2FsQUkoQVJDNENvbnRyYWN0KToKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDEKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDIKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDMKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDQKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDUKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDYKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy92ZXJpZnlfbWVkaWNhbF9haS9jb250cmFjdC5weToyOAogICAgLy8gQGFyYzQuYWJpbWV0aG9kKCkKICAgIGNhbGxzdWIgcmVjb3JkX2FpX2luZm8KICAgIGludCAxCiAgICByZXR1cm4KCm1haW5fZ2V0X2FpX2luZm9fcm91dGVAMzoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy92ZXJpZnlfbWVkaWNhbF9haS9jb250cmFjdC5weTo0NwogICAgLy8gQGFyYzQuYWJpbWV0aG9kKHJlYWRvbmx5PVRydWUpCiAgICB0eG4gT25Db21wbGV0aW9uCiAgICAhCiAgICBhc3NlcnQgLy8gT25Db21wbGV0aW9uIGlzIE5vT3AKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gaXMgbm90IGNyZWF0aW5nCiAgICBjYWxsc3ViIGdldF9haV9pbmZvCiAgICBieXRlIDB4MTUxZjdjNzUKICAgIHN3YXAKICAgIGNvbmNhdAogICAgbG9nCiAgICBpbnQgMQogICAgcmV0dXJuCgptYWluX2JhcmVfcm91dGluZ0A2OgogICAgLy8gc21hcnRfY29udHJhY3RzL3ZlcmlmeV9tZWRpY2FsX2FpL2NvbnRyYWN0LnB5OjEzCiAgICAvLyBjbGFzcyBWZXJpZnlNZWRpY2FsQUkoQVJDNENvbnRyYWN0KToKICAgIHR4biBPbkNvbXBsZXRpb24KICAgIHN3aXRjaCBtYWluX2NyZWF0ZUA3IG1haW5fb3B0X2luQDgKICAgIGVyciAvLyByZWplY3QgdHJhbnNhY3Rpb24KCm1haW5fY3JlYXRlQDc6CiAgICAvLyBzbWFydF9jb250cmFjdHMvdmVyaWZ5X21lZGljYWxfYWkvY29udHJhY3QucHk6MTMKICAgIC8vIGNsYXNzIFZlcmlmeU1lZGljYWxBSShBUkM0Q29udHJhY3QpOgogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgICEKICAgIGFzc2VydCAvLyBpcyBjcmVhdGluZwogICAgaW50IDEKICAgIHJldHVybgoKbWFpbl9vcHRfaW5AODoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy92ZXJpZnlfbWVkaWNhbF9haS9jb250cmFjdC5weToxNwogICAgLy8gQGFyYzQuYmFyZW1ldGhvZChhbGxvd19hY3Rpb25zPVsiT3B0SW4iXSkKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gaXMgbm90IGNyZWF0aW5nCiAgICAvLyBzbWFydF9jb250cmFjdHMvdmVyaWZ5X21lZGljYWxfYWkvY29udHJhY3QucHk6MTctMTgKICAgIC8vIEBhcmM0LmJhcmVtZXRob2QoYWxsb3dfYWN0aW9ucz1bIk9wdEluIl0pCiAgICAvLyBkZWYgb3B0X2luKHNlbGYpIC0+IE5vbmU6CiAgICBjYWxsc3ViIG9wdF9pbgogICAgaW50IDEKICAgIHJldHVybgoKCi8vIHNtYXJ0X2NvbnRyYWN0cy52ZXJpZnlfbWVkaWNhbF9haS5jb250cmFjdC5WZXJpZnlNZWRpY2FsQUkucmVjb3JkX2FpX2luZm8obmFtZTogYnl0ZXMsIHVzZWRfbW9kZWw6IGJ5dGVzLCBtZWRpY2FsX2RlZ3JlZTogYnl0ZXMsIG1jYXRfc2NvcmU6IGJ5dGVzLCByZXNpZGVuY3lfdHJhaW5pbmc6IGJ5dGVzLCBtZWRpY2FsX2xpY2Vuc2U6IGJ5dGVzKSAtPiB2b2lkOgpyZWNvcmRfYWlfaW5mbzoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy92ZXJpZnlfbWVkaWNhbF9haS9jb250cmFjdC5weToyOC0zNwogICAgLy8gQGFyYzQuYWJpbWV0aG9kKCkKICAgIC8vIGRlZiByZWNvcmRfYWlfaW5mbygKICAgIC8vICAgICBzZWxmLAogICAgLy8gICAgIG5hbWU6IGFyYzQuU3RyaW5nLAogICAgLy8gICAgIHVzZWRfbW9kZWw6IGFyYzQuU3RyaW5nLAogICAgLy8gICAgIG1lZGljYWxfZGVncmVlOiBhcmM0LlN0cmluZywKICAgIC8vICAgICBtY2F0X3Njb3JlOiBhcmM0LlVJbnQ2NCwKICAgIC8vICAgICByZXNpZGVuY3lfdHJhaW5pbmc6IGFyYzQuQm9vbCwKICAgIC8vICAgICBtZWRpY2FsX2xpY2Vuc2U6IGFyYzQuQm9vbAogICAgLy8gKSAtPiBOb25lOgogICAgcHJvdG8gNiAwCiAgICAvLyBzbWFydF9jb250cmFjdHMvdmVyaWZ5X21lZGljYWxfYWkvY29udHJhY3QucHk6MzgtNDUKICAgIC8vIHNlbGYuYWlfaW5mb1tUeG4uc2VuZGVyXSA9IEFpSW5mbygKICAgIC8vICAgICBuYW1lPW5hbWUsCiAgICAvLyAgICAgdXNlZF9tb2RlbD11c2VkX21vZGVsLAogICAgLy8gICAgIG1lZGljYWxfZGVncmVlPW1lZGljYWxfZGVncmVlLAogICAgLy8gICAgIG1jYXRfc2NvcmU9bWNhdF9zY29yZSwKICAgIC8vICAgICByZXNpZGVuY3lfdHJhaW5pbmc9cmVzaWRlbmN5X3RyYWluaW5nLAogICAgLy8gICAgIG1lZGljYWxfbGljZW5zZT1tZWRpY2FsX2xpY2Vuc2UsCiAgICAvLyApCiAgICBmcmFtZV9kaWcgLTYKICAgIGxlbgogICAgaW50IDE1CiAgICArCiAgICBkdXAKICAgIGl0b2IKICAgIGV4dHJhY3QgNiAyCiAgICBieXRlIDB4MDAwZgogICAgc3dhcAogICAgY29uY2F0CiAgICBzd2FwCiAgICBmcmFtZV9kaWcgLTUKICAgIGxlbgogICAgKwogICAgaXRvYgogICAgZXh0cmFjdCA2IDIKICAgIGNvbmNhdAogICAgZnJhbWVfZGlnIC0zCiAgICBjb25jYXQKICAgIGZyYW1lX2RpZyAtMgogICAgY29uY2F0CiAgICBmcmFtZV9kaWcgLTEKICAgIGludCAwCiAgICBnZXRiaXQKICAgIGludCAxMTMKICAgIHN3YXAKICAgIHNldGJpdAogICAgZnJhbWVfZGlnIC02CiAgICBjb25jYXQKICAgIGZyYW1lX2RpZyAtNQogICAgY29uY2F0CiAgICBmcmFtZV9kaWcgLTQKICAgIGNvbmNhdAogICAgLy8gc21hcnRfY29udHJhY3RzL3ZlcmlmeV9tZWRpY2FsX2FpL2NvbnRyYWN0LnB5OjM4CiAgICAvLyBzZWxmLmFpX2luZm9bVHhuLnNlbmRlcl0gPSBBaUluZm8oCiAgICB0eG4gU2VuZGVyCiAgICBieXRlICJhaV9pbmZvIgogICAgLy8gc21hcnRfY29udHJhY3RzL3ZlcmlmeV9tZWRpY2FsX2FpL2NvbnRyYWN0LnB5OjM4LTQ1CiAgICAvLyBzZWxmLmFpX2luZm9bVHhuLnNlbmRlcl0gPSBBaUluZm8oCiAgICAvLyAgICAgbmFtZT1uYW1lLAogICAgLy8gICAgIHVzZWRfbW9kZWw9dXNlZF9tb2RlbCwKICAgIC8vICAgICBtZWRpY2FsX2RlZ3JlZT1tZWRpY2FsX2RlZ3JlZSwKICAgIC8vICAgICBtY2F0X3Njb3JlPW1jYXRfc2NvcmUsCiAgICAvLyAgICAgcmVzaWRlbmN5X3RyYWluaW5nPXJlc2lkZW5jeV90cmFpbmluZywKICAgIC8vICAgICBtZWRpY2FsX2xpY2Vuc2U9bWVkaWNhbF9saWNlbnNlLAogICAgLy8gKQogICAgdW5jb3ZlciAyCiAgICBhcHBfbG9jYWxfcHV0CiAgICByZXRzdWIKCgovLyBzbWFydF9jb250cmFjdHMudmVyaWZ5X21lZGljYWxfYWkuY29udHJhY3QuVmVyaWZ5TWVkaWNhbEFJLmdldF9haV9pbmZvKCkgLT4gYnl0ZXM6CmdldF9haV9pbmZvOgogICAgLy8gc21hcnRfY29udHJhY3RzL3ZlcmlmeV9tZWRpY2FsX2FpL2NvbnRyYWN0LnB5OjQ3LTQ4CiAgICAvLyBAYXJjNC5hYmltZXRob2QocmVhZG9ubHk9VHJ1ZSkKICAgIC8vIGRlZiBnZXRfYWlfaW5mbyhzZWxmKSAtPiBBaUluZm86CiAgICBwcm90byAwIDEKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy92ZXJpZnlfbWVkaWNhbF9haS9jb250cmFjdC5weTo0OQogICAgLy8gYXNzZXJ0IG9wLmFwcF9vcHRlZF9pbihUeG4uc2VuZGVyLCBHbG9iYWwuY3VycmVudF9hcHBsaWNhdGlvbl9pZCkKICAgIHR4biBTZW5kZXIKICAgIGdsb2JhbCBDdXJyZW50QXBwbGljYXRpb25JRAogICAgYXBwX29wdGVkX2luCiAgICBhc3NlcnQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy92ZXJpZnlfbWVkaWNhbF9haS9jb250cmFjdC5weTo1MAogICAgLy8gcmV0dXJuIHNlbGYuYWlfaW5mb1tUeG4uc2VuZGVyXQogICAgdHhuIFNlbmRlcgogICAgaW50IDAKICAgIGJ5dGUgImFpX2luZm8iCiAgICBhcHBfbG9jYWxfZ2V0X2V4CiAgICBhc3NlcnQgLy8gY2hlY2sgYWlfaW5mbyBleGlzdHMgZm9yIGFjY291bnQKICAgIHJldHN1YgoKCi8vIHNtYXJ0X2NvbnRyYWN0cy52ZXJpZnlfbWVkaWNhbF9haS5jb250cmFjdC5WZXJpZnlNZWRpY2FsQUkub3B0X2luKCkgLT4gdm9pZDoKb3B0X2luOgogICAgLy8gc21hcnRfY29udHJhY3RzL3ZlcmlmeV9tZWRpY2FsX2FpL2NvbnRyYWN0LnB5OjE3LTE4CiAgICAvLyBAYXJjNC5iYXJlbWV0aG9kKGFsbG93X2FjdGlvbnM9WyJPcHRJbiJdKQogICAgLy8gZGVmIG9wdF9pbihzZWxmKSAtPiBOb25lOgogICAgcHJvdG8gMCAwCiAgICAvLyBzbWFydF9jb250cmFjdHMvdmVyaWZ5X21lZGljYWxfYWkvY29udHJhY3QucHk6MTkKICAgIC8vIHNlbGYuYWlfaW5mb1tUeG4uc2VuZGVyXSA9IEFpSW5mbygKICAgIHR4biBTZW5kZXIKICAgIGJ5dGUgImFpX2luZm8iCiAgICAvLyBzbWFydF9jb250cmFjdHMvdmVyaWZ5X21lZGljYWxfYWkvY29udHJhY3QucHk6MTktMjYKICAgIC8vIHNlbGYuYWlfaW5mb1tUeG4uc2VuZGVyXSA9IEFpSW5mbygKICAgIC8vICAgICBuYW1lPWFyYzQuU3RyaW5nKCIiKSwKICAgIC8vICAgICB1c2VkX21vZGVsPWFyYzQuU3RyaW5nKCIiKSwKICAgIC8vICAgICBtZWRpY2FsX2RlZ3JlZT1hcmM0LlN0cmluZygiIiksCiAgICAvLyAgICAgbWNhdF9zY29yZT1hcmM0LlVJbnQ2NCgwKSwKICAgIC8vICAgICByZXNpZGVuY3lfdHJhaW5pbmc9YXJjNC5Cb29sKEZhbHNlKSwKICAgIC8vICAgICBtZWRpY2FsX2xpY2Vuc2U9YXJjNC5Cb29sKEZhbHNlKSwKICAgIC8vICkKICAgIGJ5dGUgMHgwMDBmMDAxMTAwMTMwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAKICAgIGFwcF9sb2NhbF9wdXQKICAgIHJldHN1Ygo=",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMudmVyaWZ5X21lZGljYWxfYWkuY29udHJhY3QuVmVyaWZ5TWVkaWNhbEFJLmNsZWFyX3N0YXRlX3Byb2dyYW06CiAgICAvLyBzbWFydF9jb250cmFjdHMvdmVyaWZ5X21lZGljYWxfYWkvY29udHJhY3QucHk6MTMKICAgIC8vIGNsYXNzIFZlcmlmeU1lZGljYWxBSShBUkM0Q29udHJhY3QpOgogICAgaW50IDEKICAgIHJldHVybgo="
    },
    "state": {
        "global": {
            "num_byte_slices": 0,
            "num_uints": 0
        },
        "local": {
            "num_byte_slices": 1,
            "num_uints": 0
        }
    },
    "schema": {
        "global": {
            "declared": {},
            "reserved": {}
        },
        "local": {
            "declared": {
                "ai_info": {
                    "type": "bytes",
                    "key": "ai_info"
                }
            },
            "reserved": {}
        }
    },
    "contract": {
        "name": "VerifyMedicalAI",
        "methods": [
            {
                "name": "record_ai_info",
                "args": [
                    {
                        "type": "string",
                        "name": "name"
                    },
                    {
                        "type": "string",
                        "name": "used_model"
                    },
                    {
                        "type": "string",
                        "name": "medical_degree"
                    },
                    {
                        "type": "uint64",
                        "name": "mcat_score"
                    },
                    {
                        "type": "bool",
                        "name": "residency_training"
                    },
                    {
                        "type": "bool",
                        "name": "medical_license"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "get_ai_info",
                "args": [],
                "returns": {
                    "type": "(string,string,string,uint64,bool,bool)"
                }
            }
        ],
        "networks": {}
    },
    "bare_call_config": {
        "no_op": "CREATE",
        "opt_in": "CALL"
    }
}"""
APP_SPEC = algokit_utils.ApplicationSpecification.from_json(_APP_SPEC_JSON)
_TReturn = typing.TypeVar("_TReturn")


class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


_TArgs = typing.TypeVar("_TArgs", bound=_ArgsBase[typing.Any])


@dataclasses.dataclass(kw_only=True)
class _TArgsHolder(typing.Generic[_TArgs]):
    args: _TArgs


def _filter_none(value: dict | typing.Any) -> dict | typing.Any:
    if isinstance(value, dict):
        return {k: _filter_none(v) for k, v in value.items() if v is not None}
    return value


def _as_dict(data: typing.Any, *, convert_all: bool = True) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    if convert_all:
        result = dataclasses.asdict(data)
    else:
        result = {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}
    return _filter_none(result)


def _convert_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.TransactionParametersDict:
    return typing.cast(algokit_utils.TransactionParametersDict, _as_dict(transaction_parameters))


def _convert_call_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.OnCompleteCallParametersDict:
    return typing.cast(algokit_utils.OnCompleteCallParametersDict, _as_dict(transaction_parameters))


def _convert_create_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
    on_complete: algokit_utils.OnCompleteActionName,
) -> algokit_utils.CreateCallParametersDict:
    result = typing.cast(algokit_utils.CreateCallParametersDict, _as_dict(transaction_parameters))
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    result["on_complete"] = getattr(algosdk.transaction.OnComplete, on_complete_enum)
    return result


def _convert_deploy_args(
    deploy_args: algokit_utils.DeployCallArgs | None,
) -> algokit_utils.ABICreateCallArgsDict | None:
    if deploy_args is None:
        return None

    deploy_args_dict = typing.cast(algokit_utils.ABICreateCallArgsDict, _as_dict(deploy_args))
    if isinstance(deploy_args, _TArgsHolder):
        deploy_args_dict["args"] = _as_dict(deploy_args.args)
        deploy_args_dict["method"] = deploy_args.args.method()

    return deploy_args_dict


@dataclasses.dataclass(kw_only=True)
class RecordAiInfoArgs(_ArgsBase[None]):
    name: str
    used_model: str
    medical_degree: str
    mcat_score: int
    residency_training: bool
    medical_license: bool

    @staticmethod
    def method() -> str:
        return "record_ai_info(string,string,string,uint64,bool,bool)void"


@dataclasses.dataclass(kw_only=True)
class AiInfo:
    name: str
    used_model: str
    medical_degree: str
    mcat_score: int
    residency_training: bool
    medical_license: bool


@dataclasses.dataclass(kw_only=True)
class GetAiInfoArgs(_ArgsBase[AiInfo]):
    @staticmethod
    def method() -> str:
        return "get_ai_info()(string,string,string,uint64,bool,bool)"


class ByteReader:
    def __init__(self, data: bytes):
        self._data = data

    @property
    def as_bytes(self) -> bytes:
        return self._data

    @property
    def as_str(self) -> str:
        return self._data.decode("utf8")

    @property
    def as_base64(self) -> str:
        return base64.b64encode(self._data).decode("utf8")

    @property
    def as_hex(self) -> str:
        return self._data.hex()


class LocalState:
    def __init__(self, data: dict[bytes, bytes | int]):
        self.ai_info = ByteReader(typing.cast(bytes, data.get(b"ai_info")))


@dataclasses.dataclass(kw_only=True)
class SimulateOptions:
    allow_more_logs: bool = dataclasses.field(default=False)
    allow_empty_signatures: bool = dataclasses.field(default=False)
    extra_opcode_budget: int = dataclasses.field(default=0)
    exec_trace_config: models.SimulateTraceConfig | None         = dataclasses.field(default=None)


class Composer:

    def __init__(self, app_client: algokit_utils.ApplicationClient, atc: AtomicTransactionComposer):
        self.app_client = app_client
        self.atc = atc

    def build(self) -> AtomicTransactionComposer:
        return self.atc

    def simulate(self, options: SimulateOptions | None = None) -> SimulateAtomicTransactionResponse:
        request = models.SimulateRequest(
            allow_more_logs=options.allow_more_logs,
            allow_empty_signatures=options.allow_empty_signatures,
            extra_opcode_budget=options.extra_opcode_budget,
            exec_trace_config=options.exec_trace_config,
            txn_groups=[]
        ) if options else None
        result = self.atc.simulate(self.app_client.algod_client, request)
        return result

    def execute(self) -> AtomicTransactionResponse:
        return self.app_client.execute_atc(self.atc)

    def record_ai_info(
        self,
        *,
        name: str,
        used_model: str,
        medical_degree: str,
        mcat_score: int,
        residency_training: bool,
        medical_license: bool,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `record_ai_info(string,string,string,uint64,bool,bool)void` ABI method
        
        :param str name: The `name` ABI parameter
        :param str used_model: The `used_model` ABI parameter
        :param str medical_degree: The `medical_degree` ABI parameter
        :param int mcat_score: The `mcat_score` ABI parameter
        :param bool residency_training: The `residency_training` ABI parameter
        :param bool medical_license: The `medical_license` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = RecordAiInfoArgs(
            name=name,
            used_model=used_model,
            medical_degree=medical_degree,
            mcat_score=mcat_score,
            residency_training=residency_training,
            medical_license=medical_license,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def get_ai_info(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `get_ai_info()(string,string,string,uint64,bool,bool)` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = GetAiInfoArgs()
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to create an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_create(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return self

    def opt_in_bare(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a calls to the opt_in bare method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_opt_in(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
        )
        return self

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> "Composer":
        """Adds a call to the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass"""
    
        self.app_client.compose_clear_state(self.atc, _convert_transaction_parameters(transaction_parameters), app_args)
        return self


class VerifyMedicalAiClient:
    """A class for interacting with the VerifyMedicalAI app providing high productivity and
    strongly typed methods to deploy and call the app"""

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account | None = None,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        """
        VerifyMedicalAiClient can be created with an app_id to interact with an existing application, alternatively
        it can be created with a creator and indexer_client specified to find existing applications by name and creator.
        
        :param AlgodClient algod_client: AlgoSDK algod client
        :param int app_id: The app_id of an existing application, to instead find the application by creator and name
        use the creator and indexer_client parameters
        :param str | Account creator: The address or Account of the app creator to resolve the app_id
        :param IndexerClient indexer_client: AlgoSDK indexer client, only required if deploying or finding app_id by
        creator and app name
        :param AppLookup existing_deployments:
        :param TransactionSigner | Account signer: Account or signer to use to sign transactions, if not specified and
        creator was passed as an Account will use that.
        :param str sender: Address to use as the sender for all transactions, will use the address associated with the
        signer if not specified.
        :param TemplateValueMapping template_values: Values to use for TMPL_* template variables, dictionary keys should
        *NOT* include the TMPL_ prefix
        :param str | None app_name: Name of application to use when deploying, defaults to name defined on the
        Application Specification
            """

        self.app_spec = APP_SPEC
        
        # calling full __init__ signature, so ignoring mypy warning about overloads
        self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
            algod_client=algod_client,
            app_spec=self.app_spec,
            app_id=app_id,
            creator=creator,
            indexer_client=indexer_client,
            existing_deployments=existing_deployments,
            signer=signer,
            sender=sender,
            suggested_params=suggested_params,
            template_values=template_values,
            app_name=app_name,
        )

    @property
    def algod_client(self) -> algosdk.v2client.algod.AlgodClient:
        return self.app_client.algod_client

    @property
    def app_id(self) -> int:
        return self.app_client.app_id

    @app_id.setter
    def app_id(self, value: int) -> None:
        self.app_client.app_id = value

    @property
    def app_address(self) -> str:
        return self.app_client.app_address

    @property
    def sender(self) -> str | None:
        return self.app_client.sender

    @sender.setter
    def sender(self, value: str) -> None:
        self.app_client.sender = value

    @property
    def signer(self) -> TransactionSigner | None:
        return self.app_client.signer

    @signer.setter
    def signer(self, value: TransactionSigner) -> None:
        self.app_client.signer = value

    @property
    def suggested_params(self) -> algosdk.transaction.SuggestedParams | None:
        return self.app_client.suggested_params

    @suggested_params.setter
    def suggested_params(self, value: algosdk.transaction.SuggestedParams | None) -> None:
        self.app_client.suggested_params = value

    def get_local_state(self, account: str | None = None) -> LocalState:
        """Returns the application's local state wrapped in a strongly typed class with options to format the stored value"""

        state = typing.cast(dict[bytes, bytes | int], self.app_client.get_local_state(account, raw=True))
        return LocalState(state)

    def record_ai_info(
        self,
        *,
        name: str,
        used_model: str,
        medical_degree: str,
        mcat_score: int,
        residency_training: bool,
        medical_license: bool,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `record_ai_info(string,string,string,uint64,bool,bool)void` ABI method
        
        :param str name: The `name` ABI parameter
        :param str used_model: The `used_model` ABI parameter
        :param str medical_degree: The `medical_degree` ABI parameter
        :param int mcat_score: The `mcat_score` ABI parameter
        :param bool residency_training: The `residency_training` ABI parameter
        :param bool medical_license: The `medical_license` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = RecordAiInfoArgs(
            name=name,
            used_model=used_model,
            medical_degree=medical_degree,
            mcat_score=mcat_score,
            residency_training=residency_training,
            medical_license=medical_license,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def get_ai_info(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[AiInfo]:
        """Calls `get_ai_info()(string,string,string,uint64,bool,bool)` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[AiInfo]: The result of the transaction"""

        args = GetAiInfoArgs()
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        elements = self.app_spec.hints[args.method()].structs["output"]["elements"]
        result_dict = {element[0]: value for element, value in zip(elements, result.return_value)}
        result.return_value = AiInfo(**result_dict)
        return result

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Creates an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.create(
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return result

    def opt_in_bare(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the opt_in bare method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.opt_in(
            call_abi_method=False,
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
        )
        return result

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass
        :returns algokit_utils.TransactionResponse: The result of the transaction"""
    
        return self.app_client.clear_state(_convert_transaction_parameters(transaction_parameters), app_args)

    def deploy(
        self,
        version: str | None = None,
        *,
        signer: TransactionSigner | None = None,
        sender: str | None = None,
        allow_update: bool | None = None,
        allow_delete: bool | None = None,
        on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
        on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: algokit_utils.DeployCallArgs | None = None,
        update_args: algokit_utils.DeployCallArgs | None = None,
        delete_args: algokit_utils.DeployCallArgs | None = None,
    ) -> algokit_utils.DeployResponse:
        """Deploy an application and update client to reference it.
        
        Idempotently deploy (create, update/delete if changed) an app against the given name via the given creator
        account, including deploy-time template placeholder substitutions.
        To understand the architecture decisions behind this functionality please see
        <https://github.com/algorandfoundation/algokit-cli/blob/main/docs/architecture-decisions/2023-01-12_smart-contract-deployment.md>
        
        ```{note}
        If there is a breaking state schema change to an existing app (and `on_schema_break` is set to
        'ReplaceApp' the existing app will be deleted and re-created.
        ```
        
        ```{note}
        If there is an update (different TEAL code) to an existing app (and `on_update` is set to 'ReplaceApp')
        the existing app will be deleted and re-created.
        ```
        
        :param str version: version to use when creating or updating app, if None version will be auto incremented
        :param algosdk.atomic_transaction_composer.TransactionSigner signer: signer to use when deploying app
        , if None uses self.signer
        :param str sender: sender address to use when deploying app, if None uses self.sender
        :param bool allow_delete: Used to set the `TMPL_DELETABLE` template variable to conditionally control if an app
        can be deleted
        :param bool allow_update: Used to set the `TMPL_UPDATABLE` template variable to conditionally control if an app
        can be updated
        :param OnUpdate on_update: Determines what action to take if an application update is required
        :param OnSchemaBreak on_schema_break: Determines what action to take if an application schema requirements
        has increased beyond the current allocation
        :param dict[str, int|str|bytes] template_values: Values to use for `TMPL_*` template variables, dictionary keys
        should *NOT* include the TMPL_ prefix
        :param algokit_utils.DeployCallArgs | None create_args: Arguments used when creating an application
        :param algokit_utils.DeployCallArgs | None update_args: Arguments used when updating an application
        :param algokit_utils.DeployCallArgs | None delete_args: Arguments used when deleting an application
        :return DeployResponse: details action taken and relevant transactions
        :raises DeploymentError: If the deployment failed"""

        return self.app_client.deploy(
            version,
            signer=signer,
            sender=sender,
            allow_update=allow_update,
            allow_delete=allow_delete,
            on_update=on_update,
            on_schema_break=on_schema_break,
            template_values=template_values,
            create_args=_convert_deploy_args(create_args),
            update_args=_convert_deploy_args(update_args),
            delete_args=_convert_deploy_args(delete_args),
        )

    def compose(self, atc: AtomicTransactionComposer | None = None) -> Composer:
        return Composer(self.app_client, atc or AtomicTransactionComposer())

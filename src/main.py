import argparse
import sys
from rpc import ProtocolRpcService
from output import ProtocolOutput, NodeIdentification
from input import ProtocolInput
from protocol import ProtocolCore
from ui import ProtocolPyQtUi
from PyQt6.QtWidgets import QApplication, QPlainTextEdit
from text_editor import DemoTextEditor


def parse_node(value):
    if "=" not in value:
        raise ValueError(f"Node '{value}' must be in the form <id>=<host>:<port>")

    node_id_text, address = value.split("=", 1)
    if ":" not in address:
        raise ValueError(f"Node '{value}' must include a host:port address")

    try:
        node_id = int(node_id_text)
    except ValueError as exc:
        raise ValueError(f"Node id '{node_id_text}' is not an integer") from exc

    host, port_text = address.rsplit(":", 1)
    try:
        port = int(port_text)
    except ValueError as exc:
        raise ValueError(f"Port '{port_text}' is not an integer") from exc

    return node_id, host, port


def parse_args():
    parser = argparse.ArgumentParser(description="Start a tracked text editor node")
    parser.add_argument("--port", type=int, required=True, help="Local port for this node")
    parser.add_argument("--id", type=int, required=True, help="Node id in the range 0..N-1")
    parser.add_argument(
        "--nodes",
        nargs="*",
        required=True,
        help="List of other node addresses in the form <id>=<host>:<port>",
    )
    args = parser.parse_args()

    try:
        nodes = [parse_node(node) for node in args.nodes]
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    node_ids = [node_id for node_id, _, _ in nodes]
    if len(set(node_ids)) != len(node_ids):
        raise SystemExit("Node ids must be unique")

    if any(node_id < 0 for node_id in node_ids):
        raise SystemExit("Node ids must be non-negative")

    if args.id in node_ids:
        raise SystemExit("Node list must not include the current node id")

    if not 0 <= args.id <= len(nodes):
        raise SystemExit("--id must be in the range 0...N where N is the number of node addresses")

    args.nodes = nodes
    return args


if __name__ == "__main__":
    args = parse_args()

    nodes = list(map(
        lambda n: NodeIdentification(
            id=n[0],
            host=n[1],
            port=n[2]
        ),
        args.nodes
    ))
    node_count = len(nodes) + 1

    ui = ProtocolPyQtUi()
    output = ProtocolOutput(nodes)
    core = ProtocolCore(args.id, output, ui)
    input = ProtocolInput(core)
    rpcService = ProtocolRpcService(input)

    app = QApplication(sys.argv)
    editor = DemoTextEditor(core, ui)
    editor.setWindowTitle(f"Tracked Text Edit - node {args.id} : port {args.port}")
    editor.resize(500, 300)
    editor.show()

    sys.exit(app.exec())
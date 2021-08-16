import json


def send_msg(obj, conn):
    msg_json = json.dumps(obj)
    # print("sending message: " + msg_json)
    encoded_json = msg_json.encode()
    conn.sendall(encoded_json)


def recv_msg(conn):
    data = ""
    # print("receiving message: \n")
    while True:
        recv_data = conn.recv(1)
        # print(recv_data.decode() + "\n")
        data += recv_data.decode()
        try:
            recv_json = json.loads(data)
            break
        except json.JSONDecodeError:
            pass
    return recv_json

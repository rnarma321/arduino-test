from pickle import TRUE
from re import T
import serial
from enum import IntEnum
import random
import time


START_MSG = 128
END_MSG = 129
START_ACK = 130
END_ACK = 131


class Commands(IntEnum):
    CLEAR_BUFFER = -1
    GET_COMMANMD_LIST = 0
    GET_ID = 1
    READY_FOR_WALK = 2
    WALKING = 3
    LOADING = 4
    SCORE_DISPLAY = 5
    ERROR = 6
    INVALID_WALK = 7
    TURN_OFF_EXIT_LIGHTS = 8
    TURN_OFF_ENTRY_LIGHTS = 9
    SHUTDOWN_ANIMATIONS = 10
    OVERHEAT_ANIMATION = 11
    CLEAR_TEMPERATURE_WARNING = 13
    SET_ENTRY_NUMBERS = 14
    SET_EXIT_NUMBERS = 15


def send_message(
    comm: serial.Serial, cmd: Commands, ack_request: bool, data: list[int]
) -> bool:
    if cmd == Commands.GET_COMMANMD_LIST:
        command_message()
        return True
    if cmd == Commands.CLEAR_BUFFER:
        comm.flush()
        return True
    int_msg = [START_MSG, cmd.value, int(ack_request), *data, END_MSG]
    byte_msg = bytearray(int_msg)
    print(f"sending bytes: {byte_msg}")
    print(f"Int_msg: {int_msg}")
    try:
        comm.write(byte_msg)
    except Exception as e:
        print(e)
        print("Cannot write to Arduino", flush=True)
        return False

    if not ack_request:
        return True

    reply = read_ack_request(comm, time_to_wait=1)
    if not reply:
        print("FAILED ACK REQUEST")
        return False
    print(f"Working ack: {reply}")
    return True

    # break

    # print(f"sending {byte_msg}")
    # for msg_part in final_msg:
    #     try:
    #         comm.write(msg_part.to_bytes(1, "little", signed=False))
    #     except Exception as e:
    #         print(e)
    #         print("Cannot write to Arduino", flush=True)
    #         break


def read_ack_request(
    comm: serial.Serial, timeout: int = 5, time_to_wait: float = 0.1
) -> list:
    msg_started = False
    msg = []
    time.sleep(time_to_wait)
    while comm.in_waiting:
        msg_part = int.from_bytes(comm.read(), "little")
        # int.from_bytes(msg_part,byteorder="little")
        # print(f"msg_part: {msg_part}")
        if msg_started and msg_part == START_ACK:
            msg_started = True
        else:
            if msg_part == END_ACK:
                msg.append(msg_part)
                # msg_started = False
                return msg
            else:
                msg.append(msg_part)
    print(msg)
    return []  # did not return a full message


def command_message():
    for name, member in Commands.__members__.items():
        print(f"CMD {member.value} = {name.replace('_',' ')}")


def main():
    arduino_serial = serial.Serial("/dev/ttyACM0", baudrate=250000)
    command_message()
    while True:
        # for _ in range(100):
        # time.sleep(1)
        command_number = (int)(input("Enter command: "))
        # command_number = random.randint(1, 10)
        command = Commands(command_number)
        send_message(arduino_serial, command, ack_request=True, data=[0, 1, 2, 3])


if __name__ == "__main__":
    main()
    # arduino_serial = serial.Serial("/dev/ttyACM0", baudrate=115200)
    # send_message(arduino_serial, Commands.GET_ID, [0, 0, 0])
